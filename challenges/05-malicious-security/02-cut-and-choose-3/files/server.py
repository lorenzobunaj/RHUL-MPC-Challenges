import socket
import threading
import secrets
from utils import pwn_input_inline, pwn_print, bytes_to_bits
from setup import setup
from private.parameters import S

CIRCUITS_NUM = 96

PORT = 1366
with open("flag.txt") as f:
    FLAG = f.read().strip()

assert len(S) == 16

def challenge(conn):
    s = bytes.fromhex(S)

    circuits, commitments = setup(CIRCUITS_NUM)

    for i in range(CIRCUITS_NUM):
        pwn_print(conn, f"C[{i}]: {commitments[i]}")

    choosen_circuits_str = pwn_input_inline(conn, "Which circuits do you want to open? ")
    choosen_circuits_bits = [int(c) for c in choosen_circuits_str]
    
    for (i, c) in enumerate(circuits):
        if choosen_circuits_bits[i] == 1:
            pwn_print(conn, f"Seed[{i}]: {c["seed"]}")

    x = pwn_input_inline(conn, f"Player's input (hex): ")
    x = bytes.fromhex(x)

    res = bytes_to_bits(bytes(a ^ b for a, b in zip(x, s)))

    j = 0
    for (i, c) in enumerate(circuits):
        if j == 8 * len(s):
            break
        
        if choosen_circuits_bits[i] == 0:
            pwn_print(conn, f"Label[{i}]: {c["wires"][f"L{res[j]}"]}")
            pwn_print(conn, f"preL0[{i}]: {c["wires"]["preL0"]}")
            j += 1

    y = pwn_input_inline(conn, f"Player's 2nd input (hex): ")
    y = bytes.fromhex(y)

    res = bytes_to_bits(bytes(a ^ b for a, b in zip(y, s)))
    if res == [0] * 64:
        pwn_print(conn, f"flag: {FLAG}")
    
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