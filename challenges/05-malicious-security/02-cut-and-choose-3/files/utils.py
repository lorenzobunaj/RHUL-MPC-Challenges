import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter

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

def pwn_input_inline(conn, prompt):
    conn.sendall((prompt).encode())
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            break
        data += chunk
    return data.strip().decode()

def H(data: bytes):
    return hashlib.sha256(data).digest()[:16]

def PRG(seed):
    ctr = Counter.new(128)
    cipher = AES.new(seed.ljust(16, b'\x00')[:16], AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(b'\x00' * 16)

def bytes_to_bits(bs):
    return [(b >> i) & 1 for b in bs for i in reversed(range(8))]