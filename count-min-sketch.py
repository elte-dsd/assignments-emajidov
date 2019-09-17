import random
import string
import pandas as pd
import numpy as np

letters = string.ascii_uppercase
list = []

table = np.zeros([26, 26])

for i in range(100):
    list.append(random.choice(letters))


def hashes(value, n):
    hashes = []
    for i in range(26):
        hashes.append(random.randint(0, 25))
    return hashes


def create_hash_table():
    dict = {}
    for i in letters:
        dict[i] = hashes(i, 26)
    df = pd.DataFrame(dict)
    return df


h = create_hash_table()


def increment(key):
    indexes = h[key]
    for i in range(26):
        table[i, indexes[i]] = table[i, indexes[i]] + 1


def estimate(key):
    indexes = h[key]
    values = []
    for i in range(26):
        values.append(table[i, indexes[i]])
    res = min(values)

    print(key + "- " + str(res))

for i in list:
    increment(i)
for i in letters:
    estimate(i)

dict = {} # for checking counts
for i in letters:
    dict[i] = 0

for i in list:
    dict[i] = dict[i]+1