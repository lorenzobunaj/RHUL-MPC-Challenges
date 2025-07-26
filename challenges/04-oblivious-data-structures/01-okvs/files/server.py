from pwn import *
from utils import *
from okvs import OKVS
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from random import shuffle

PORT = 1360
with open("flag.txt") as f:
    FLAG = f.read().strip()

def challenge(conn):
    secret = pad(get_random_bytes(8), 16)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    secret = H(secret[:8].hex().encode())

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ct: {ct.hex()}")

    values = []
    okvs = OKVS(16)
    for i in range(16):
        key = bytes([i] * 16)
        val = get_random_bytes(16)
        values.append(val)
        okvs.encode(val, key)

    shuffle(values)
    okvs.encode(get_random_bytes(16), secret)
    enc_values = okvs.get_okvs()

    for i in range(len(values)):
        pwn_print(conn, f"v[{i}] = {values[i].hex()}")
        pwn_print(conn, f"okvs[{i}] = {enc_values[i].hex()}") 

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)
    server.close()

if __name__ == "__main__":
    main()