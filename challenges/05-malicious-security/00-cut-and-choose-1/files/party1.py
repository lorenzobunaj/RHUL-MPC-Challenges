class Party1:
    def __init__(self, s):
        self.s = s
        self.status = 0

    def isAbort(self):
        return self.status
    
    def evaluates(self, i, a):
        res = ord(self.s[i]) + a
        res %= 256

        if res != ord(self.s[i]) + a:
            self.status = 1
        else:
            print(ord(self.s[i]) + a)

    def reset(self):
        self.status = 0