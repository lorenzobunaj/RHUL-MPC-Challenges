import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def pwn_print(conn, message: str):
    conn.sendline(message.encode())

def pwn_input(conn, prompt: str) -> str:
    conn.send(prompt.encode())
    return conn.recvline().decode().strip()

def xor(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def random_oracle(val, l):
    r = random.Random()
    r.seed(val)
    indices = r.sample(range(l), 3)

    return tuple(indices)

def H(val : bytes):
    k1 = [v for v in val[:4]]
    random.shuffle(k1)
    k1 = bytes(k1)

    k2 = [v for v in val[4:8]]
    k2 = xor(k1, k2)

    k3 = [v for v in val[8:12]]
    random.shuffle(k3)
    k3 = bytes(k3)

    k4 = [v for v in val[12:16]]
    k4 = xor(k3, k4)

    return k1 + k2 + k3 + k4

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))