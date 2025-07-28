import socket
import threading
from utils import *
import random
from sympy import prime

PORT = 1356
with open("flag.txt") as f:
    FLAG = f.read().strip()

def permute(sequence, k):
    l = len(sequence)
    new_sequence = [None] * l

    for i in range(l):
        new_sequence[(i + k) % l] = sequence[i]

    return new_sequence

def challenge(conn):
    stop = 0
    next_seed_guess = None
    while stop == 0:
        seed = random.getrandbits(32)
        bits = list(map(int, bin(seed)[2:].zfill(32)))

        if next_seed_guess is not None:
            if next_seed_guess == seed:
                pwn_print(conn, f"Flag: {FLAG}")
            
        pwn_print(conn, "New sequence: ")
        sequence = []
        for i in range(32):
            conn.sendall(f"seq[{i}]: ".encode())
            num = int(pwn_recvline(conn))
            sequence.append(num)
        for _ in range(19):
            sequence.append(None)

        k = 1
        for i in range(16):
            if bits[i] == 1:
                k *= prime(i+1)

        new_sequence = list(sequence)
        for _ in range(20):
            tmp_sequence = permute(new_sequence, k)
            for num in tmp_sequence:
                conn.sendall(f'{"-" if num is None else num} '.encode())
            conn.sendall(b"\n")
            if None in new_sequence:
                new_sequence.remove(None)

        k = 1
        for i in range(16):
            if bits[16+i] == 1:
                k *= prime(i+1)

        new_sequence = list(sequence)
        for _ in range(20):
            tmp_sequence = permute(new_sequence, k)
            for num in tmp_sequence:
                conn.sendall(f'{"-" if num is None else num} '.encode())
            conn.sendall(b"\n")
            if None in new_sequence:
                new_sequence.remove(None)
        
        next_seed_guess = int(pwn_input(conn, "Your next seed guess: "))

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