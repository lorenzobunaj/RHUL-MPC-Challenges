import socket
import threading
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Util.Padding import unpad
from random import randint
from utils import *

PORT = 1342
with open("flag.txt") as f:
    FLAG = f.read().strip()

assert len(FLAG) == 40

keys = [get_random_bytes(16) for _ in range(64)]
iv = get_random_bytes(16)

access = [0 for _ in range(64)]

def decrypt(ct, key, x, y):
    if access[8 * x + y] == 1:
        raise ValueError
    access[8 * x + y] = 1

    new_key = key
    moves = [-2, -1, 1, 2]
    for m1 in moves:
        for m2 in moves:
            if abs(m1) != abs(m2) and x+m1 in range(8) and y+m2 in range(8) and keys[8 * (x+m1) + y+m2] == key:
                new_key = keys[8 * x + y]

    cipher = AES.new(new_key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    return (pt, new_key)

shares = []
for i in range(4):
    secret = int.from_bytes(FLAG[10*i:10*(i+1)].encode(), "little")
    shares.append(Shamir.split(16, 16, secret))

lut = [[-1 for _ in range(8)] for _ in range(8)]
for i in range(2):
    for j in range(2):
        offset = [4*i, 4*j]
        for idx, share in shares[2*i + j]:
            qindex = [(idx-1) // 4, (idx-1) % 4]
            lut[offset[0] + qindex[0]][offset[1] + qindex[1]] = encrypt(share, keys[8 * (offset[0] + qindex[0]) + offset[1] + qindex[1]], iv)

def menu(conn):
    pwn_print(conn, "Which entry do you want to decrypt (insert an invalid index to exit)?")
    x = int(pwn_input(conn, "x: "))
    y = int(pwn_input(conn, "y: "))
    key = bytes.fromhex(pwn_input(conn, "key: "))

    return (x, y, key)

def challenge(conn):
    public_x, public_y = randint(0, 7), randint(0, 7)
    pwn_print(conn, f"x = {public_x}")
    pwn_print(conn, f"y = {public_y}")
    pwn_print(conn, f"key = {keys[8 * public_x + public_y].hex()}")

    x, y = 0, 0
    while x in range(8) and y in range(8):
        (x, y, key) = menu(conn)
        if x not in range(8) or y not in range(8):
            break

        try:
            (pt, new_key) = decrypt(lut[x][y], key, x, y)
            pwn_print(conn, f"share: {pt.hex()}")
            pwn_print(conn, f"key: {new_key.hex()}")
        except ValueError:
            pwn_print(conn, "You can't decrypt the same entry twice.")

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