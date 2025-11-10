from Crypto.Random import random

class Party2:
    def __init__(self):
        self.p = (1 << 127) - 1
        self.xi = random.randint(0, self.p - 1)

    def receive_params(self, d, t):
        self.di = d
        self.ti = t

    def send_x(self):
        return self.xi
    
    def receive_x(self, xj):
        self.x = (self.xi + xj) % self.p

    def send_commitment(self):
        c = (self.di * self.x - self.ti) % self.p
        return c
    
    def receive_commitment(self, c):
        self.cj = c
    
    def collude(self, tj):
        
        delta_x = self.cj + tj + self.di * self.x
        return delta_x
