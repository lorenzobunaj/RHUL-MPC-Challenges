from pwn import *
from Crypto.Random import get_random_bytes
from oblivious_stack import ObliviousStack
from utils import *

PORT = 1359
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    secret = get_random_bytes(16)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ct: {ct.hex()}")

    stack = ObliviousStack(32)

    for _ in range(100):
        stack.condPush(randint(0, 255))
    for s in secret:
        stack.condPush(s)
    stack.emptyStack()

    pops = 0
    limit = 16
    while pops < min(limit, 48):
        pwn_print(conn, "What do you want to do?")
        pwn_print(conn, "(1) Push")
        pwn_print(conn, "(2) Pop")
        conn.send(b"You choice: ")
        choice = int(conn.recvline().decode())

        if choice == 1:
            conn.sendline(b"Your input: ")
            val = int(conn.recvline().strip().decode())
            stack.condPush(val)
            limit += 1
        elif choice == 2:
            val = stack.pop()
            conn.sendline(f"Your output: {val}".encode())
            pops += 1

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)
    server.close()

if __name__ == "__main__":
    main()