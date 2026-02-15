
## 3) `src/encoder.py`
```python
import struct

def encode_payload(temp_c: float, humidity_pct: float, battery_v: float) -> bytes:
    """
    Encode three values into a compact 6-byte payload:
    - temp_c: int16 in centi-degrees (e.g., 23.45C -> 2345)
    - humidity_pct: uint16 in centi-percent (e.g., 56.78% -> 5678)
    - battery_v: uint16 in milli-volts (e.g., 3.97V -> 3970)

    Payload format (big-endian):
    [temp_i16][hum_u16][bat_u16]
    """
    t = int(round(temp_c * 100))
    h = int(round(humidity_pct * 100))
    b = int(round(battery_v * 1000))

    # bounds protection (simple)
    t = max(-32768, min(32767, t))
    h = max(0, min(65535, h))
    b = max(0, min(65535, b))

    return struct.pack(">hHH", t, h, b)

