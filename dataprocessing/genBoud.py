from glove.models.dynamic.templategenerator.bstemplate import BsTemplateGenerator
import pickle
import matplotlib.pyplot as plt
import numpy as np

from swd import decompositionSwingTwist, mulQuat, invQuat

bstg = BsTemplateGenerator(delta=0.05)
#seqNum = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
seqNum = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

path = "data/gestures/"
#fileind = "line/line({num})"
#fileind = "log/log({num})"
#fileind = "rect/rect({num})"
#fileind = "triangle/triangle({num})"
fileind = "v/v({num})"
procrec = ".proc"
for num in seqNum:
    with open((path + fileind + procrec).format(num=num), 'rb') as f:
        procDict = pickle.load(f)
        t = procDict["itime"]
        axg = procDict["axg"]
        ayg = procDict["ayg"]
        azg = procDict["azg"]
        sx = procDict["sx"]
        sy = procDict["sy"]
        sz = procDict["sz"]
        q = procDict["q"]

        ind = 0
        invInd = -1

        while (axg[ind] == 0) and (ayg[ind] == 0) and (azg[ind] == 0):
            ind += 1

        while (axg[invInd] == 0) and (ayg[invInd] == 0) and (azg[invInd] == 0):
            invInd -= 1

        #print(ind, invInd)

        sx = list(sx[ind:invInd])
        sy = list(sy[ind:invInd])
        sz = list(sz[ind:invInd])
        t = t[ind:invInd]
        q = q[ind:invInd]
        ql = q[0]

        #swing, twist = decompositionSwingTwist(ql, np.array([0, 0, -1]))
        #twistinv = invQuat(twist)
        #for i in range(len(t)):
        #    _, sx[i], sy[i], sz[i] = mulQuat(mulQuat(twistinv, np.array([0, sx[i], sy[i], sz[i]])), twist)

        bstg.fit(t, [sx, sy, sz])


_, proc = bstg.getProcSeq()
x, bounds = bstg.getBounds()

fig0, ax = plt.subplots()

for seq in proc:
    color = ['r', 'g', 'b']
    for i in range(3):
        ax.plot(x, seq[i], color[i])


fig1, ax = plt.subplots()

ax.plot(x, bounds[0][0], "r")
ax.plot(x, bounds[0][1], "r")

ax.plot(x, bounds[1][0], "g")
ax.plot(x, bounds[1][1], "g")

ax.plot(x, bounds[2][0], "b")
ax.plot(x, bounds[2][1], "b")

plt.show()
