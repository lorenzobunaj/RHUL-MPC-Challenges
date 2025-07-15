from pwn import *
from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES
from random import randint
from utils import *
from functionalities import ot_functionality
from party1 import Party1

PORT = 1350
with open("flag.txt") as f:
    FLAG = f.read().strip()

def update_shares(w1, w2):
    nw1, nw2 = b"", b""

    for i in range(len(w1)):
        t = w1[i] ^ w2[i]
        r = t ^ randint(0, 255)
        nw1 += bytes([t ^ r])
        nw2 += bytes([r])

    return nw1, nw2

def challenge(conn):
    m = [get_random_bytes(16), get_random_bytes(16)]

    secret = bytes([m[i % 2][i] for i in range(16)])
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    party1 = Party1(m[0], m[1], 16, 16)

    r_choice = pwn_input(conn, "Choice bits: ")
    r_choice = [int(b) % 2 for b in r_choice]

    Trows = []
    Urows = []
    for i in range(16):
        tr = bytes.fromhex(pwn_input(conn, f"T's {i}-th row (hex): "))[:16]
        ur = bytes.fromhex(pwn_input(conn, f"U's {i}-th row (hex): "))[:16]
        key = bytes.fromhex(pwn_input(conn, f"T's {i}-th row encryption key (hex): "))[:8]

        r = get_random_bytes(16)
        tr = xor(tr, r)
        
        cipher = DES.new(key, DES.MODE_ECB)
        tr = cipher.encrypt(tr)

        if tr[0] < 50:
            tr = cipher.decrypt(tr)
        else:
            tr = cipher.encrypt(tr)

        tr = xor(tr, r)

        Trows.append(tr)
        Urows.append(ur)

    Tcols = [bytes([
            Trows[j][i] 
            for j in range(16)
        ]) for i in range(16)
    ]
    Ucols = [bytes([
            Urows[j][i] 
            for j in range(16)
        ]) for i in range(16)
    ]

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