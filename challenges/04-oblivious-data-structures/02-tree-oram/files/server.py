from pwn import *
from Crypto.Random import get_random_bytes
from random import randint
from utils import *
from oram import TreeORAM

PORT = 1361
with open("flag.txt") as f:
    FLAG = f.read().strip()

N = 65537
Z = 65537
def challenge(conn):
    secret = get_random_bytes(16)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ciphertext: {ct.hex()}")

    mem = TreeORAM(N, Z, int.from_bytes(secret))

    for i in range(N):
        mem.write(i, get_random_bytes(8))

    choice = 0
    while choice in [0, 1]:
        pwn_print(conn, "What do you want to do?")
        pwn_print(conn, "(0) Read")
        pwn_print(conn, "(1) Dump ORAM")
        conn.send(b"You choice: ")
        choice = int(conn.recvline().strip().decode())

        if choice == 0:
            conn.send(b"Block id: ")
            bid = int(conn.recvline().strip().decode())
            conn.sendline(mem.read(bid).hex().encode())
        elif choice == 1:
            out = mem.dump()
            pwn_print(conn, "Position map:")
            for key, val in out['position_map'].items():
                conn.send(f"({key} : {val}) ".encode())
            conn.sendline()
            pwn_print(conn, "Tree:")
            for i, bucket in enumerate(out['tree']):
                conn.send(f"{i} | ")
                for block in bucket:
                    conn.send(f"{block} ".encode())
                conn.sendline()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)
    server.close()

if __name__ == "__main__":
    main()