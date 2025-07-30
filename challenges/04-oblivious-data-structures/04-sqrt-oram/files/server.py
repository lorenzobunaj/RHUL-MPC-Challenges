import socket
import threading
import random
import math
from utils import *
from oram import SqrtORAM

PORT = 1363
with open("flag.txt") as f:
    FLAG = f.read().strip()

LEN = 64
def challenge(conn):
    flag_content = FLAG[5:-1]
    flag_bytes = bytes.fromhex(flag_content)

    mem = SqrtORAM(LEN)

    assert len(flag_content) == 16

    data = list(flag_bytes)
    for _ in range(LEN - len(flag_bytes)):
        data.append(random.randint(0, 255))

    mem.initialize(data)

    position_map = None
    stash_len = 0
    choice = 0
    while choice in [0, 1]:
        if stash_len == 0:
            position_map = mem.get_position_map()
            inverse_position_map = {v : k for k, v in position_map.items()}

        pwn_print(conn, "What do you want to do?")
        pwn_print(conn, "(0) Read flag")
        pwn_print(conn, "(1) Read block data")
        conn.sendall(b"You choice: ")
        choice = int(pwn_recvline(conn))

        if choice == 0:
            conn.sendall(f"Which flag character do you want to read (0/1/.../{len(flag_bytes)})? ".encode())
            fc = int(pwn_recvline(conn))
            if fc not in range(len(flag_content)):
                continue

            data, res = mem.read(inverse_position_map[fc])
            pwn_print(conn, "Character read!")

            if res == 1:
                stash_len += 1

        elif choice == 1:
            conn.sendall(f"Which block do you want to read (0/1/.../{LEN-1})? ".encode())
            bid = int(pwn_recvline(conn))
            if bid not in range(LEN):
                continue

            data, res = mem.read(bid)
            pwn_print(conn, "Block read!")
            pwn_print(conn, f"data: {data}")

            if res == 1:
                stash_len += 1

        if stash_len == math.ceil(math.sqrt(LEN)):
            stash_len = 0

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