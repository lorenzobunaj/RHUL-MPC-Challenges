from Crypto.Random import get_random_bytes

class Party1:
    def __init__(self, secret):
        self.secret = secret
        self.g = 2
        self.p = pow(2, 127) - 1
        self.x = int.from_bytes(get_random_bytes(16), byteorder='little')

    def parameters(self):
        y = pow(self.g, self.x, self.p)

        return [self.g, self.p, y]
    
    def verify(self, r, s):
        if s.bit_length() < 128:
            return "verification failed"
            
        if pow(self.g, s, self.p) == (pow(self.g, self.x, self.p) * r) % self.p:
            return self.secret
        
        return "verification failed"
