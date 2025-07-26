from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def pwn_print(conn, message: str):
    conn.sendline(message.encode())

def pwn_input(conn, prompt: str) -> str:
    conn.send(prompt.encode())
    return conn.recvline().decode().strip()

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))