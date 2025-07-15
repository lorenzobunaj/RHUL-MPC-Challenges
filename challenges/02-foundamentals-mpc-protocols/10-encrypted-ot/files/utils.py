from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def pwn_print(conn, message: str):
    conn.sendline(message.encode())

def pwn_input(conn, prompt: str) -> str:
    pwn_print(conn, prompt)
    return conn.recvline().decode().strip()

def xor(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)