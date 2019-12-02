import numpy as np
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.exceptions import NotFittedError
from sklearn.metrics import accuracy_score

class DynamicWeightedMajority:
    def __init__(self, beta, theta, period):
        self.experts = np.array([])
        self.weights = np.array([])
        self.beta = beta
        self.theta = theta
        self.period = period

    def createExpert(self):
        expert = GaussianNB()
        self.experts = np.append(self.experts, expert)
        self.weights = np.append(self.weights, 1)

    def removeExpert(self):
        indexes = self.weights > self.theta
        self.experts = self.experts[indexes]
        self.weights = self.weights[indexes]

    def normalizeWeights(self, max_weight):
        for weight in self.weights:
            weight *= 1 / max_weight

    def getExpertPrediction(self, expert, x):
        try:
            return expert.predict([x])
        except NotFittedError as ex:
            return np.random.choice([0, 1])

    def fit(self, X, y):
        train_size = len(X)
        x_test = X[int(train_size - train_size/6):train_size]
        X = X[0:train_size - int(train_size / 6)]
        y_test = y[int(train_size- train_size/6):train_size]
        y = y[0:train_size - int(train_size / 6)]
        m = 1
        self.createExpert()
        num_classes = len(np.unique(y))
        predictions = np.zeros((num_classes,))
        max_weight = 0
        acc = []
        nb_acc = []
        sizes =[]
        nb = GaussianNB()
        for i, sample in enumerate(X):
            for j, exp in enumerate(self.experts):
                y_hat = self.getExpertPrediction(exp,sample)
                y_hat = int(y_hat)
                if (y_hat != y[i]) and (i % self.period == 0):
                    self.weights[j] *= self.beta
                    print(str(self.experts[j]) + "th Expert Weight: " + str(self.weights[j]))


                predictions[y_hat] += self.weights[j]
                max_weight = max(max_weight, self.weights[j])
            y_hat = np.array([np.argmax(predictions)])

            if i % self.period == 0:

                self.normalizeWeights(max_weight)
                self.removeExpert()
                if y_hat != y[i]:
                    m = m + 1
                    self.createExpert()

            nb.partial_fit([sample], [y[i]], np.unique(y))
            nb_pred = nb.predict(x_test)
            nb_acc.append(accuracy_score(y_test,nb_pred))
            for exp in self.experts:
                exp.partial_fit([sample], [y[i]], np.unique(y))
            sizes.append(len(self.experts))
            acc.append(accuracy_score(self.predict(x_test), y_test))
        return sizes, acc, nb_acc

    def predict(self, X):
        try:
            preds = np.array([np.array(self.experts[j].predict(X)) * self.weights[j]
                              for j in range(len(self.experts))])
            sum_weights = sum(self.weights[j] for j in range(len(self.weights)))
            aggregate = np.sum(preds / sum_weights, axis=0)
            return (aggregate + 0.5).astype(int)
        except NotFittedError as ex:
            return np.random.choice([0, 1])