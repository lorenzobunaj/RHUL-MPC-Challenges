from Crypto.Random import get_random_bytes
from random import randint
from private.lagrange_interpolation import lagrange_interpolation

class Party:
    def __init__(self, p):
        self.p = p

    def generate_shares(self, secret, n):
        a = randint(1, self.p)
        shares = []
        for i in range(1, n + 1):
            shares.append((a * i + secret) % self.p)
        return shares
    
    def public_mul_gate(self, s1, s2, n):
        q = s1 * s2
        return self.generate_shares(q, n)

Party.lagrange_interpolation = lagrange_interpolation
