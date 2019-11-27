import numpy as np
from sklearn.naive_bayes import GaussianNB
from skmultiflow.data import WaveformGenerator
from skmultiflow.trees import HoeffdingTree
from skmultiflow.evaluation import EvaluatePrequential

stream  = WaveformGenerator()
stream.prepare_for_use()


def create_expert(x, y):
    clf = GaussianNB()
    clf.fit(x, y)
    return clf


def normalize(arr):
    mean = np.mean(arr)
    for i in len(arr):
        arr[i] = arr[i] / mean
    return arr


def remove_experts(experts, weights, theta):
    idx = []
    for i in len(weights):
        if (weights[i] < theta):
            idx.append(i)
    weights = np.delete(weights, idx)
    for i in idx:
        del experts[i]
    return experts, weights


def dwm(x, y, c, beta, theta, p):
    expert1 = create_expert(x, y)
    expert2 = create_expert(x, y)
    expert3 = create_expert(x, y)
    expert4 = create_expert(x, y)

    m = 4
    experts = [expert1, expert2, expert3, expert4]
    w = np.ones((m,), dtype=np.float16)
    labels = np.unique(y)
    n = len(x)  # number of samples
    sigmas = {}
    for i in labels:
        sigmas[y] = 0
    for i in range(n):

        for j in range(m):
            l = experts[j].predict(x)
            if (l != y[i] and i % p == 0):
                w[j] = beta * w[j]
            sigmas[y[i]] = sigmas[y[i]] + w[j]
        L = sigmas.max()
        if (i % p == 0):
            w = normalize(w)
            experts, w = remove_experts(experts, w, theta)
        if (L != y[i]):
            m = m + 1
            expert = create_expert(x, y)
            experts.append(expert)
            w = np.append(w, [1])
        for j in range(m):
            print("done")
    # train experts
