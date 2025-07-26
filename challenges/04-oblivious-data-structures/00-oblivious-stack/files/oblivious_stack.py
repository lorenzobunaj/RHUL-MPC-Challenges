from random import randint

class ObliviousStack:
    def __init__(self, N):
        self.capacity = N
        self.size = 0
        self.stash_size = 0
        self.values = [(-1, -1)] * (2 * self.capacity)

    def emptyStack(self):
        self.values[:self.capacity] = [(-1, -1)] * self.capacity
        self.size = 0

    def condPush(self, val):
        if self.size == self.capacity:
            self.stashPush(val)
            return

        p = randint(0,1)
        self.values[self.size] = (val, p)
        self.size += 1

        if p == 1:
            self.stashPush(val)

    def pop(self):
        val, _ = self.values[self.size - 1]
        self.values[self.size - 1] = (-1,-1)
        self.size -= 1

        return val
    
    def stashPush(self, val):
        curr_el = (val, 1)
        i = 0
        while i < self.capacity and self.values[self.capacity + i] != (-1,-1):
            tmp_el  = self.values[self.capacity + i]
            self.values[self.capacity + i] = curr_el
            curr_el = tmp_el
            i += 1
            
        if i < self.capacity:
            self.values[self.capacity + i] = curr_el