from pwn import *
from Crypto.Util.Padding import pad
from hashlib import sha256

HOST = "localhost" # change to the actual host
PORT = 1346 # change to the actual port

def generate_product_share(a_share, b_share, c_share, d, e, p):
    prod_share = d * e + d * b_share + a_share * e + c_share

    return prod_share % p

def xor(nums):
    res = 0
    for n in nums:
        res ^= n

    return res

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

def lagrange_interpolation(shares, p, n):
    coeffs = lagrange_coeffs([i+1 for i in range(n)], p)
    s = 0
    for i in range(n):
        s += shares[i] * coeffs[i]

    return s % p

def main():
    conn = remote(HOST, PORT)

    p = 65537

    table = []
    for _ in range(16):
        shares = conn.recvline().strip().decode()
        table.append(list(map(int, shares.split("|"))))

    conn.recvuntil(b"d share: ")
    d_share2 = int(conn.recvline().strip().decode())
    conn.recvuntil(b"e share: ")
    e_share2 = int(conn.recvline().strip().decode())

    for j in range(10):
        # compute shares
        x_share1 = xor([table[i][0] for i in range(16) if i != j]) % p
        y_share1 = xor([table[i][1] for i in range(16) if i != j]) % p
        a_share1 = xor([table[i][2] for i in range(16) if i != j]) % p
        b_share1 = xor([table[i][3] for i in range(16) if i != j]) % p
        c_share1 = xor([table[i][4] for i in range(16) if i != j]) % p

        # compute d, e
        d_share1 = (x_share1 - a_share1) % p
        e_share1 = (y_share1 - b_share1) % p
        conn.sendline(str(d_share1).encode())
        conn.sendline(str(e_share1).encode())
        d = lagrange_interpolation([d_share1, d_share2], p, 2)
        e = lagrange_interpolation([e_share1, e_share2], p, 2)

        # compute prod
        conn.recvuntil(b"Product share: ")
        prod_share2 = int(conn.recvline().strip().decode())
        prod_share1 = generate_product_share(a_share1, b_share1, c_share1, d, e, p)
        prod = lagrange_interpolation([prod_share1, prod_share2], p, 2)

        secret = sha256(str((prod)).encode()).digest()[:16].hex().encode()
        conn.sendline(secret)
        conn.recvline()
        flag = bytes.fromhex(conn.recvline().strip().decode())
        if flag[:4] == b'RHUL':
            print(flag)

    conn.close()

if __name__ == "__main__":
    main()