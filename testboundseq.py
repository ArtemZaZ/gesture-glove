import matplotlib.pyplot as plt
import seaborn as sns
from glove.models.dynamic.boundseq import BoundingSequencesModel
import pickle
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

datapath = "dataprocessing/data/gestures/"
linefileind = "line/line({num})"
logfileind = "log/log({num})"
rectfileind = "rect/rect({num})"
trianglefileind = "triangle/triangle({num})"
vfileind = "v/v({num})"
datatail = ".proc"
dataSeqNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

boundpath = "dataprocessing/data/bound/"
boundtail = ".bst".format()


def getBound(filepath):
    with open(filepath, 'rb') as f:
        x, bounds = pickle.load(f)
    return x, bounds


lineBS = BoundingSequencesModel({"boundSecPath": boundpath + "line" + boundtail})
logBS = BoundingSequencesModel({"boundSecPath": boundpath + "log" + boundtail})
rectBS = BoundingSequencesModel({"boundSecPath": boundpath + "rect" + boundtail})
triangleBS = BoundingSequencesModel({"boundSecPath": boundpath + "triangle" + boundtail})
vBS = BoundingSequencesModel({"boundSecPath": boundpath + "v" + boundtail})

data = {"line": [], "log": [], "rect": [], "triangle": [], "v": []}
motionClassifier = {0: lineBS, 1: logBS, 2: rectBS, 3: triangleBS, 4: vBS}


def classify(s):
    class scope:
        data = {"seq": s}
    maxind = 0
    predictval = 0.0
    for key in motionClassifier.keys():
        p = motionClassifier[key].classify(scope)
        if p > predictval:
            predictval = p
            maxind = key
    return maxind, predictval


for key in data.keys():
    fileind = key + "/" + key + "({num})"
    for num in dataSeqNum:
        with open((datapath + fileind + datatail).format(num=num), 'rb') as f:
            procDict = pickle.load(f)
            t = procDict["itime"]
            axg = procDict["axg"]
            ayg = procDict["ayg"]
            azg = procDict["azg"]

            sx = procDict["sx"]
            sy = procDict["sy"]
            sz = procDict["sz"]
            ind = 0
            invInd = -1
            while (axg[ind] == 0) and (ayg[ind] == 0) and (azg[ind] == 0):
                ind += 1
            while (axg[invInd] == 0) and (ayg[invInd] == 0) and (azg[invInd] == 0):
                invInd -= 1
            axg = axg[ind:invInd]
            ayg = ayg[ind:invInd]
            azg = azg[ind:invInd]
            t = t[ind:invInd]
            sx = list(sx[ind:invInd])
            sy = list(sy[ind:invInd])
            sz = list(sz[ind:invInd])

            t = np.array(t) - t[0]  # нормализуем t
            t = t / t[-1]
            sx = np.interp(np.linspace(0, 1, 1000), t, sx)
            sy = np.interp(np.linspace(0, 1, 1000), t, sy)
            sz = np.interp(np.linspace(0, 1, 1000), t, sz)
            seq = np.array([sx, sy, sz])
            maxarg = np.amax(np.abs(seq))
            seq = seq / maxarg

            data[key].append(seq)

            """
            print("lineBS predict {ind}:".format(ind=fileind.split("/")[0]), lineBS.classify(scope))
            print("logBS predict {ind}:".format(ind=fileind.split("/")[0]), logBS.classify(scope))
            print("rectBS predict {ind}:".format(ind=fileind.split("/")[0]), rectBS.classify(scope))
            print("triangleBS predict {ind}:".format(ind=fileind.split("/")[0]), triangleBS.classify(scope))
            print("vBS predict {ind}:".format(ind=fileind.split("/")[0]), vBS.classify(scope))
            """

predict = []
for type in ["line", "log", "rect", "triangle", "v"]:
    for seq in data[type]:
        k, v = classify(seq)
        if v < 0.80:
            k = -1
        predict.append(k)
        print(k, v)

trueVal = [0]*10 + [1]*10 + [2]*10 + [3]*10 + [4]*10

conf = confusion_matrix(trueVal, predict, normalize="true")
disp = ConfusionMatrixDisplay(confusion_matrix=conf,
                              display_labels=["drop", "line", "log", "rect", "triangle", "v"])
print(conf)
disp.plot()
plt.show()