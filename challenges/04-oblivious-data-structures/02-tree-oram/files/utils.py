from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad

def pwn_print(conn, message):
    conn.sendall((message + "\n").encode())

def pwn_input(conn, prompt):
    pwn_print(conn, prompt)
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            break
        data += chunk
    return data.strip().decode()

def pwn_recvline(conn):
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            break
        data += chunk
    return data.strip().decode()

def encrypt(pt, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.encrypt(pad(pt, AES.block_size))