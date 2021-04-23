import pickle
import matplotlib.pyplot as plt
import numpy as np
from glove.models.dynamic.templategenerator.mlctemplate import MlcTemplateGenerator
from util.extmath import *
import pandas as pd
import seaborn as sns

parts = 2
mlctg = MlcTemplateGenerator(part=parts)
seqNum = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
#seqNum = [7, 8, 10]

motionTypes = {
    "line": 0,
    "log": 1,
    "rect": 2,
    "triangle": 3,
    "v": 4
}

path = "data/gestures/"
#fileind = "line/line({num})"
#fileind = "log/log({num})"
#fileind = "rect/rect({num})"
#fileind = "triangle/triangle({num})"
fileind = "v/v({num})"
procrec = ".proc"
outpath = "data/ml/{mt}({parts}p).mlt".format(mt=fileind.split("/")[0], parts=parts)
isSave = True

ag = []
motionType = motionTypes[fileind.split("/")[0]]
print(motionType)

for num in seqNum:
    with open((path + fileind + procrec).format(num=num), 'rb') as f:
        procDict = pickle.load(f)
        t = procDict["itime"]
        ax = procDict["ax"]
        ay = procDict["ay"]
        az = procDict["az"]

        axg = procDict["axg"]
        ayg = procDict["ayg"]
        azg = procDict["azg"]

        q = procDict["q"]

        ind = 0
        invInd = -1

        while (axg[ind] == 0) and (ayg[ind] == 0) and (azg[ind] == 0):
            ind += 1

        while (axg[invInd] == 0) and (ayg[invInd] == 0) and (azg[invInd] == 0):
            invInd -= 1

        axg = axg[ind:invInd]
        ayg = ayg[ind:invInd]
        azg = azg[ind:invInd]
        ax = ax[ind:invInd]
        ay = ay[ind:invInd]
        az = az[ind:invInd]
        t = t[ind:invInd]

        ag.append([t, axg, ayg, azg])
        q = q[ind:invInd]

        for i in range(len(t)):
            qinv = invQuat(q[i])
            gla = mulQuat(mulQuat(q[i], np.array([0, ax[i], ay[i], az[i]])), qinv)
            gla = gla[1:]
            gla[-1] -= 1.0
            gla[-1] = -gla[-1]
            ax[i] = gla[0]
            ay[i] = gla[1]
            az[i] = gla[2]

        mlctg.fit(t, [ax, ay, az])

rawseq = mlctg.getRawSeq()
x, proc = mlctg.getProcSeq()
steps, params = mlctg.getParam()

df = pd.DataFrame(params)
#sns.heatmap(df.corr(), xticklabels=df.columns.values, yticklabels=df.columns.values)
df["mtype"] = [motionType] * len(seqNum)
if isSave:
    df.to_pickle(outpath)

print(df)
df.info()
df.hist()
print(df.columns.values)

fig0, ax = plt.subplots()
ax.set_ylabel("$a, м/с^2$")
ax.set_xlabel('t, c')
count = 0

for t, seq in rawseq:
    color = ['r', 'g', 'b']
    label = ["$a_x$", "$a_y$", "$a_z$"]
    t = t - t[0]
    for i in range(3):
        if count == 0:
            ax.plot(t, seq[i], color[i], label=label[i])
        else:
            ax.plot(t, seq[i], color[i])
    count += 1
#ax.plot([0, 1], [0, 0], 'k:')
ax.legend()


fig1, ax = plt.subplots()
ax.set_ylabel("$\Delta{a}/a_{max}$")
ax.set_xlabel('points')
count = 0

for seq in proc:
    color = ['r', 'g', 'b']
    label = ["$a_x$", "$a_y$", "$a_z$"]
    for i in range(3):
        if count == 0:
            ax.plot(x, seq[i], color[i], label=label[i])
        else:
            ax.plot(x, seq[i], color[i])
    count += 1
ax.plot([0, 1], [0, 0], 'k:')

ax.legend()

print(steps)
try:
    a = steps[0]/steps[-1]
    b = steps[-1]/steps[-1]
except ZeroDivisionError:
    a = 0
    b = 1
stepSize = (b - a)/len(steps)

procNum = 2

fig2, ax = plt.subplots()

ax.plot([0, 1], [0, 0], 'k:')
for i in range(len(steps)+1):
    ax.plot([a + i/len(steps), a + i/len(steps)], [-1.0, 1.0], 'k:')

color = ['r', 'g', 'b']
label = ["$K_x$", "$K_y$", "$K_z$"]
for i in range(3):
    ax.plot(x, proc[procNum][i], color[i], label=label[i])
ax.legend()

fig3 = plt.figure()

ax_1 = fig3.add_subplot(3, 1, 1)
ax_1.set(xlabel="points", ylabel="$K_x  params$")
ax_2 = fig3.add_subplot(3, 1, 2)
ax_2.set(xlabel="points", ylabel="$K_y  params$")
ax_3 = fig3.add_subplot(3, 1, 3)
ax_3.set(xlabel="points", ylabel="$K_z  params$")

meanKx = []
for i in range(len(steps)):
    meanKx.append(params[procNum]["abs_mean_Kx" + str(i)])
meanKy = []
for i in range(len(steps)):
    meanKy.append(params[procNum]["abs_mean_Ky" + str(i)])
meanKz = []
for i in range(len(steps)):
    meanKz.append(params[procNum]["abs_mean_Kz" + str(i)])

maamKx = []
for i in range(len(steps)):
    maamKx.append(params[procNum]["max_abs_abs_mean_Kx" + str(i)])
maamKy = []
for i in range(len(steps)):
    maamKy.append(params[procNum]["max_abs_abs_mean_Ky" + str(i)])
maamKz = []
for i in range(len(steps)):
    maamKz.append(params[procNum]["max_abs_abs_mean_Kz" + str(i)])

ax_1.bar(np.linspace(a, b-stepSize, len(steps)), meanKx, width=stepSize/2, color='y', alpha=0.8, align='edge', label='$|\overline{K_x}|$')
ax_1.bar(np.linspace(a+stepSize/2, b-stepSize/2, len(steps)), maamKx, width=stepSize/2, color='g', alpha=0.8, align='edge', label='$(|K_x|_{max}-|\overline{K_x}|)$')
ax_1.plot([0, 1], [0, 0], 'k:')
for i in range(len(steps)+1):
    ax_1.plot([a + i/len(steps), a + i/len(steps)], [0.0, 1.0], 'k:')
ax_1.legend()

ax_2.bar(np.linspace(a, b-stepSize, len(steps)), meanKy, width=stepSize/2, color='y', alpha=0.8, align='edge', label='$|\overline{K_y}|$')
ax_2.bar(np.linspace(a+stepSize/2, b-stepSize/2, len(steps)), maamKy, width=stepSize/2, color='g', alpha=0.8, align='edge', label='$(|K_y|_{max}-|\overline{K_y}|)$')
ax_2.plot([0, 1], [0, 0], 'k:')
for i in range(len(steps)+1):
    ax_2.plot([a + i/len(steps), a + i/len(steps)], [0.0, 1.0], 'k:')
ax_2.legend()

ax_3.bar(np.linspace(a, b-stepSize, len(steps)), meanKz, width=stepSize/2, color='y', alpha=0.8, align='edge', label='$|\overline{K_z}|$')
ax_3.bar(np.linspace(a+stepSize/2, b-stepSize/2, len(steps)), maamKz, width=stepSize/2, color='g', alpha=0.8, align='edge', label='$(|K_z|_{max}-|\overline{K_z}|)$')
ax_3.plot([0, 1], [0, 0], 'k:')
for i in range(len(steps)+1):
    ax_3.plot([a + i/len(steps), a + i/len(steps)], [0.0, 1.0], 'k:')
ax_3.legend()

plt.show()


