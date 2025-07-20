from sympy import prime, factorint
from sympy.ntheory.modular import crt
import random
from mt19937predictor import MT19937Predictor

N = 624

def generate_seeds():
    seeds = []
    seeds_moduli = []
    for _ in range(N):
        bits = random.getrandbits(32)
        bits = list(map(int, bin(bits)[2:].zfill(32)))

        k = 1
        for i in range(16):
            if bits[i] == 1:
                k *= prime(i+1)
        seeds.append(k)
        seeds_moduli.append([])
        for i in range(20):
            seeds_moduli[-1].append(k % (32 + i))
        
        k = 1
        for i in range(16):
            if bits[16+i] == 1:
                k *= prime(i+1)
        seeds.append(k)
        seeds_moduli.append([])
        for i in range(20):
            seeds_moduli[-1].append(k % (32 + i))
    
    return seeds_moduli

def is_square_free(n):
    factors = factorint(abs(n), use_trial=True, limit=100)
    return all(p <= prime(16) and exp == 1 for p, exp in factors.items())

def main():
    seeds_moduli = generate_seeds()

    kmax = 1
    for i in range(16):
        kmax *= prime(i+1)
    
    seeds_recovered = []
    for s in seeds_moduli:
        residues, moduli = [], []

        for i in range(20):
            residues.append(s[i])
            moduli.append(32 + i)

        x, step = crt(moduli, residues)

        while x < kmax:
            if is_square_free(x):
                seeds_recovered.append(x)
                break
            
            x += step

    primes = [prime(i+1) for i in range(16)]
    views = []
    for i in range(N):
        bits = [1 if seeds_recovered[2*i] % p == 0  else 0 for p in primes] + [1 if seeds_recovered[2*i + 1] % p == 0 else 0 for p in primes]
        views.append(int(''.join(map(str, bits)), 2))

    predictor = MT19937Predictor()
    for v in views:
        predictor.setrandbits(v, 32)

    print(predictor.getrandbits(32) == random.getrandbits(32))


if __name__ == "__main__":
    main()