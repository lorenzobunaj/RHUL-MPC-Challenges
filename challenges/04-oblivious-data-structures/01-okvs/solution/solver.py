from pwn import *
import random
import itertools
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

HOST = "localhost" # change to the actual host
PORT = 1360 # change to the actual port

OKVS_SIZE = 10

def random_oracle(val, l):
    r = random.Random()
    r.seed(val)
    indices = r.sample(range(l), 3)

    return tuple(indices)

def xor(a, b):
    return bytes([ai ^ bi for ai, bi in zip(a, b)])

def Hinverse(secret : bytes):
    val = [None] * 4
    val[1] = xor(secret[:4], secret[4:8])
    val[2] = xor(secret[4:8], secret[8:12])
    val[3] = xor(secret[8:12], secret[12:16])
    val[0] = xor(secret[:4], val[3])

    return val[0] + val[1] + val[2] + val[3]

def decrypt(ct, secret, iv):
    cipher = AES.new(secret, AES.MODE_CBC, iv)

    return cipher.decrypt(ct)

def main():
    conn = remote(HOST, PORT)

    conn.recvuntil(b"iv: ")
    iv = bytes.fromhex(conn.recvline().strip().decode())
    conn.recvuntil(b"ct: ")
    ct = bytes.fromhex(conn.recvline().strip().decode())

    values = [None] * OKVS_SIZE
    enc_values = [None] * OKVS_SIZE

    for i in range(OKVS_SIZE):
        conn.recvuntil(f"v[{i}] = ".encode())
        values[i] = bytes.fromhex(conn.recvline().strip().decode())
        conn.recvuntil(f"okvs[{i}] = ".encode())
        enc_values[i] = bytes.fromhex(conn.recvline().strip().decode())

    secret = None
    values_perms = list(itertools.permutations(values))
    limit = len(values_perms)
    for it, vp in enumerate(values_perms):
        tmp_enc_values = list(enc_values)
        if it % 10000 == 0:
            print(f"max {limit - it} rounds remaining")
        for i in range(OKVS_SIZE):
            pos1, pos2, pos3 = random_oracle(vp[i], OKVS_SIZE)

            key = bytes([i] * 16)
            tmp_enc_values[pos1] = xor(tmp_enc_values[pos1], key)
            tmp_enc_values[pos2] = xor(tmp_enc_values[pos2], key)
            tmp_enc_values[pos3] = xor(tmp_enc_values[pos3], key)

        cnt = 0
        for ev in tmp_enc_values:
            if ev == b"\x00" * 16:
                cnt += 1
        
        if cnt >= OKVS_SIZE - 3:
            for ev in tmp_enc_values:
                if ev != b"\x00" * 16:
                    secret = ev
                    break
            break

    secret = pad(bytes.fromhex(Hinverse(secret).decode()), 16)

    print(decrypt(ct, secret, iv))

    conn.close()

if __name__ == "__main__":
    main()