import hashlib
import random

class CuckooHashTable:
    def __init__(self, size, num_hashes=3, max_kicks=500):
        self.size = size
        self.num_hashes = num_hashes
        self.max_kicks = max_kicks
        self.table = [None] * size
        self.stash = []

    def _hash(self, y: bytes, i: int) -> int:
        return int.from_bytes(hashlib.sha256(str(i).encode() + y).digest(), 'big') % self.size

    def _get_candidate_bins(self, y: bytes):
        return [self._hash(y, i) for i in range(self.num_hashes)]

    def insert(self, y: bytes) -> bool:
        for _ in range(self.max_kicks):
            bins = self._get_candidate_bins(y)
            for b in bins:
                if self.table[b] is None:
                    self.table[b] = y
                    return True
                
            kick_bin = random.choice(bins)
            self.table[kick_bin], y = y, self.table[kick_bin]

        self.stash.append(y)
        return False
    
    def search(self, y: bytes) -> bool:
        return y in self.table
    
    def get_stash(self):
        return self.stash
