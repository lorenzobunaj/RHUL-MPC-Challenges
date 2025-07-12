from pwn import *
from Crypto.Random import get_random_bytes

HOST = "localhost" # change to the actual host
PORT = 1345 # change to the actual port

def generate_shares(secret, n, p):
    a = randint(1, p)
    shares = []
    for i in range(1, n + 1):
        shares.append((a * i + secret) % p)
    return shares

def modinv(a, p):
    return pow(a, -1, p)

def lagrange_coeffs(x_s, p):
    coeffs = []
    for j, xj in enumerate(x_s):
        num = 1
        denom = 1
        for m, xm in enumerate(x_s):
            if m != j:
                num = (num * (-xm)) % p
                denom = (denom * (xj - xm)) % p
        lambda_j = (num * modinv(denom, p)) % p
        coeffs.append(lambda_j)
    return coeffs

def lagrange_interpole(shares, p):
    coeffs = lagrange_coeffs([i+1 for i in range(3)], p)
    s = 0
    for i in range(3):
        s += shares[i] * coeffs[i]

    return s % p

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"z: ")
    z = int(conn.recvline().strip().decode())
    conn.recvuntil(b"p: ")
    p = int(conn.recvline().strip().decode())

    z_shares = generate_shares(z, 3, p)
    for share in z_shares:
        conn.sendline(str(share).encode())

    input_shares = []
    for i in range(3):
        conn.recvuntil(f"from party {i+1}: ".encode())
        input_shares.append(int(conn.recvline().strip().decode()))

    add_shares = [(input_shares[i % 3] + input_shares[(i+1) % 3]) % p for i in range(3)]

    generated_mul1_public_shares = generate_shares(add_shares[0] * add_shares[1], 3, p)
    for share in generated_mul1_public_shares:
        conn.sendline(str(share).encode())

    mul1_public_shares = []
    for i in range(3):
        conn.recvuntil(f"from party {i+1}: ".encode())
        mul1_public_shares.append(int(conn.recvline().strip().decode()))

    mul1_share = lagrange_interpole(mul1_public_shares, p)

    generated_mul2_public_shares = generate_shares(mul1_share * add_shares[2], 3, p)
    for share in generated_mul2_public_shares:
        conn.sendline(str(share).encode())

    mul2_public_shares = []
    for i in range(3):
        conn.recvuntil(f"from party {i+1}: ".encode())
        mul2_public_shares.append(int(conn.recvline().strip().decode()))
    
    mul2_shares = []
    for i in range(2):
        conn.recvuntil(f"from party {i+1}: ".encode())
        mul2_shares.append(int(conn.recvline().strip().decode()))
    mul2_shares.append(lagrange_interpole(mul2_public_shares, p))

    secret = lagrange_interpole(mul2_shares, p) % p
    conn.sendline(str(secret).encode())

    print(conn.recvall())
    
    conn.close()

if __name__ == "__main__":
    main()