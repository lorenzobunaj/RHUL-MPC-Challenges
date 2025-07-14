from pwn import *
from Crypto.Random import get_random_bytes
from utils import *

PORT = 1347
with open("flag.txt") as f:
    FLAG = f.read().strip()

assert len(FLAG) == 46

def challenge(conn):
    msg = (int.from_bytes(get_random_bytes(16), "big"), int.from_bytes(FLAG.encode(), "big"))

    n1 = int(pwn_input(conn, "n1: "))
    k1 = int(pwn_input(conn, "k1: "))
    n2 = int(pwn_input(conn, "n1: "))
    k2 = int(pwn_input(conn, "k2: "))

    if n1.bit_length() < 512 or n2.bit_length() < 512 or k1.bit_length() < 9 or k2.bit_length() < 9 or k1 == k2:
        conn.close()
        return

    c1 = pow(msg[0], k1, n1)
    c2 = pow(msg[1], k2, n2)

    pwn_print(conn, f"c1: {c1}")
    pwn_print(conn, f"c2: {c2}")

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()