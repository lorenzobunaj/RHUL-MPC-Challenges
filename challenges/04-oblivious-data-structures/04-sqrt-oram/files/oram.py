import math
import random
from time import sleep

TIME_DELAY = 0.2
class SqrtORAM:
    def __init__(self, N):
        self.cap = N
        self.data = [None] * N
        self.stash = []
        self.stash_limit = math.ceil(math.sqrt(N))

        indices = [i for i in range(N)]
        random.shuffle(indices)
        self.position_map = {i : indices[i] for i in range(N)}

    def _update_perm(self):
        indices = [i for i in range(self.cap)]
        random.shuffle(indices)
        self.position_map = {i : indices[i] for i in range(self.cap)}

    def initialize(self, data):
        if len(data) != self.cap:
            return
        
        for idx, d in enumerate(data):
            self.data[idx] = d

    def get_position_map(self):
        return self.position_map.copy()

    def read(self, block_id):
        for id, data in self.stash:
            if id == block_id:
                return data, 0
            sleep(TIME_DELAY)

        data = self.data[self.position_map[block_id]]
        self.stash.append((block_id, data))

        if len(self.stash) == self.stash_limit:
            self.stash = []
            self._update_perm()
    
        return data, 1
        
