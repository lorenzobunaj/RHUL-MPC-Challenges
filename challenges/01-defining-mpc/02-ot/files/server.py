import socket
import threading
from utils import pwn_input, pwn_print
from party1 import Party1

PORT = 1340
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    party1 = Party1(FLAG)

    messages = party1.generateMessages()

    choice_bits = []
    for _ in range(len(messages)):
        bit = int(pwn_input(conn, "Enter the next choice bit: "))
        if bit not in [0,1]:
            return
        choice_bits.append(bit)

    for (i, b) in enumerate(choice_bits):
        pwn_print(conn, str(messages[i][b]))

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