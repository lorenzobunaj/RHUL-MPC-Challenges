from pwn import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import re
import ast

HOST = "localhost" # change to the actual host
PORT = 1361 # change to the actual port

def parse_bucket(bucket_str):
    tuple_strs = re.findall(r"\(\d+, b'(?:[^'\\]|\\.)*'\)", bucket_str)
    return [eval(ts) for ts in tuple_strs]

def read_position_map(conn):
    conn.recvuntil(b"Position map:\n")
    pm_pairs = re.findall(r'\((\d+)\s*:\s*(\d+)\)', conn.recvline().strip().decode())
    position_map = {int(k): int(v) for k, v in pm_pairs}

    return position_map

def read_tree(conn):
    conn.recvuntil(b"Tree:\n")
    tree = conn.recvline().strip().decode()
    tree = []
    for _ in range(2 * N - 1):
        conn.recvuntil(b"| ")
        bucket_str = conn.recvline().strip().decode()
        if bucket_str == "":
            tree.append([])
        else:
            tree.append(parse_bucket(bucket_str))

    return tree

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

    for _ in range(pow(2,5) - 1):
        conn.sendline(b"0")
        conn.sendline(f"{target}".encode())
        conn.sendline(b"1")
    
    position_map = read_position_map(conn)
    c = position_map[target]

    print(a, b, c)

    conn.close()

if __name__ == "__main__":
    main()