import random
import math

class TreeORAM:
    def __init__(self, N, Z, secret):
        self.N = N  # number of data blocks
        self.Z = Z  # bucket capacity
        self.height = math.ceil(math.log2(N))  # tree height

        self.real_leaves = N # number of real leaves
        self.total_leaves = 2 ** self.height # number of leaves assuming the tree is complete
        self.total_nodes = 2 * self.total_leaves - 1

        self.tree = [[] for _ in range(self.total_nodes)]
        self.original_position_map = {i: random.randint(0, self.real_leaves - 1) for i in range(N)}
        self.position_map = dict(self.original_position_map)
        self.block_data = {i: None for i in range(N)}
        self.s = secret
        self.remap_cnt = 0

    def _get_leaf_node_index(self, leaf):
        return self.total_nodes - self.total_leaves + leaf

    def _get_path(self, leaf):
        path = []
        node = self._get_leaf_node_index(leaf)
        while node >= 0:
            path.append(node)
            if node == 0:
                break
            node = (node - 1) // 2
        return path[::-1]

    def read(self, block_id):
        leaf = self.position_map[block_id]
        path = self._get_path(leaf)
        for node in reversed(path):
            for i, (bid, _) in enumerate(self.tree[node]):
                if bid == block_id:
                    data = self.tree[node].pop(i)[1]
                    self.remap_cnt += 1
                    self._remap(block_id)
                    self._evict(block_id, data)
                    return data
        return self.block_data[block_id]

    def write(self, block_id, data):
        self.block_data[block_id] = data
        self._remap(block_id)
        self._evict(block_id, data)

    def _remap(self, block_id):
        self.position_map[block_id] = pow(self.original_position_map[block_id], pow(self.s, self.remap_cnt, self.real_leaves), self.real_leaves)

    def _evict(self, block_id, data):
        leaf = self.position_map[block_id]
        path = self._get_path(leaf)[::-1]
        for node in path:
            if len(self.tree[node]) < self.Z:
                self.tree[node].append((block_id, data))
                return

    def dump(self):
        return {
            'position_map': self.position_map
        }