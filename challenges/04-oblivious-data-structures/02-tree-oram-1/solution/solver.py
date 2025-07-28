from pwn import *
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import re

HOST = "localhost" # change to the actual host
PORT = 1361 # change to the actual port

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

def read_position_map(conn):
    conn.recvuntil(b"Position map:\n")
    pm_pairs = re.findall(r'\((\d+)\s*:\s*(\d+)\)', conn.recvline().strip().decode())
    position_map = {int(k): int(v) for k, v in pm_pairs}

    return position_map

N = 2 ** 15
Z = 2 ** 15
SECRET_LEN = 16
def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ciphertext: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    secret_recovered = [None] * SECRET_LEN
    changed_bid_recovered = []

    conn.sendline(b"1")
    position_map1 = read_position_map(conn)

    while len(changed_bid_recovered) < SECRET_LEN:
        changed_bid = None

        conn.sendline(b"1")
        position_map2 = read_position_map(conn)

        for key in position_map1.keys():
            if position_map1[key] != position_map2[key]:
                changed_bid = key
                break
        
        if changed_bid is not None and (changed_bid % SECRET_LEN) not in changed_bid_recovered:
            conn.sendline(b"0")
            conn.sendline(str(changed_bid).encode())
            conn.recvuntil(b"Block id: ")

            changed_data = bytes.fromhex(conn.recvline().strip().decode())
            secret_recovered[changed_bid % SECRET_LEN] = changed_data[-1]
            changed_bid_recovered.append(changed_bid % SECRET_LEN)

        position_map1 = position_map2.copy()

    secret = bytes(secret_recovered)

    print(decrypt(ct, secret, iv))

    conn.close()

if __name__ == "__main__":
    main()