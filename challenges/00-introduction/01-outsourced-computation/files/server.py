import socket
import threading
from utils import *
from party1 import Party1
from party2 import Party2

PORT = 1337
with open("flag.txt") as f:
    FLAG = int(f.read().strip().encode().hex(), 16)

def challenge(conn):
    party1 = Party1(FLAG)
    party2 = Party2()

    msg1 = party1.int1()
    msg2 = party2.int1(msg1)
    msg3 = party1.int2(msg2)
    msg4 = party2.int2(msg3)

    pwn_print(conn, str(msg4))

    conn.close()

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