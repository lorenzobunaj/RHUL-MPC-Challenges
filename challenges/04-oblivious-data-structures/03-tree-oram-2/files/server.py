import socket
import threading
from Crypto.Random import get_random_bytes
from utils import *
from oram import TreeORAM

PORT = 1362
with open("flag.txt") as f:
    FLAG = f.read().strip()

N = 65537
Z = 65537
def challenge(conn):
    secret = get_random_bytes(16)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ciphertext: {ct.hex()}")

    mem = TreeORAM(N, Z, int.from_bytes(secret[:2]))

    for i in range(N):
        mem.write(i, get_random_bytes(8))

    reset_cnt = 0
    choice = 0
    while choice in [0, 1, 2]:
        pwn_print(conn, "What do you want to do?")
        pwn_print(conn, "(0) Read")
        pwn_print(conn, "(1) Dump ORAM")
        pwn_print(conn, "(2) Reset")
        conn.sendall(b"You choice: ")
        choice = int(pwn_recvline(conn))

        if choice == 0:
            conn.sendall(b"Block id: ")
            bid = int(pwn_recvline(conn))
            conn.sendall(mem.read(bid).hex().encode() + b"\n")
        elif choice == 1:
            out = mem.dump()
            pwn_print(conn, "Position map:")
            for key, val in out['position_map'].items():
                conn.sendall(f"({key} : {val}) ".encode())
            conn.sendall(b"\n")
        elif choice == 2:
            if reset_cnt == 7:
                return
            reset_cnt += 1

            mem = TreeORAM(N, Z, int.from_bytes(secret[reset_cnt*2:(reset_cnt+1)*2]))

            for i in range(N):
                mem.write(i, get_random_bytes(8))

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