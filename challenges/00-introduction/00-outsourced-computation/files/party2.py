from random import randint

def utility(x):
    return (x == 0 or (x and (x - 1) == 0))

class Party2:
    def __init__(self):
        self.secret = randint(pow(2, 40), pow(2, 80))

    def int1(self, in1):
        out1 = in1 ^ utility(self.secret)

        return out1
    
    def int2(self, in2):
        out2 = in2 ^ utility(self.secret >> 1)

        return out2