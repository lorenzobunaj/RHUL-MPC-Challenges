import socket
import threading
from Crypto.Random import get_random_bytes
from utils import *

PORT = 1354
with open("flag.txt") as f:
    FLAG = f.read().strip()

def and_gg(Wa, Wb, Wc):
    la = [None] * 2
    pa = [None] * 2
    lb = [None] * 2
    pb = [None] * 2
    [(la[0], pa[0]), (la[1], pa[1])] = Wa
    [(lb[0], pb[0]), (lb[1], pb[1])] = Wb

    table = []
    for i in range(4):
        table.append(xor(H(la[i // 2], lb[i % 2]), Wc[pa[i // 2] ^ pb[i % 2]]))

    return table

def challenge(conn):
    delta = get_random_bytes(16)
    Wc = [get_random_bytes(16)]
    Wc.append(xor(Wc[0], delta))

    Wb = [(get_random_bytes(16), 0), (get_random_bytes(16), 1)]
    h = None
    for _ in range(2):
        Wa = [None] * 2
        nWa = [None] * 2
        
        nWa[0] = (bytes.fromhex(pwn_input(conn, "La0: "))[:16], 0)
        nWa[1] = (bytes.fromhex(pwn_input(conn, "La1: "))[:16], 1)

        if Wa[0] is None:
            Wa = list(nWa)
        else:
            for i in range(2):
                for j in range(2):
                    if Wa[i] == nWa[j]:
                        conn.close()
                        return
            Wa = list(nWa)

        table = and_gg(Wa, Wb, Wc)
        for tr in table:
            pwn_print(conn, tr.hex())

        if h is None:
            h = xor(table[-1], Wc[1])
        else:
            h = xor(h, xor(table[0], Wc[0]))
    
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), H(h, delta), iv)

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ct: {ct.hex()}")

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