from pwn import *
import re
from sympy.ntheory.residue_ntheory import n_order
from math import gcd

HOST = "localhost" # change to the actual host
PORT = 1362 # change to the actual port

def read_position_map(conn):
    conn.recvuntil(b"Position map:\n")
    pm_pairs = re.findall(r'\((\d+)\s*:\s*(\d+)\)', conn.recvline().strip().decode())
    position_map = {int(k): int(v) for k, v in pm_pairs}

    return position_map

def has_multiplicative_order(g, q, n):
    if gcd(g, n) != 1:
        return False  # g must be in the multiplicative group mod n
    return n_order(g, n) == q

N = 65537
Z = 65537
d = pow(2,5)
def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ciphertext: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())
    
    print("iv =", iv)
    print("ct =", ct)

    g_list = []
    A_list = []
    B_list = []

    for rc in range(8):
        # recover t
        conn.sendline(b"1")
        position_map = read_position_map(conn)
        for i in range(N):
            if has_multiplicative_order(position_map[i], N - 1, N):
                target = i
        a = position_map[target]

        # recover t^s
        conn.sendline(b"0")
        conn.sendline(f"{target}".encode())
        conn.sendline(b"1")
        position_map = read_position_map(conn)
        b = position_map[target]

        # recover t^(s^d)
        for i in range(d - 1):
            conn.sendline(b"0")
            conn.sendline(f"{target}".encode())
        
        conn.sendline(b"1")
        
        position_map = read_position_map(conn)
        c = position_map[target]

        print(f"reset {rc+1}")
        g_list.append(a)
        A_list.append(b)
        B_list.append(c)

        if rc != 7:
            conn.sendline(b"2")

    print("g_list =", g_list)
    print("A_list =", A_list)
    print("B_list =", B_list)

    conn.close()

if __name__ == "__main__":
    main()