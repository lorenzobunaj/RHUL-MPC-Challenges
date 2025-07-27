import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def H(label1: bytes, label2: bytes) -> bytes:
    return hashlib.sha256(label1 + label2).digest()[:16]

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))