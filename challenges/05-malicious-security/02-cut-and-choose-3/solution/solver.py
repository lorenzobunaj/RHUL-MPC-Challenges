from pwn import *
import hashlib
from lagrange_interpolation import lagrange_coefficients

HOST = "localhost" # change to the actual host
PORT = 1366 # change to the actual port

CIRCUITS_NUM = 96
T = 32

def random_coeffs(coeffs, x):
    p = (1 << 127) - 1
    y = 0
    for a in reversed(coeffs):
        y = (y * x + a) % p
    return y.to_bytes(16, "big")

def H(data: bytes):
    return hashlib.sha256(data).digest()[:16]

def main():
    conn = remote(HOST, PORT)

    commitments = []
    for i in range(CIRCUITS_NUM):
        conn.recvuntil(f"C[{i}]: ".encode())
        C = bytes.fromhex(conn.recvline().strip().decode())

        commitments.append(C)

    payload_choice = b"1" * T + b"0" * (CIRCUITS_NUM - T)
    conn.sendline(payload_choice)

    seeds = []
    for i in range(T):
        conn.recvuntil(f"Seed[{i}]: ".encode())
        s = bytes.fromhex(conn.recvline().strip().decode())

        seeds.append(s)
    
    choosen_masks = [bytes(a ^ b for a, b in zip(commitments[i], H(seeds[i] + i.to_bytes(4, 'big')))) for i in range(T)]
    coeffs = lagrange_coefficients(list(range(T)), [int.from_bytes(m) for m in choosen_masks])

    payload_x = bytes([255] * 8).hex()
    conn.sendline(payload_x.encode())

    s_bits = []
    for i in range(T, CIRCUITS_NUM):
        conn.recvuntil(f"Label[{i}]: ".encode())
        label = bytes.fromhex(conn.recvline().strip().decode())
        conn.recvuntil(f"preL0[{i}]: ".encode())
        preL0 = bytes.fromhex(conn.recvline().strip().decode())

        label_unmasked = bytes(a ^ b for a, b in zip(random_coeffs(coeffs, i), label))

        s_bits.append(int(label_unmasked == preL0))
    
    s = s[::-1]
    s = int(''.join(str(bit) for bit in s_bits), 2).to_bytes(len(s_bits) // 8, byteorder='big')

    conn.sendline(s.hex().encode())

    conn.recvuntil(b"flag: ")
    flag = conn.recvline().strip().decode()

    print(flag)

    conn.close()

if __name__ == "__main__":
    main()

