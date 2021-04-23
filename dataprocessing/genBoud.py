from glove.models.dynamic.templategenerator.bstemplate import BsTemplateGenerator
import pickle
import matplotlib.pyplot as plt
import numpy as np
from swd import decompositionSwingTwist, mulQuat, invQuat

bstg = BsTemplateGenerator(delta=0.05)
seqNum = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
#seqNum = [4]

path = "data/gestures/"
fileind = "line/line({num})"
#fileind = "log/log({num})"
#fileind = "rect/rect({num})"
#fileind = "triangle/triangle({num})"
#fileind = "v/v({num})"
procrec = ".proc"
outpath = "data/bound/{mt}.bst".format(mt=fileind.split("/")[0])
isSave = True
ag = []

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
        axg = axg[ind:invInd]
        ayg = ayg[ind:invInd]
        azg = azg[ind:invInd]
        t = t[ind:invInd]
        ag.append([t, axg, ayg, azg])

        sx = list(sx[ind:invInd])
        sy = list(sy[ind:invInd])
        sz = list(sz[ind:invInd])
        q = q[ind:invInd]
        ql = q[0]

        #swing, twist = decompositionSwingTwist(ql, np.array([0, 0, -1]))
        #twistinv = invQuat(twist)
        #for i in range(len(t)):
        #    _, sx[i], sy[i], sz[i] = mulQuat(mulQuat(twistinv, np.array([0, sx[i], sy[i], sz[i]])), twist)

        bstg.fit(t, [sx, sy, sz])


_, proc = bstg.getProcSeq()
x, bounds = bstg.getBounds()

if isSave:
    with open(outpath, 'xb') as f:
        pickle.dump([x, bounds], f)

fig0, ax = plt.subplots()
ax.set_ylabel("$\Delta{S}/S_{max}$")
ax.set_xlabel('points')
count = 0
for seq in proc:
    color = ['r', 'g', 'b']
    label = ["$S_x$", "$S_y$", "$S_z$"]
    for i in range(3):
        if count == 0:
            ax.plot(x, seq[i], color[i], label=label[i])
        else:
            ax.plot(x, seq[i], color[i])
    count += 1

ax.legend()

fig1, ax = plt.subplots()
ax.set_ylabel("$\Delta{S}/S_{max}$")
ax.set_xlabel('points')
ax.plot(x, bounds[0][0], "r", label="$m_x | M_x$")
ax.plot(x, bounds[0][1], "r")

ax.plot(x, bounds[1][0], "g", label="$m_y | M_y$")
ax.plot(x, bounds[1][1], "g")

ax.plot(x, bounds[2][0], "b", label="$m_z | M_z$")
ax.plot(x, bounds[2][1], "b")
ax.legend()

fig2, ax = plt.subplots()
ax.set_ylabel("$\Delta{a}/a_{max}$")
ax.set_xlabel('$\Delta{t}/t_{max}$')
count = 0
for a in ag:
    a[0] = (np.array(a[0]) - a[0][0])/(a[0][-1] - a[0][0])
    maxarg = np.amax(np.abs(a[1:]))
    a[1] = np.array(a[1]/maxarg)
    a[2] = np.array(a[2]/maxarg)
    a[3] = np.array(a[3]/maxarg)
    if count == 0:
        ax.plot(a[0], a[1], "r", label="$a_x$")
        ax.plot(a[0], a[2], "g", label="$a_y$")
        ax.plot(a[0], a[3], "b", label="$a_z$")
    else:
        ax.plot(a[0], a[1], "r")
        ax.plot(a[0], a[2], "g")
        ax.plot(a[0], a[3], "b")
    count += 1

ax.legend()
plt.show()
