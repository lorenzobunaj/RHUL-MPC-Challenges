import socket
import threading
from utils import pwn_input, pwn_print
from party1 import Party1

PORT = 1341
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    party1 = Party1(FLAG)

    [g, p, y] = party1.parameters()

    pwn_print(conn, str(g))
    pwn_print(conn, str(p))
    pwn_print(conn, str(y))

    try:
        r = int(pwn_input(conn, "r: "))
        s = int(pwn_input(conn, "s: "))
    except:
        pwn_print("r, s not valid")
        conn.close()
        return 
    
    pwn_print(conn, party1.verify(r, s))

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