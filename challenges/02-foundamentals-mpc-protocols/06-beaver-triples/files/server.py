import socket
import threading
from Crypto.Random import get_random_bytes
from random import randint, shuffle
from hashlib import sha256
from utils import *
from private.secret_functions import generate_product_share, lagrange_interpolation

PORT = 1346
with open("flag.txt") as f:
    FLAG = f.read().strip()

def generate_shares(secret, p, n):
    a = randint(1, p-1)
    shares = []
    for i in range(1, n + 1):
        shares.append((a * i + secret) % p)

    return shares

def generate_xor_shares(v, p, n):
    shares = [randint(0, p-1) for _ in range(n - 1)]
    last = v
    for s in shares:
        last ^= s 
    
    shares.append(last)

    return shares

def challenge(conn):
    p = 65537

    x = randint(0, p-1)
    y = randint(0, p-1)
    a = randint(0, p-1)
    b = randint(0, p-1)
    c = (a * b) % p

    x_shares = generate_shares(x, p, 2)
    y_shares = generate_shares(y, p, 2)
    a_shares = generate_shares(a, p, 2)
    b_shares = generate_shares(b, p, 2)
    c_shares = generate_shares(c, p, 2)

    x_xor_shares = generate_xor_shares(x_shares[0], p, 15) + generate_xor_shares(x_shares[1], p, 15)
    y_xor_shares = generate_xor_shares(y_shares[0], p, 15) + generate_xor_shares(y_shares[1], p, 15)
    a_xor_shares = generate_xor_shares(a_shares[0], p, 15) + generate_xor_shares(a_shares[1], p, 15)
    b_xor_shares = generate_xor_shares(b_shares[0], p, 15) + generate_xor_shares(b_shares[1], p, 15)
    c_xor_shares = generate_xor_shares(c_shares[0], p, 15) + generate_xor_shares(c_shares[1], p, 15)

    table = []
    table.append([randint(0, p-1), randint(0, p-1), randint(0, p-1), randint(0, p-1), randint(0, p-1)])
    for i in range(15):
        table.append([
            x_xor_shares[i],
            y_xor_shares[i],
            a_xor_shares[i],
            b_xor_shares[i],
            c_xor_shares[i]
        ])

    iv = get_random_bytes(16)
    secret = sha256(str((x * y) % p).encode()).digest()[:16]
    ct = encrypt(FLAG.encode(), secret, iv)

    shuffle(table)
    for r in table:
        pwn_print(conn, f"{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}")

    x_share2 = xor(x_xor_shares[15:]) % p
    y_share2 = xor(y_xor_shares[15:]) % p
    a_share2 = xor(a_xor_shares[15:]) % p
    b_share2 = xor(b_xor_shares[15:]) % p
    c_share2 = xor(c_xor_shares[15:]) % p

    d_share2 = (x_share2 - a_share2) % p
    e_share2 = (y_share2 - b_share2) % p

    pwn_print(conn, f"d share: {d_share2}")
    pwn_print(conn, f"e share: {e_share2}")

    for _ in range(10):
        d_share1 = int(pwn_input(conn, "Your d share: "))
        e_share1 = int(pwn_input(conn, "Your e share: "))

        d = lagrange_interpolation([d_share1, d_share2], p, 2)
        e = lagrange_interpolation([e_share1, e_share2], p, 2)

        prod_share2 = generate_product_share(a_share2, b_share2, c_share2, d, e, p) # generates prod share using beaver triples
        pwn_print(conn, f"Product share: {prod_share2}")

        secret_guess = bytes.fromhex(pwn_input(conn, "Secret: "))

        pwn_print(conn, decrypt(ct, secret_guess, iv).hex())

    conn.close()

def handle_client(conn):
    try:
        challenge(conn)
    except Exception as e:
        print(f"Error handling client: {repr(e)}")
    finally:
        conn.close()

def main():
    print(f"[+] Server listening on port {PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        print(f"[*] New connection received from {addr}")
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()