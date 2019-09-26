from assignment_2.bloom_filter import BloomFilter

b = BloomFilter(100)  # initialize the algorithm

b.add("emajidov")  # add he element to the list

print(b.consists("emajidov"))  # check the availability of the element
print(b.consists("emajidov1"))
print(b.consists("emajido")) #check the availability of different versions

print(b.consists("emajido"))