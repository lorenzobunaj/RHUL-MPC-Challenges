from pwn import *
from Crypto.Random import get_random_bytes
from random import randint, shuffle
from utils import *
from oprf import OPRFServer
from cuckoo import CuckooHashTable

PORT = 1353
with open("flag.txt") as f:
    FLAG = f.read().strip()

def generate_secret(x, a, b, n):
    public = b""
    secret = b""

    for _ in range(8):
        x = (a*x + b) % n
        public += bytes([x % 256, x // 256])

    for _ in range(16):
        secret += bytes([x % 256])
    
    return public, secret

def menu(conn):
    pwn_print(conn, "What do you want to do?")
    pwn_print(conn, "(1) Access the OPRF Oracle")
    pwn_print(conn, "(2) Access the Cuckoo Hash Table")
    pwn_print(conn, "(3) Print the stash")
    pwn_print(conn, "(4) Decrypt the flag")

    choice = int(pwn_input(conn, "Your choice: "))

    if choice not in range(1, 5):
        choice = 1

    return choice

def challenge(conn):
    oprf_key = get_random_bytes(16)
    oprf = OPRFServer(oprf_key)
    cuckoo_table = CuckooHashTable(40)
    
    x = randint(1, pow(2, 20))
    a = randint(1, pow(2, 20))
    b = randint(1, pow(2, 20))
    n = randint(1, pow(256, 2))

    iv = get_random_bytes(16)
    public, secret = generate_secret(x, a, b, n)
    ct = encrypt(FLAG.encode(), secret, iv)

    items = [public[2*i:2*(i+1)].hex() + str(i) for i in range(8)]

    s0 = list(items)
    s1 = list(items)

    for _ in range(24):
        s0.append(get_random_bytes(2).hex() + str(randint(0, 7)))
        s1.append(get_random_bytes(2).hex() + str(randint(0, 7)))

    shuffle(s0)
    shuffle(s1)
    
    pwn_print(conn, "S1:")
    for i in range(40):
        cuckoo_table.insert(oprf.evaluate(s0[i]))
        pwn_print(conn, s1[i])

    choice = 0
    while choice != 4:
        choice = menu(conn)
        
        if choice == 1:
            x = pwn_input(conn, "Your input: ")
            pwn_print(conn, oprf.evaluate(x).hex())
        elif choice == 2:
            y = bytes.fromhex(pwn_input(conn, "Your input: "))
            f = cuckoo_table.search(y)
            pwn_print(conn, ("" if f else "not ") + "found")
        elif choice == 3:
            stash = cuckoo_table.get_stash()
            pwn_print(conn, str(len(stash)))
            for b in stash:
                pwn_print(conn, b.hex())
        elif choice == 4:
            secret = bytes.fromhex(pwn_input(conn, "Secret: "))
            pt = decrypt(ct, secret, iv)

            pwn_print(conn, f"Flag: {pt.hex()}")

    conn.close()

def main():
    server = listen(PORT)
    print(f"Server listening on port {PORT}")
    challenge(server)

if __name__ == "__main__":
    main()