# IoT Uplink Pipeline (Simulated TTN-style) — Node-RED/Firebase Ready

This project simulates an IoT device sending compact payloads (like LoRaWAN uplinks) and produces TTN-like JSON
messages. The payload is encoded, decoded, and stored locally (and can optionally be pushed to Firebase).

✅ No hardware required.  
✅ Shows real IoT workflow: payload encoding/decoding + uplink message format + storage pipeline.

## What it demonstrates
- Compact sensor payload encoding (bytes → Base64)
- TTN-like uplink JSON generation
- Payload decoding back to engineering units
- Storage pipeline (local JSON) + optional Firebase push

## Repo structure
- `src/` simulator + encoder + decoder + storage writer
- `sample-data/` example uplink and decoded JSON
- `output/` generated logs

## How to run
1) Install Python 3
2) Install requirements:
```bash
pip install -r requirements.txt
