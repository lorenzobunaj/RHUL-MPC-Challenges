import socket
import threading
from Crypto.Random import get_random_bytes
from random import randint
from utils import *

PORT = 1355
with open("flag.txt") as f:
    FLAG = f.read().strip()

def generator_gate(conn, a, c, delta, va, r):
    pwn_print(conn, f"a: {a[va].hex()}")

    p = bytes([va * r * d for d in delta])
    pwn_print(conn, f"G's output: {xor(H(a[va]), xor(c[0], p)).hex()}")

def evaluator_gate(conn, a, b, c, va, vb, r):
    pwn_print(conn, f"va: {va}")
    pwn_print(conn, f"b: {b[vb].hex()}")

    pwn_print(conn, f"G's output: {xor(H(a[1]), xor(c[0], b[r])).hex()}")

def half_gates_protocol(conn, va, vb):
    r = randint(0,1)
    delta = bitsToBytes([randint(0,1) for _ in range(63)] + [1])

    a = [get_random_bytes(8)]
    a.append(xor(a[0], delta))
    b = [bitsToBytes([randint(0,1) for _ in range(63)] + [r])]
    b.append(xor(b[0], delta))
    c = [H(a[0])]
    c.append(xor(c[0], delta))

    pwn_print(conn, "####################")
    generator_gate(conn, a, c, delta, va, r)
    evaluator_gate(conn, a, b, c, va, vb, r)

def challenge(conn):
    va = bytesToBits(get_random_bytes(8))
    vb = bytesToBits(get_random_bytes(8))
    vc = [vai & vbi for vai, vbi in zip(va, vb)]

    secret = random_oracle(bitsToBytes(vc))
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ct: {ct.hex()}")

    vc_guess = []
    for i in range(len(vc)):
        vc_guess.append(half_gates_protocol(conn, va[i], vb[i]))

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