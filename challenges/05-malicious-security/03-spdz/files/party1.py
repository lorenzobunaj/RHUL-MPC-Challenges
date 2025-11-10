from Crypto.Random import random

class Party1:
    def __init__(self):
        self.p = (1 << 127) - 1

    def generate_delta(self):
        self.delta = random.randint(0, self.p - 1)

        d1 = random.randint(0, self.p - 1)
        d2 = (self.delta - d1) % self.p
        return (d1, d2)
    
    def generate_t(self, x):
        t = (self.delta * x) % self.p

        t1 = random.randint(0, self.p - 1)
        t2 = (t - t1) % self.p
        return (t1, t2)
    
