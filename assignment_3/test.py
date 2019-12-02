from assignment_3.DynamicWeightedMajority import DynamicWeightedMajority
from assignment_3.Stagger import Stagger
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
import numpy as np
stagger = Stagger(120)
x_train, y_train = stagger.generateData()



dwm = DynamicWeightedMajority(0.5, 0.01, 120)

size, accs = dwm.dwm(x_train, y_train)
# preds = dwm.predict(x_test)

nb = GaussianNB()
nb.fit(x_train,y_train)

# preds_gs = nb.predict(x_test)
#
# acc1 = accuracy_score(y_test,preds)
# acc2 = accuracy_score(y_test,preds_gs)

# print(acc1)
# print(acc2)
res= []
for i, sample in enumerate(x_train):
    nb.partial_fit([sample], [y_train[i]])
    predictions = nb.predict(x_train)
    res.append(accuracy_score(y_train,predictions))

# plt.figure(1, figsize=(16,1))
plt.subplot(121)
plt.title("Acurracies over single run")
plt.plot(np.arange(len(res)), res, label="DWM-NB")
plt.legend()
plt.subplot(121)
plt.title("Acurracies over single run")
plt.plot(np.arange(len(accs)), accs, label="DWM-NB")
plt.show()