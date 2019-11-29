import copy
import numpy as np
from skmultiflow.bayes import NaiveBayes
from skmultiflow.data.waveform_generator import WaveformGenerator
from sklearn.datasets import load_iris

base_classifier = NaiveBayes()

epochs = 30
experts = {}
num_experts = 4


def createExpert():
    return copy.copy(base_classifier)


def removeExpert(experts, theta):
    return [exp for exp in experts if experts[exp] >= theta]


def normalizeWeights(max_weight):
    exps = experts.keys()

    for exp in exps:
        experts[exp] *= 1 / max_weight

    return experts


def getExpertPredictions(experts, X):
    experts = experts.keys()
    return [exp.predidct(X) for exp in experts]


# def train(exp, X, y, classes, beta, theta, period):
#     for i in range(len(X)):
#         dwm(X[i:i + 1, :], y[i:i + 1], classes, beta, theta, period)


def dwm(X, y, classes, beta, theta, period):
    predictions = np.zeros(classes)
    max_weight = 0
    weakest_expert_weight = 1
    weakest_expert_index = 0
    exps = list(experts.keys())

    for i, exp in enumerate(exps):
        y_hat = exp.predict(X)
        if np.any(y_hat != y) and epochs % period == 0:
            experts[exp] *= beta

        predictions[y_hat] += experts[exp]
        max_weight = max(max_weight, experts[exp])

        if experts[exp] < weakest_expert_weight:
            weakest_expert_index = i
            weakest_expert_weight = experts[exp]
    y_hat = np.array([np.argmax(predictions)])

    if epochs % period == 0:
        normalizeWeights(max_weight)
        removeExpert(experts, theta)

        if np.any(y_hat != y):
            if len(experts) == num_experts:
                experts.pop(exps[weakest_expert_index])
            experts[createExpert()] = 1
        for exp in experts.keys():
            exp.fit(X, y, classes=classes)


def predict(X):
    predictions = np.array([np.array(exp.predict(X)) * experts[exp] for exp in experts.keys()])
    sum_weights = sum(experts[exp] for exp in experts.keys())
    aggregate = np.sum(predictions / sum_weights, axis=0)
    return (aggregate + 0.5).astype(int)


stream = WaveformGenerator(random_state=774, has_noise=True)

for i in range(4):
    experts[createExpert()] = 1

data = load_iris()
X = data.data
y = data.target

classes = 3
period = 10
beta = 0.1
theta = 0.7
period = 100
classes = 3

train = X[1:120, :]
test = X[120:150, :]

dwm(train, y, 3, 0.1, 0.7, 10)
