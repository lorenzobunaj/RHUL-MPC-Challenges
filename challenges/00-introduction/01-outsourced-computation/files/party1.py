from random import randint

class Party1:
    def __init__(self, s):
        self.secret = s
        self.r = randint(8, 15)

    def int1(self):
        out1 = self.secret
        for _ in range(self.r):
            out1 *= 3

        return out1
    
    def int2(self, in2):
        mask = []
        for i in range(self.r):
            mask.append(1 if i % 2 == 0 else 0)
        
        k = int("".join(str(b) for b in mask), 2)
        out2 = in2 ^ k

        return out2