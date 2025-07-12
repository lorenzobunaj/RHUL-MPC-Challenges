from Crypto.Random import get_random_bytes
from random import randint
from private.bgw_gates import add_gate, cmul_gate, mul_gate

class Party:
    def __init__(self, p):
        self.p = p
        self.a = randint(1, p)

    def generate_shares(self, x, n):
        shares = []
        for i in range(1, n + 1):
            shares.append((self.a * i + x) % self.p)
        return shares
    
    def public_mul_gate(self, s1, s2, n):
        a = randint(1, self.p)
        d = (s1 * s2) % self.p

        shares = []
        for i in range(1, n+1):
            shares.append((a * i + d) % self.p)

        return shares

Party.add_gate = add_gate # # execute local computation for add gate
Party.cmul_gate = cmul_gate # execute local computation for constant multiplication gate
Party.mul_gate = mul_gate # execute local computation for multiplication gate
