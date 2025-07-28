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

def encrypt(pt, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(pt, AES.block_size))

    return ct

def decrypt(ct, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)

    return pt

def bitsToBytes(bits):
    byte_arr = []

    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte |= (bits[i + j] << (7 - j))
        byte_arr.append(byte)

    return bytes(byte_arr)

def bytesToBits(bytes):
    bits = []
    for byte in bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def xorBytes(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def notBytes(a):
    return bytes([ai ^ 0xff for ai in a])

def andBytes(a, b):
    return bytes([ai & bi for ai, bi in zip(a, b)])