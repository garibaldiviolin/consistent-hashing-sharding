import hashlib
from collections import defaultdict
from bisect import bisect_right, bisect
from utils.storage_node import servers


def hash_fn(key, total_slots):
    sha = hashlib.sha256()
    sha.update(bytes(key, 'utf-8'))
    return int(sha.hexdigest(), 16) % total_slots


class ConsistentHash:
    def __init__(self):
        self._keys = []  # indexes taken on the ring
        self.nodes = []  # nodes in the ring
        self.total_slots = 3000

    def add_node(self, node):
        if len(self._keys) == self.total_slots:
            raise Exception('Full')

        key = hash_fn(node.host, self.total_slots)
        index = bisect(self._keys, key)

        if index > 0 and self._keys[index - 1] == key:
            raise Exception('Collision Detected')

        self.nodes.insert(index, node)
        self._keys.insert(index, key)
        return key

    def upload(self, file_name):
        key = hash_fn(file_name, self.total_slots)
        index = bisect_right(self._keys, key)
        if index > len(self.nodes) - 1:
            index = 0

        host = self.nodes[index].host
        name = self.nodes[index].name

        print(f'Uploading: {file_name} To: {name} Host: {host}')
        return index


ch = ConsistentHash()


# Add the available servers to the pool
for node in servers:
    ch.add_node(node)

indices = defaultdict(int)

# Upload File
for i in range(1_000_000):
    index = ch.upload(f'newPic_{i}.txt')
    indices[index] += 1


indices_sorted = list(indices.keys())
indices_sorted.sort()
print("\nResumo:")
for index in indices_sorted:
    print(index, "=", indices[index])
