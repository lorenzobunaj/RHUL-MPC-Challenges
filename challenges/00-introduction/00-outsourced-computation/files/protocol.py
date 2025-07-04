from pwn import *
from utils import pwn_input, pwn_print
from client import Client
from server import Server

PORT = 5000
with open("flag.txt") as f:
    FLAG = int(f.read().strip().encode().hex(), 16)

def protocol(conn):
    client = Client(FLAG)
    server = Server()

    msg1 = client.int1()
    msg2 = server.int1(msg1)
    msg3 = client.int2(msg2)
    msg4 = server.int2(msg3)

    pwn_print(conn, str(msg4))

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    conn = server
    protocol(server)

if __name__ == "__main__":
    main()