from pwn import *
from phe import paillier
import pickle
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

HOST = "localhost" # change to the actual host
PORT = 1357 # change to the actual port

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

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

def xor(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def notBytes(a):
    return bytes([ai ^ 0xff for ai in a])

def gmw_and(conn, a, b):
    for i in range(4):
        sx = i // 2
        ry = i % 2
        conn.sendline(str(0 ^ ((sx ^ a) & (ry ^ b))).encode())
    
def gmw_full_adder(conn, a, b, cin):
    s = a ^ b ^ cin
    cout = 0
    gmw_and(conn, a, b)
    gmw_and(conn, a, cin)
    gmw_and(conn, b, cin)

    return s, cout

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ct: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    public_key, private_key = paillier.generate_paillier_keypair()
    pk_hex = pickle.dumps(public_key).hex()
    conn.sendline(pk_hex.encode())

    conn.recvuntil(b"Sum of encryptions: ")
    sum_enc_bytes = bytes.fromhex(conn.recvline().strip().decode())
    sum_enc = pickle.loads(sum_enc_bytes)
    secret_sum = private_key.decrypt(sum_enc)

    rx = get_random_bytes(17)
    sx = xor(int.to_bytes(secret_sum, 17, "big"), rx)

    conn.sendline(sx.hex().encode())
    conn.recvuntil(b"Server's share: ")
    sy = bytes.fromhex(conn.recvline().strip().decode())

    sy = notBytes(sy)

    rx_bits = bytesToBits(rx)
    sy_bits = bytesToBits(sy)
    
    res = []
    cin = 0
    for i in range(len(sy_bits) - 1, -1, -1):
        s, cin = gmw_full_adder(conn, rx_bits[i], sy_bits[i], cin)
        res.insert(0, s)
    resx = bitsToBytes(res)
    conn.recvuntil(b"Final share: ")
    resy = bytes.fromhex(conn.recvline().strip().decode())

    secret = xor(resx, resy)
    for i in range(256):
        overflow = bytes([0] * 15 + [i])
        key = xor(overflow, secret[1:])
        flag = decrypt(ct, key, iv)
        if flag[:4] == b"RHUL":
            print(flag.strip())
            break

if __name__ == "__main__":
    main()