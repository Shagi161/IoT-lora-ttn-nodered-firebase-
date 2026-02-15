import argparse
import base64
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from encoder import encode_payload
from decoder import decode_payload_b64
from firebase_writer import append_jsonl, push_to_firebase

OUTPUT_UPLINKS = Path("output/uplinks.jsonl")
OUTPUT_DECODED = Path("output/decoded.jsonl")

def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def ttn_like_uplink(device_id: str, payload_b64: str, f_port: int = 1) -> Dict[str, Any]:
    # Simplified TTN-like structure (enough for portfolio + decoder integration)
    return {
        "end_device_ids": {
            "device_id": device_id,
            "application_ids": {"application_id": "demo-app"}
        },
        "received_at": iso_now(),
        "uplink_message": {
            "f_port": f_port,
            "frm_payload": payload_b64,
            "rx_metadata": [
                {
                    "gateway_ids": {"gateway_id": "demo-gateway"},
                    "rssi": random.randint(-120, -30),
                    "snr": round(random.uniform(-20, 10), 1)
                }
            ]
        }
    }

def generate_sensor_reading() -> Dict[str, float]:
    return {
        "temperature_c": round(random.uniform(18.0, 32.0), 2),
        "humidity_pct": round(random.uniform(30.0, 80.0), 2),
        "battery_v": round(random.uniform(3.5, 4.2), 3),
    }

def main(count: int, interval: float, device_id: str,
         firebase_url: Optional[str], firebase_token: Optional[str]) -> None:
    print(f"Simulating {count} uplinks for device_id='{device_id}' ...")

    for i in range(count):
        reading = generate_sensor_reading()
        raw = encode_payload(reading["temperature_c"], reading["humidity_pct"], reading["battery_v"])
        payload_b64 = base64.b64encode(raw).decode("ascii")

        uplink = ttn_like_uplink(device_id, payload_b64)
        decoded_vals = decode_payload_b64(payload_b64)

        decoded_record = {
            "device_id": device_id,
            "time_utc": uplink["received_at"],
            **decoded_vals,
            "rssi": uplink["uplink_message"]["rx_metadata"][0]["rssi"],
            "snr": uplink["uplink_message"]["rx_metadata"][0]["snr"],
        }

        append_jsonl(OUTPUT_UPLINKS, uplink)
        append_jsonl(OUTPUT_DECODED, decoded_record)

        print(f"[{i+1}/{count}] payload={payload_b64} -> {decoded_vals}")

        if firebase_url:
            code = push_to_firebase(firebase_url, "telemetry", decoded_record, firebase_token)
            print(f"  Firebase POST status: {code}")

        if i < count - 1:
            time.sleep(interval)

    print("\nSaved:")
    print(f"- {OUTPUT_UPLINKS}")
    print(f"- {OUTPUT_DECODED}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--interval", type=float, default=2.0)
    p.add_argument("--device-id", type=str, default="esp32-lora-demo")
    p.add_argument("--firebase-url", type=str, default=None, help="e.g., https://YOUR-PROJECT.firebaseio.com")
    p.add_argument("--firebase-token", type=str, default=None, help="optional auth token")
    args = p.parse_args()
    main(args.count, args.interval, args.device_id, args.firebase_url, args.firebase_token)

