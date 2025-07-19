from pwn import *
from Crypto.Cipher import AES

HOST = "localhost" # change to the actual host
PORT = 1355 # change to the actual port

def decrypt(ct, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)

    return pt

def H(label: bytes) -> bytes:
    return hashlib.sha256(label).digest()[:8]

def random_oracle(label: bytes) -> bytes:
    return hashlib.sha256(label).digest()[:16]

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

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ct: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    vc = []
    for _ in range(64):
        conn.recvline()

        conn.recvuntil(b"a: ")
        a = bytes.fromhex(conn.recvline().strip().decode())
        conn.recvuntil(b"output: ")
        h = bytes.fromhex(conn.recvline().strip().decode())
        c = xor(H(a), h)
        vc1 = bytesToBits(c)[-1]

        conn.recvuntil(b"b: ")
        b = bytes.fromhex(conn.recvline().strip().decode())
        conn.recvuntil(b"va: ")
        va = int(conn.recvline().strip().decode())
        conn.recvuntil(b"output: ")
        h = bytes.fromhex(conn.recvline().strip().decode())
        if va == 0:
            c = H(a)
        else:
            c = xor(xor(H(a), h), b)
        vc2 = bytesToBits(c)[-1]

        vc.append(vc1 ^ vc2)

    secret = random_oracle(bitsToBytes(vc))
    print(decrypt(ct, secret, iv))

    conn.close()

if __name__ == "__main__":
    main()

