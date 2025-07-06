from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from pwn import *
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

def protocol(conn):
    p = int(pwn_input(conn, "Enter the modulo (as integer): "))
    x = int.from_bytes(key, 'little')
    g = 2
    if p.bit_length() < 256:
        return -1
    
    y = pow(g, x, p)

    pwn_print(conn, str(y))

def decryptFlag(conn):
    try:
        guess_int = int(pwn_input(conn, "Enter the key (as integer): "))
        guess_key = guess_int.to_bytes(16, 'little')
        cipher = AES.new(guess_key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)

        pwn_print(conn, pt.decode())
    except Exception:
        pwn_print(conn, "Decryption failed.")

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    
    for _ in range(2):
        choice = menu(server)
        if choice == 1:
            protocol(server)
        elif choice == 2:
            decryptFlag(server)

    server.close()

if __name__ == "__main__":
    main()