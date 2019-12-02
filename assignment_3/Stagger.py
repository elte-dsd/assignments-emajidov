import numpy as np
import random
class Stagger:
    def __init__(self, size):
        self.size = size


    def generateData(self):
        data = np.zeros([self.size, 9])
        for i in range(self.size):
            data[i, 0 + np.random.choice([0,1,2])] = 1
            data[i, 3 + np.random.choice([0,1,2])] = 1
            data[i, 6 + np.random.choice([0,1,2])] = 1

            target = np.ndarray([self.size, 1])

        slice = int(self.size / 3)
        target[:slice, 0] = (data[:slice, 2] == 1) * (data[:slice, 6] == 1)
        target[slice:2 * slice, 0] = (data[slice:2 * slice, 0] == 1) + (data[slice:2 * slice, 4] == 1)
        target[2 * slice:self.size, 0] = (data[2 * slice:self.size, 7] == 1)
        return data, target