import socket
import threading
import random
import time
from utils import pwn_input, pwn_print
from party1 import Party1

PORT = 1364
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    party1 = Party1(FLAG)

    abort = 0
    for i in range(len(FLAG)):
        test = pwn_input(conn, "Enter 20 inputs (a1|a2|...|a20): ")
        test = list(map(int, test.split("|")))

        weighted_array = [1] * 10 + [0] * 10
        random.shuffle(weighted_array)
        cut_test = []
        for (j, b) in enumerate(weighted_array):
            if b == 1:
                cut_test.append(test[j])

        for a in cut_test:
            conn.sendall(b".")
            party1.evaluates(i, a)
            if party1.isAbort():
                conn.sendall(b"Aborted.")
                abort = 1
                party1.reset()
                time.sleep(1)
                break

        conn.sendall(b"\n")

        if abort:
            break

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