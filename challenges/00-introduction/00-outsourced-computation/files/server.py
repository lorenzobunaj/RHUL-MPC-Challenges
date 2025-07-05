from pwn import *
from utils import pwn_input, pwn_print
from party1 import Party1
from party2 import Party2

PORT = 1337
with open("flag.txt") as f:
    FLAG = int(f.read().strip().encode().hex(), 16)

def protocol(conn):
    party1 = Party1(FLAG)
    party2 = Party2()

    msg1 = party1.int1()
    msg2 = party2.int1(msg1)
    msg3 = party1.int2(msg2)
    msg4 = party2.int2(msg3)

    pwn_print(conn, str(msg4))

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    protocol(server)

if __name__ == "__main__":
    main()