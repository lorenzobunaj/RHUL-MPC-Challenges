import socket
import threading
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from utils import pwn_input, pwn_print

PORT = 1339
with open("flag.txt") as f:
    FLAG = f.read().strip().encode()

key = get_random_bytes(16)
iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG, AES.block_size))

def menu(conn):
    pwn_print(conn, "What do you want to do?")
    pwn_print(conn, "(1) Interact with the other party")
    pwn_print(conn, "(2) Decrypt the flag")
    choice = int(pwn_input(conn, "Your choice: "))

    return choice

def challenge(conn):
    p = int(pwn_input(conn, "Enter the modulo (as integer): "))
    x = int.from_bytes(key, 'little')
    g = 2
    if p.bit_length() < 256:
        return -1
    
    y = pow(g, x, p)

    pwn_print(conn, str(y))

    try:
        guess_int = int(pwn_input(conn, "Enter the key (as integer): "))
        guess_key = guess_int.to_bytes(16, 'little')
        cipher = AES.new(guess_key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)

        pwn_print(conn, pt.decode())
    except Exception:
        pwn_print(conn, "Decryption failed.")

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