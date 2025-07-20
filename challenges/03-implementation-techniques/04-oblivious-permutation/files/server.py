from pwn import *
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
    guess_k = None
    while stop == 0:
        pwn_print(conn, "New sequence: ")
        sequence = []
        for i in range(32):
            conn.send(f"seq[{i}]: ".encode())
            num = int(conn.recvline().decode().strip())
            sequence.append(num)
        for _ in range(19):
            sequence.append(None)

        bits = random.getrandbits(32)
        bits = list(map(int, bin(bits)[2:].zfill(32)))

        if guess_k is not None:
            if guess_k == k:
                pwn_print(conn, f"Flag: {FLAG}")

        k = 1
        for i in range(16):
            if bits[i] == 1:
                k *= prime(i+1)

        new_sequence = list(sequence)
        for _ in range(20):
            tmp_sequence = permute(new_sequence, k)
            for num in tmp_sequence:
                conn.send(f'{"-" if num is None else num}'.encode())
            conn.send(b"\n")
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
                conn.send(f'{"-" if num is None else num}'.encode())
            conn.send(b"\n")
            if None in new_sequence:
                new_sequence.remove(None)
        
        guess_k = int(pwn_input(conn, "Your seed guess: "))

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()