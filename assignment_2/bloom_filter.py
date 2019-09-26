import hashlib


class BloomFilter():
    def __init__(self, size):
        self.n = size
        self.bitmap = [0] * self.n * 100

    def hashes(self, key):
        res = []
        for _ in range(self.n):
            key = int(hashlib.sha3_512(str(key).encode("utf-8")).hexdigest(), 32) % (self.n * 10)
            res.append(key)
        return res

    def add(self, key):
        indexes = self.hashes(key)
        for i in indexes:
            self.bitmap[i] = 1

    def consists(self, key):
        indexes = self.hashes(key)
        for i in indexes:
            if self.bitmap[i] == 0:
                return False
            break
        return True



b = BloomFilter(100)

