from pwn import *
import pickle
from phe import paillier
from Crypto.Random import get_random_bytes
from utils import *

PORT = 1357
with open("flag.txt") as f:
    FLAG = f.read().strip()

def valid_key(public_key):
    try:
        if not isinstance(public_key, paillier.PaillierPublicKey):
            return False
        
        n = public_key.n
        if not isinstance(n, int) or n <= 1:
            return False
        
        _ = public_key.encrypt(1)
        
        return True

    except Exception as e:
        return False
    
def gmw_and(conn, a, b):
    table = []
    for _ in range(4):
        tr = pwn_input(conn, "Table row: ")
        table.append(tr)

    return table[2*a + b]
    
def gmw_full_adder(conn, a, b, cin):
    s = a ^ b ^ cin
    cout = gmw_and(conn, a, b)
    cout ^= gmw_and(conn, a, cin)
    cout ^= gmw_and(conn, b, cin)

    return s, cout

def challenge(conn):
    pk_bytes = bytes.fromhex(pwn_input(conn, "Public key: "))
    pk = pickle.loads(pk_bytes)

    if not valid_key(pk):
        return
    
    secret = get_random_bytes(16)
    iv = get_random_bytes(16)
    ct = encrypt(FLAG.encode(), secret, iv)

    pwn_print(conn, f"iv: {iv.hex()}")
    pwn_print(conn, f"ct: {ct.hex()}")

    x = int.from_bytes(secret, "big")
    r = int.from_bytes(get_random_bytes(16), "big")

    x_enc = pk.encrypt(x)
    r_enc = pk.encrypt(r)
    sum_enc = x_enc + r_enc
    sum_enc_hex = pickle.dumps(sum_enc).hex()
    pwn_print(conn, f"Sum of encryptions: {sum_enc_hex}")

    sx = bytes.fromhex(pwn_input(conn, f"Player's share: "))

    ry = get_random_bytes(16)
    sy = xor(int.to_bytes(r, 16, "big"), ry)
    if len(ry) < len(sx):
        ry = ry.rjust(len(sx), b'\x00')
    sy = xor(int.to_bytes(r, len(sx), "big"), ry)
    
    pwn_print(conn, f"Server's share: {sy.hex()}")

    sx_bits = bytesToBits(sx)
    ry_bits = bytesToBits(ry)

    res = []
    cin = 0
    for i in range(16 * 8 - 1, -1, -1):
        s, cin = gmw_full_adder(conn, sx_bits[i], ry_bits[i], cin)
        res.insert(0, s)

    pwn_print(conn, f"Final share: {bitsToBytes(res).hex()}")

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)
    server.close()

if __name__ == "__main__":
    main()