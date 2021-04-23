import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import neighbors, tree
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.tree import DecisionTreeClassifier

parts = 10

path = "dataprocessing/data/ml/"
tail = "({parts}p).mlt".format(parts=parts)
dotpath = "dataprocessing/data/ml/tree_lcrtv({parts}p).dot".format(parts=parts)

lineData = pd.read_pickle(path + "line" + tail)
logData = pd.read_pickle(path + "log" + tail)
rectData = pd.read_pickle(path + "rect" + tail)
triangleData = pd.read_pickle(path + "triangle" + tail)
vData = pd.read_pickle(path + "v" + tail)

data = lineData.copy()
data = data.append(logData)
data = data.append(rectData)
data = data.append(triangleData)
#data = data.append(vData)

#data.info()
#print(data)
#sns.heatmap(data.corr(), xticklabels=data.columns.values, yticklabels=data.columns.values)
#data.hist()


keys = []
for i in range(parts):
    keys.append("mode_Kx" + str(i))
    keys.append("mode_Ky" + str(i))
    keys.append("mode_Kz" + str(i))
    keys.append("mean_Kx" + str(i))
    keys.append("mean_Ky" + str(i))
    keys.append("mean_Kz" + str(i))
    keys.append("max_abs_Kx" + str(i))
    keys.append("max_abs_Ky" + str(i))
    keys.append("max_abs_Kz" + str(i))

data = data.drop(keys, axis=1)
data.info()
print(data)
#sns.heatmap(data.corr(), xticklabels=data.columns.values, yticklabels=data.columns.values)
#data.hist()

attributes = data.drop(['mtype'], axis=1)
motionType = data['mtype']
xtrain, xtest, ytrain, ytest = train_test_split(attributes, motionType, test_size=0.5, random_state=2)
knn = neighbors.KNeighborsClassifier(n_neighbors=2, metric='euclidean', weights='distance')
knn.fit(xtrain, ytrain)
ytestpredict = knn.predict(xtest)
ytrainpredict = knn.predict(xtrain)

linepredict = knn.predict(data.loc[data["mtype"] == 0].drop(['mtype'], axis=1))
logpredict = knn.predict(data.loc[data["mtype"] == 1].drop(['mtype'], axis=1))
rectpredict = knn.predict(data.loc[data["mtype"] == 2].drop(['mtype'], axis=1))
trianglepredict = knn.predict(data.loc[data["mtype"] == 3].drop(['mtype'], axis=1))
#vpredict = knn.predict(data.loc[data["mtype"] == 4].drop(['mtype'], axis=1))

print("KNeighborsClassifier test error: ", np.mean(ytest != ytestpredict)*100)
print("KNeighborsClassifier train error: ", np.mean(ytrain != ytrainpredict)*100)

for i in range(10):
    print("predict " + str(i) + ":", list(knn.predict_proba([xtest.iloc[i]])[0]), ytest.iloc[i])
tr = DecisionTreeClassifier(criterion='entropy', max_depth=6, random_state=20)
tr.fit(X=xtrain, y=ytrain)
ytestpredict = tr.predict(xtest)
ytrainpredict = tr.predict(xtrain)


print("DecisionTreeClassifier test error: ", np.mean(ytest != ytestpredict)*100)
print("DecisionTreeClassifier train error: ", np.mean(ytrain != ytrainpredict)*100)

plot_confusion_matrix(knn, xtest, ytest, normalize='true')
plot_confusion_matrix(tr, xtest, ytest, normalize='true')

tree.export_graphviz(tr, out_file=dotpath, feature_names=attributes.keys(), class_names=['line', 'circle', 'rect', 'triangle', 'v'])

plt.show()
