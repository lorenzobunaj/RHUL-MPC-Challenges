from pwn import *
from phe import paillier
import pickle
from Crypto.Random import get_random_bytes

HOST = "localhost" # change to the actual host
PORT = 1357 # change to the actual port

def main():
    conn = remote(HOST, PORT)

    public_key, private_key = paillier.generate_paillier_keypair()
    pk_hex = pickle.dumps(public_key).hex()
    conn.sendline(pk_hex.encode())

    conn.recvuntil(b"Sum of encryptions: ")
    sum_enc_bytes = bytes.fromhex(conn.recvline().strip().decode())
    sum_enc = pickle.loads(sum_enc_bytes)
    secret_sum = private_key.decrypt(sum_enc)

    rx = get_random_bytes(16)
    sx = xor(int.to_bytes(secret_sum, 17, "big"), rx)

    conn.sendline(sx.hex().encode())

    conn.recvuntil(b"Server's share: ")
    sy = bytes.fromhex(conn.recvline().strip().decode())

    print(rx)
    print(sy)

if __name__ == "__main__":
    main()