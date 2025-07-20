from pwn import *
from utils import *

PORT = 1356
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    pwn_print(conn, "hello")

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()