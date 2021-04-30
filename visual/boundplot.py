import sys
import time

from vispy import app, scene
import matplotlib.pyplot as plt
import seaborn as sns

from glove.gesturefsm import GestureFsm
from glove.models.dynamic.boundseq import BoundingSequencesModel
import pickle
import numpy as np
from plotting.linadcanvas import LinadCanvas
from glove.models.segmentation.linad import LinadModel

bound = BoundingSequencesModel({"boundSecPath": "../dataprocessing/data/bound/triangle.bst"})
procDict = pickle.load(open("../dataprocessing/data/gestures/triangle/triangle(4).proc", "rb"))
dataoutPath = "triangle(4).seq"
isSave = True

test = {
    "name": "thumb-down",
    "activationList": [
        "70 <= little_flex",
        "70 <= ring_flex",
        "middle_flex <= 20",
        "index_flex <= 20",
        "thumb_flex <= 20",
        "not ((9.8-1.2) < sqrt(ax**2+ay**2+az**2) < (9.8+1.0))",
        "(time-t[5]) > 0.03"
    ],
    "deactivationList": [
        "(9.8-1.0) < sqrt(ax**2+ay**2+az**2) < (9.8+1.0)",
        "(time-t[0]) > 0.03"
    ]
}


class Scope:
    def __init__(self):
        self._data = {"seq": [[], [], []], "tm": []}

    def update(self, frame):
        self._data["seq"][0].append(frame["sx"])
        self._data["seq"][1].append(frame["sy"])
        self._data["seq"][2].append(frame["sz"])
        self._data["tm"].append(frame["tm"])

    def reset(self):
        del self._data["seq"]
        self._data = {"seq": []}

    @property
    def data(self):
        global bound, isSave

        t = self._data["tm"]
        sx = self._data["seq"][0][:]
        sy = self._data["seq"][1][:]
        sz = self._data["seq"][2][:]

        if isSave:
            pickle.dump({"seq": [t, sx, sy, sz], "bounds": bound._bounds}, open(dataoutPath, "wb"))

        t = np.array(t) - t[0]  # нормализуем t
        t = t / t[-1]
        print(len(t), len(sx))
        sx = np.interp(np.linspace(0, 1, 1000), t, sx)
        sy = np.interp(np.linspace(0, 1, 1000), t, sy)
        sz = np.interp(np.linspace(0, 1, 1000), t, sz)
        seq = np.array([sx, sy, sz])
        maxarg = np.amax(np.abs(seq))
        seq = seq / maxarg
        sx, sy, sz = seq

        for i, dim in enumerate(bound._bounds):
            color = ['r', 'g', 'b']
            for dir in dim:
                plt.plot(np.linspace(0, 1, 1000), dir, color[i])

        plt.plot(np.linspace(0, 1, 1000), sx, "r:")
        plt.plot(np.linspace(0, 1, 1000), sy, "g:")
        plt.plot(np.linspace(0, 1, 1000), sz, "b:")

        return {"seq": [sx, sy, sz]}


linad = LinadModel(rules=test)
linadCanvas = LinadCanvas(linad, view=(True, True))
gfsm = GestureFsm(segmentation=linad, dynamicModel=bound, dynamicScope=Scope(), handler=lambda x: print("gesture:", x))

t = procDict["itime"]
ax = np.array(procDict["ax"]) * 9.8
ay = np.array(procDict["ay"]) * 9.8
az = np.array(procDict["az"]) * 9.8
axg = procDict["axg"]
ayg = procDict["ayg"]
azg = procDict["azg"]
sx = procDict["sx"]
sy = procDict["sy"]
sz = procDict["sz"]

d1, d2, d3, d4, d5 = procDict["d1"], procDict["d2"], procDict["d3"], procDict["d4"], procDict["d5"],
d = [None, None, None, None, None]

for i in range(5):
    q = procDict["d" + str(i + 1)]
    d[i] = np.interp(t, np.linspace(t[0], t[-1], len(q)), q)

d[0] = -((d[0] - 190) * 1.0)
d[1] = ((d[1] - 140) * 3.0)
d[2] = ((d[2] - 75) * 1.6)
d[3] = ((d[3] - 165) * 1.9)
d[4] = ((d[4] - 90) * 1.2)
flex = [d[0], d[4], d[3], d[2], d[1]]

#plt.plot(t, sx)
#plt.show()

count = 0


def update(ev):
    try:
        global count, linad, linadCanvas, flex, ax, ay, az, t, gfsm, timer
        print(t[count], gfsm._state)
        gfsm.update({"thumb_flex": float(flex[0][count]), "index_flex": float(flex[1][count]),
                     "middle_flex": float(flex[2][count]), "ring_flex": float(flex[3][count]),
                     "little_flex": float(flex[4][count]), "ax": float(ax[count]),
                     "ay": float(ay[count]), "az": float(az[count]), "tm": float(t[count]),
                     "sx": float(sx[count]), "sy": float(sy[count]), "sz": float(sz[count])})
        #linadCanvas.update()
        count += 1
    except:
        timer.stop()
        plt.show()


timer = app.Timer(interval=0.01)
timer.connect(update)
timer.start()

if sys.flags.interactive != 1:
    app.run()
