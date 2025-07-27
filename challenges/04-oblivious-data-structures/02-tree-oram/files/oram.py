import random
import math

class TreeORAM:
    def __init__(self, N, Z):
        self.N = N # logical data blocks number
        self.Z = Z # buckets capacity
        self.height = math.ceil(math.log2(N))
        self.num_leaves = 2 ** self.height
        self.tree = [[] for _ in range(2 * self.num_leaves - 1)]
        self.position_map = {i: random.randint(0, self.num_leaves - 1) for i in range(N)}
        self.block_data = {i: None for i in range(N)}  # actual data

    def _get_path(self, leaf):
        path = []
        node = 0
        for h in range(self.height + 1):
            path.append(node)
            node = 2 * node + 1 + (leaf >> (self.height - h) & 1)

        return path

    def read(self, block_id):
        leaf = self.position_map[block_id]
        path = self._get_path(leaf)
        for node in path[::-1]:
            for i, (bid, _) in enumerate(self.tree[node]):
                if bid == block_id:
                    data = self.tree[node].pop(i)[1]
                    self._remap(block_id)
                    self._evict(block_id, data)
                    return data
                
        return self.block_data[block_id]  # fallback (e.g., after init)

    def write(self, block_id, data):
        self.block_data[block_id] = data
        self._remap(block_id)
        self._evict(block_id, data)

    def _remap(self, block_id):
        self.position_map[block_id] = random.randint(0, self.num_leaves - 1)

    def _evict(self, block_id, data):
        leaf = self.position_map[block_id]
        path = self._get_path(leaf)[::-1]
        for node in path:
            if len(self.tree[node]) < self.Z:
                self.tree[node].append((block_id, data))
                return

    def dump(self):
        return {
            'position_map': self.position_map,
            'tree': [[(bid, val) for (bid, val) in node] for node in self.tree]
        }

# Example usage
if __name__ == "__main__":
    oram = TreeORAM(N=8, Z=2)
    oram.write(3, "FLAG{circuit_oram_test}")
    print("Read block 3:", oram.read(3))

    import pprint
    pprint.pprint(oram.dump())