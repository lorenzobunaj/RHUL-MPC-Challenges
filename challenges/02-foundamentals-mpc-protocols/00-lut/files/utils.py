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

def encrypt(pt, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(pt, AES.block_size))

    return ct
    