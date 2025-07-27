from pwn import *
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from random import shuffle
from utils import *
from okvs import OKVS

PORT = 1360
with open("flag.txt") as f:
    FLAG = f.read().strip()

OKVS_SIZE = 10
def challenge(conn):
    secret = get_random_bytes(8)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), pad(secret, 16), iv)

    secret = H(secret[:8].hex().encode())

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ct: {ct.hex()}")

    values = []
    okvs = OKVS(OKVS_SIZE)
    for i in range(OKVS_SIZE):
        key = bytes([i] * 16)
        val = get_random_bytes(16)
        values.append(val)
        okvs.encode(val, key)

    shuffle(values)
    okvs.encode(get_random_bytes(16), secret)
    enc_values = okvs.get_okvs()

    for i in range(OKVS_SIZE):
        pwn_print(conn, f"v[{i}] = {values[i].hex()}")
        pwn_print(conn, f"okvs[{i}] = {enc_values[i].hex()}") 

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)
    server.close()

if __name__ == "__main__":
    main()