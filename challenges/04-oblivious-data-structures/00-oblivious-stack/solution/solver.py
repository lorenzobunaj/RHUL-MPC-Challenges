from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = "localhost" # change to the actual host
PORT = 1359 # change to the actual port

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ct: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    secret_bytes = []

    for _ in range(32):
        conn.recvuntil(b"choice: ")
        conn.sendline(b"1")
        conn.sendline(b"41")
    
    for i in range(48):
        conn.recvuntil(b"choice: ")
        conn.sendline(b"2")
        conn.recvuntil(b"output: ")
        if i > 31:
            secret_bytes.insert(0, int(conn.recvline().strip().decode()))

    secret = bytes(secret_bytes)

    conn.close()

    flag_guess = decrypt(ct, secret[::-1], iv)
    if flag_guess[:4] == b"RHUL":
        print(unpad(flag_guess, AES.block_size))
        return

    secret_postfix = secret[:15]
    for i in range(256):
        secret_fixed = bytes([i]) + secret_postfix
        flag_guess = decrypt(ct, secret_fixed[::-1], iv)
        if flag_guess[:4] == b"RHUL":
            print(unpad(flag_guess, AES.block_size))
            return
    
    secret_prefix = secret[1:]
    for i in range(256):
        secret_fixed = secret_prefix + bytes([i])
        flag_guess = decrypt(ct, secret_fixed[::-1], iv)
        if flag_guess[:4] == b"RHUL":
            print(unpad(flag_guess, AES.block_size))
            return

if __name__ == "__main__":
    main()