import string
import random
from assignment_1.count_min_sketch import CountMinSketch


letters = string.ascii_uppercase
list = []
for i in range(1000):
    list.append(random.choice(letters))

alg = CountMinSketch(26, letters)
alg.create_hash_table()

# the following two loops is created for testing the algorithm's accuracy
dict  = {}
for i in letters:
    dict[i] = 0
for i in list:
    dict[i] = dict[i] + 1
hash_table = alg.create_hash_table()

for i in list:
    alg.increment(i)
for i in letters:
    print(i + " - Estimated: " + str(alg.estimate(i)) + " | Actual: " + str(dict[i]))

