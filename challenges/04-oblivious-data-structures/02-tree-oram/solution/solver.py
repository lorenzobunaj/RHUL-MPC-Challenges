from pwn import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import re
import ast

HOST = "localhost" # change to the actual host
PORT = 1361 # change to the actual port

def read_position_map(conn):
    conn.recvuntil(b"Position map:\n")
    pm_pairs = re.findall(r'\((\d+)\s*:\s*(\d+)\)', conn.recvline().strip().decode())
    position_map = {int(k): int(v) for k, v in pm_pairs}

    return position_map

N = 43
Z = 43
def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ciphertext: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    # find t
    conn.sendline(b"1")
    position_map = read_position_map(conn)
    for i in range(N):
        if position_map[i] not in [0, 1]:
            target = i
    a = position_map[target]

    # find t^s
    conn.sendline(b"0")
    conn.sendline(f"{target}".encode())
    conn.sendline(b"1")
    position_map = read_position_map(conn)
    b = position_map[target]

    # find t^(s^d)
    for _ in range(pow(2,5) - 1):
        conn.sendline(b"0")
        conn.sendline(f"{target}".encode())
        conn.sendline(b"1")
    
    position_map = read_position_map(conn)
    c = position_map[target]

    print("iv = ", iv)
    print("ct = ", ct)
    print("a = ", a)
    print("b = ", b)
    print("c = ", c)

    conn.close()

if __name__ == "__main__":
    main()