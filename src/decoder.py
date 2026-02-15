import base64
import struct
from typing import Dict, Any

def decode_payload_b64(payload_b64: str) -> Dict[str, Any]:
    raw = base64.b64decode(payload_b64)
    if len(raw) != 6:
        raise ValueError(f"Unexpected payload length: {len(raw)} bytes (expected 6)")

    t, h, b = struct.unpack(">hHH", raw)
    return {
        "temperature_c": t / 100.0,
        "humidity_pct": h / 100.0,
        "battery_v": b / 1000.0,
    }

