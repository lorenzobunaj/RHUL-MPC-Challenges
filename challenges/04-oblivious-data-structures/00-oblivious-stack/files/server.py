import socket
import threading
from random import randint
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
        conn.sendall(b"You choice: ")
        choice = int(pwn_recvline(conn))

        if choice == 1:
            conn.sendall(b"Your input: \n")
            val = int(pwn_recvline(conn))
            stack.condPush(val)
            limit += 1
        elif choice == 2:
            val = stack.pop()
            conn.sendall(f"Your output: {val}\n".encode())
            pops += 1

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