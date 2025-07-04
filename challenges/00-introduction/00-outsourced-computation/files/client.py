from random import randint

class Client:
    def __init__(self, s):
        self.secret = s

    def int1(self):
        out1 = self.secret
        for _ in range(randint(8, 15)):
            out1 *= 3

        return out1
    
    def int2(self, in2):
        k = pow(2, 12)
        out2 = in2 ^ k

        return out2