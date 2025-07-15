from pwn import *
from Crypto.Random import get_random_bytes
from hashlib import sha256

HOST = "localhost" # change to the actual host
PORT = 1350 # change to the actual port

def xor(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def random_oracle(x, l):
    out = sha256(x).digest()[:l]

    return out

def main():
    conn = remote(HOST, PORT)

    r_choice = ""
    for i in range(16):
        r_choice += str(i % 2)
        
    conn.sendline(r_choice.encode())

    Trows = [get_random_bytes(16) for _ in range(16)]
    Urows = [xor(Trows[i], bytes([int(r_choice[i])] * 16)) for i in range(16)]

    weak_key = b'\x01\x01\x01\x01\x01\x01\x01\x01'
    for i in range(16):
        conn.sendline(Trows[i].hex().encode())
        conn.sendline(Urows[i].hex().encode())
        conn.sendline(weak_key.hex().encode())

    conn.recvuntil(b"15-th row encryption key (hex): \n")

    secret = b""
    
    for i in range(16):
        pair = conn.recvline().strip().decode()[1:-1].split(", ")
        pair = [int(pair[0]), int(pair[1])]

        h = random_oracle(Trows[i], 1)
        secret += xor(bytes([pair[int(r_choice[i])]]), h)
    
    conn.sendline(secret.hex().encode())

    conn.recvuntil(b"output: ")
    flag = bytes.fromhex(conn.recvline().strip().decode())

    print(flag)

    conn.close()

if __name__ == "__main__":
    main()