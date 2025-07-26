from utils import random_oracle, xor

class OKVS:
    def __init__(self, N):
        self.cap = N
        self.array = [bytes([0] * 16)] * N

    def encode(self, val, key):
        pos1, pos2, pos3 = random_oracle(val, self.cap)

        self.array[pos1] = xor(self.array[pos1], key)
        self.array[pos2] = xor(self.array[pos2], key)
        self.array[pos3] = xor(self.array[pos3], key)

    def get_okvs(self):
        return self.array