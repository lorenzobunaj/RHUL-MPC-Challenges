import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def pwn_print(conn, message):
    conn.sendall((message + "\n").encode())

def pwn_input(conn, prompt):
    pwn_print(conn, prompt)
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            break
        data += chunk
    return data.strip().decode()

def H(label1: bytes, label2: bytes) -> bytes:
    if len(label1) < 16:
        raise ValueError
    
    return hashlib.sha256(label1 + label2).digest()

def xor(x: bytes, y: bytes) -> bytes:
    return bytes([xi ^ yi for xi, yi in zip(x,y)])

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))