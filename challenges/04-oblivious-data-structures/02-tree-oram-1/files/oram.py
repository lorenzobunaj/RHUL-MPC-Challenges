import random
import math
from Crypto.Random import get_random_bytes

class TreeORAM:
    def __init__(self, N, Z, secret):
        self.N = N  # number of logical data blocks
        self.Z = Z  # bucket capacity
        self.height = math.ceil(math.log2(N))  # height of complete binary tree

        self.total_leaves = 2 ** self.height
        self.total_nodes = 2 * self.total_leaves - 1

        self.tree = [[] for _ in range(self.total_nodes)]  # full binary tree
        self.position_map = {i: random.randint(0, self.total_leaves - 1) for i in range(N)}
        self.block_data = {i: None for i in range(N)}

        self.s = secret

    def _get_leaf_index(self, leaf):
        return self.total_nodes - self.total_leaves + leaf

    def _get_path(self, leaf):
        path = []
        node = self._get_leaf_index(leaf)
        while node >= 0:
            path.append(node)
            if node == 0:
                break
            node = (node - 1) // 2
        return path[::-1]

    def read(self, block_id):
        return self.block_data[block_id]

    def write(self, block_id, data):
        self.block_data[block_id] = data
        self._remap(block_id)
        self._evict(block_id, data)

    def _remap(self, block_id):
        self.position_map[block_id] = random.randint(0, self.total_leaves - 1)

    def _evict(self, block_id, data):
        leaf = self.position_map[block_id]
        path = self._get_path(leaf)[::-1]
        for node in path:
            if len(self.tree[node]) < self.Z:
                self.tree[node].append((block_id, data))
                return

    def dump(self):
        block_id = random.randint(0, self.total_leaves - 1)
        self.write(block_id, get_random_bytes(len(self.s) - 1) + bytes([self.s[block_id % len(self.s)]]))

        return {
            'position_map': self.position_map
        }