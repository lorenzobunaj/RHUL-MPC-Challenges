from pwn import *
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from random import randint, shuffle
from utils import *

PORT = 1346
with open("flag.txt") as f:
    FLAG = f.read().strip()

def generate_shares(v, p, n):
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

    x_shares = generate_shares(x, p, 29)
    y_shares = generate_shares(y, p, 29)
    a_shares = generate_shares(a, p, 29)
    b_shares = generate_shares(b, p, 29)
    c_shares = generate_shares(c, p, 29)

    table = [[randint(0, p-1), randint(0, p-1), randint(0, p-1), randint(0, p-1), randint(0, p-1)]]
    for i in range(29):
        table.append([
            x_shares[i],
            y_shares[i],
            a_shares[i],
            b_shares[i],
            c_shares[i]
        ])

    iv = get_random_bytes(16)
    secret = pad((str(table[0][2]) + str(table[0][3]) + str(table[0][4])).encode(), 16)
    ct = encrypt(FLAG.encode(), secret, iv)
    pwn_print(conn, f"ciphertext: {ct.hex()}")

    shuffle(table)
    for r in table:
        pwn_print(conn, f"{r[0]}|{r[1]}|{r[2]}|{r[3]}|{r[4]}")

    secret_guess = pwn_input(conn, "Secret: ").encode()
    pwn_print(conn, decrypt(ct, secret_guess, iv).hex())

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()