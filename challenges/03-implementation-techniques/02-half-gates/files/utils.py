import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def pwn_print(conn, message: str):
    conn.sendline(message.encode())

def pwn_input(conn, prompt: str) -> str:
    pwn_print(conn, prompt)
    return conn.recvline().decode().strip()

def H(label: bytes) -> bytes:
    return hashlib.sha256(label).digest()[:8]

def random_oracle(label: bytes) -> bytes:
    return hashlib.sha256(label).digest()[:16]

def xor(x: bytes, y: bytes) -> bytes:
    return bytes([xi ^ yi for xi, yi in zip(x,y)])

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))

def bytesToBits(bytes):
    bits = []
    for byte in bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def bitsToBytes(bits):
    byte_arr = []

    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte |= (bits[i + j] << (7 - j))
        byte_arr.append(byte)

    return bytes(byte_arr)