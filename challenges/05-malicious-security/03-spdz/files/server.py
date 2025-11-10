import socket
import threading
from Crypto.Random import random
from utils import pwn_input, pwn_print
from party1 import Party1
from party2 import Party2

P = (1 << 127) - 1

PORT = 1367
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    S = Party1()
    P2 = Party2()

    d1, d2 = S.generate_delta()
    x1, x2 = random.randint(0, P - 1), P2.send_x()
    t1, t2 = S.generate_t(x1 + x2)

    P2.receive_params(d2, t2)
    P2.receive_x(x1)
    c2 = P2.send_commitment()

    pwn_print(conn, f"d1: {d1}")
    pwn_print(conn, f"x1: {x1}")
    pwn_print(conn, f"x: {(x1 + x2) % P}")
    pwn_print(conn, f"t1: {t1}")

    pwn_print(conn, f"c2: {c2}")

    c1 = int(pwn_input(conn, "Commitment c1: "))

    P2.receive_commitment(c1)

    # check the commitment
    comm = c1 - (d1 * (x1 + x2) % P) + (x1 % P)
    if comm % P == 0 and c1 % P != c1:
        conn.close()
        return

    delta_x = P2.collude(t1)

    k = int(pwn_input(conn, "Your message: "))

    if ((k + delta_x) % P) == (((d1 + d2) * (x1 + x2)) % P) and k % P != 0:
        pwn_print(conn, FLAG)

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