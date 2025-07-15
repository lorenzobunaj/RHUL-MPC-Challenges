from pwn import *
from Crypto.Random import get_random_bytes
from utils import *
from functionalities import ot_functionality
from party1 import Party1

PORT = 1349
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    m = [get_random_bytes(16), get_random_bytes(16)]

    secret = bytes([m[i % 2][i] for i in range(16)])
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    party1 = Party1(m[0], m[1], 16, 16)

    r_choice = pwn_input(conn, "Choice bits: ")
    r_choice = [int(b) % 2 for b in r_choice]

    Tcols = []
    Ucols = []
    for i in range(16):
        tc = bytes.fromhex(pwn_input(conn, f"T's {i}-th col (hex): "))[:16]
        uc = bytes.fromhex(pwn_input(conn, f"U's {i}-th col (hex): "))[:16]

        Tcols.append(tc)
        Ucols.append(uc)

    s = party1.receiver_role()

    Qcols = []
    for i in range(len(s)):
        Qcols.append(ot_functionality([Tcols[i], Ucols[i]], s[i]))
    Sout = party1.sender_role(Qcols)

    for h1, h2 in Sout:
        pwn_print(conn, f"({h1}, {h2})")

    secret = bytes.fromhex(pwn_input(conn, "Secret (in hex): "))
    pt = decrypt(ct, secret, iv)

    pwn_print(conn, f"Your output: {pt.hex()}")

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()