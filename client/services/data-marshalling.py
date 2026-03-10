import struct
import socket

# ── Constants ──────────────────────────────────────────────────────────────
# Currency enum codes get from utis/currency-mapping.py

# Service IDs
OPEN_ACCOUNT     = 0
CLOSE_ACCOUNT    = 1
CHECK_BALANCE    = 2
CHANGE_PASSWORD   = 3
DEPOSIT_WITHDRAW = 4
MONITOR_UPDATES  = 5


# ── Primitive Packers (Network Byte Order = Big-Endian) ────────────────────

def pack_int(value: int) -> bytes:
    """4-byte signed int, big-endian (equivalent to htonl)"""
    return struct.pack("!i", value)

def pack_float(value: float) -> bytes:
    """4-byte IEEE 754 float, big-endian"""
    return struct.pack("!f", value)

def pack_enum(value: int) -> bytes:
    """Enums transmitted as 4-byte int"""
    return pack_int(value)

def pack_string(value: str) -> bytes:
    """Variable-length string: [4-byte length prefix][utf-8 bytes]"""
    encoded = value.encode("utf-8")
    return pack_int(len(encoded)) + encoded

def pack_fixed_string(value: str, size: int) -> bytes:
    """Fixed-length string (e.g. password): padded/truncated to exact size"""
    encoded = value.encode("utf-8")
    return encoded[:size].ljust(size, b'\x00')

# ── Request Header (sent with every request) ──────────────────────────────
# | requestID (4) | serviceID (4) |  →  8 bytes

def pack_header(request_id: int, service_id: int) -> bytes:
    return pack_int(request_id) + pack_int(service_id)
