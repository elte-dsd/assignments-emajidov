import random
import pandas as pd
import numpy as np


class CountMinSketch():
    def __init__(self, n, unique_elements):
        '''@:param n is used to define number of unique elements in the array
           @:param unique_elements is used to create hash table for eachy element (this can be eliminated also, just
           added for flexibility'''
        self.unique_elements = unique_elements
        self.n = n
        self.table = np.zeros([n, n])  # freuquency table for counting the elements in the stream
        self.hash_table = pd.DataFrame(
            np.zeros([n, n]))  # the hash table that we want for the hash functions for elements

    def hashes(self):
        ''' this method creates random numbers for hashing as much as unique elements '''
        hashes = []
        for i in range(self.n):
            hashes.append(random.randint(0, self.n - 1))
        return hashes

    def create_hash_table(self):
        '''this method is used to create hash table for each elements randomly, the hash of each element is
        the corresponding column'''
        dict = {}
        for i in self.unique_elements:
            dict[i] = self.hashes()
        self.hash_table = pd.DataFrame(dict)
        return self.hash_table

    def increment(self, key):
        '''@:param key - is the element in the stream
        this function is used for mapping the hash values on the table from hash table '''
        indexes = self.hash_table[key]
        for i in range(26):
            self.table[i, indexes[i]] = self.table[i, indexes[i]] + 1

    def estimate(self, key):
        '''@:param key -  is the element in the stream that we want the frequency
        this counnt number of element in the frequency table'''
        indexes = self.hash_table[key]
        values = []
        for i in range(26):
            values.append(self.table[i, indexes[i]])
        res = min(values)
        return res
