from pwn import *
from sympy import prime, factorint
from sympy.ntheory.modular import crt
from mt19937predictor import MT19937Predictor

N = 624
HOST = "localhost" # change to the actual host
PORT = 1356 # change to the actual port

def is_square_free(n):
    factors = factorint(abs(n), use_trial=True, limit=100)
    return all(p <= prime(16) and exp == 1 for p, exp in factors.items())

def calculate_seed(seed_moduli):
    kmax = 1
    for i in range(16):
        kmax *= prime(i+1)
    primes = [prime(i+1) for i in range(16)]

    seeds_recovered = []

    for s in seed_moduli:
        residues = []
        moduli = []
        for i in range(20):
            residues.append(s[i])
            moduli.append(51 - i)

        x, step = crt(moduli, residues)

        while x < kmax:
            if is_square_free(x):
                seeds_recovered.append(x)
                
            x += step
    
    bits = [1 if seeds_recovered[0] % p == 0  else 0 for p in primes] + [1 if seeds_recovered[1] % p == 0 else 0 for p in primes]
    seed = int(''.join(map(str, bits)), 2)

    return seed

def new_seed(conn):
    moduli = []
    for i in range(32):
        conn.sendline(f"{i+1}".encode())

    conn.recvuntil(b"seq[31]: ")
    moduli.append([])
    for _ in range(20):
        # print(list(map(lambda el: None if el == "-" else int(el), conn.recvline().strip().decode().split(" "))))
        moduli[-1].append(list(map(lambda el: None if el == "-" else int(el), conn.recvline().strip().decode().split(" "))).index(1))
    moduli.append([])
    for _ in range(20):
        # print(list(map(lambda el: None if el == "-" else int(el), conn.recvline().strip().decode().split(" "))))
        moduli[-1].append(list(map(lambda el: None if el == "-" else int(el), conn.recvline().strip().decode().split(" "))).index(1))
    
    seed = calculate_seed(moduli[-2:])

    return seed

def main():
    conn = remote(HOST, PORT)

    predictor = MT19937Predictor()

    for i in range(N):
        seed = new_seed(conn)
        predictor.setrandbits(seed, 32)
        if i < N-1:
            conn.sendline(b"1")

    conn.sendline(str(predictor.getrandbits(32)).encode())

    conn.recvuntil(b"Flag: ")
    print(conn.recvline().strip().decode())
    
    conn.close()

if __name__ == "__main__":
    main()