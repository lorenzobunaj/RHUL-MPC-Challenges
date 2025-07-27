from pwn import *
from Crypto.Cipher import AES
import hashlib

HOST = "localhost" # change to the actual host
PORT = 1354 # change to the actual port

def xor(x: bytes, y: bytes) -> bytes:
    return bytes([xi ^ yi for xi, yi in zip(x,y)])

def H(label1: bytes, label2: bytes) -> bytes:
    if len(label1) < 16:
        raise ValueError
    
    return hashlib.sha256(label1 + label2).digest()

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

def main():
    conn = remote(HOST, PORT)

    la = [bytes([0] * 16), bytes([1] * 16)]

    conn.sendline(la[0].hex().encode())
    conn.sendline(la[0].hex().encode())
    conn.recvuntil(b"La1: \n")
    table0 = []
    for _ in range(4):
        table0.append(bytes.fromhex(conn.recvline().strip().decode()))

    conn.sendline(la[1].hex().encode())
    conn.sendline(la[1].hex().encode())
    conn.recvuntil(b"La1: \n")
    table1 = []
    for _ in range(4):
        table1.append(bytes.fromhex(conn.recvline().strip().decode()))

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ct: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    h = xor(table0[1], table1[0])
    delta = xor(table0[1], table0[3])

    flag = decrypt(ct, H(h, delta), iv)

    print(flag)

    conn.close()

if __name__ == "__main__":
    main()