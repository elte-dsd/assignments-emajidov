import hashlib


class BloomFilter():
    def __init__(self, size):
        '''@:param size - means the size of the array that we need for checking element
         beforehand we can estimate how much element we will have and based on this we can
         define the size of the array for the bits'''
        self.n = size
        self.bitmap = [0] * self.n * 10  # in order to have a big range for not having collusion

    def hashes(self, key):
        '''this function creates a hash array for an element
         the number of hashes depends on the size of the bit array, if we have big bit array we will have more hashes
         in order to have ig variety'''
        res = []
        for _ in range(self.n):
            key = int(hashlib.sha3_512(str(key).encode("utf-8")).hexdigest(), 32) % (self.n * 10)
            res.append(key)
        return res

    def add(self, key):
        '''this method adds the element to the bit array, it updates the elements on the bit array according to the
        hash array'''
        indexes = self.hashes(key)
        for i in indexes:
            self.bitmap[i] = 1

    def consists(self, key):
        '''this method checks if the element exists, for this if one of the element according to the hash
        is 0 it means that element does not exist in the array'''
        indexes = self.hashes(key)
        for i in indexes:
            if self.bitmap[i] == 0:
                return False
            break
        return True
