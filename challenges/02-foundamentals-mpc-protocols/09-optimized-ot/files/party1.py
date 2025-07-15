from random import randint
from utils import xor
from functionalities import random_oracle

class Party1:
    def __init__(self, m1, m2, m, k):
        self.m1 = m1
        self.m2 = m2
        self.m = m
        self.k = k

    def receiver_role(self):
        self.s = [randint(0,1) for _ in range(self.m)]
        return self.s

    def sender_role(self, Qcols):
        Qrows = [bytes([
                Qcols[j][i] 
                for j in range(self.k)
            ]) for i in range(self.m)
        ]
        sb = bytes(self.s)

        return [(
            int.from_bytes(xor(random_oracle(Qrows[i], 1), bytes([self.m1[i]])), "big"), 
            int.from_bytes(xor(random_oracle(xor(Qrows[i], sb), 1), bytes([self.m2[i]])), "big")
        ) for i in range(self.m)]