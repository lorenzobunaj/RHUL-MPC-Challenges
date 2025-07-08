import hashlib

def xor(a: bytes, b: bytes) -> bytes:
    return bytes([x ^ y for x, y in zip(a, b)])

def H(label1: bytes, label2: bytes) -> bytes:
    return hashlib.sha256(label1 + label2).digest()