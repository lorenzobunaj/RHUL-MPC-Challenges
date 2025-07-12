from random import randint

def add_gate(self, s1, s2):
    return (s1 + s2) % self.p
    
def cmul_gate(self, s1, k):
    return (s1 * k) % self.p

def mul_gate(self, r):
    s = sum(r) % self.p
    return s