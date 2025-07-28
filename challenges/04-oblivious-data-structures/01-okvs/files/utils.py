import random
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

def xor(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def random_oracle(val, l):
    r = random.Random()
    r.seed(val)
    indices = r.sample(range(l), 3)

    return tuple(indices)

def H(val : bytes):
    k1 = val[:4]
    k2 = val[4:8]
    k3 = val[8:12]
    k4 = val[12:16]

    k1 = xor(k4, k1)
    k2 = xor(k1, k2)
    k3 = xor(k2, k3)
    k4 = xor(k3, k4)

    return k1 + k2 + k3 + k4

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))