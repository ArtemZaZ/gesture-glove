import sys
import time
from util.extmath import *
import numpy as np
from vispy import app, scene
from glove.gloveHandle import GloveHandle, SourceConfig, Sources
from plotting.imuplotter import ImuPlotter
from util.filers import MagvikFilter, LPFilterIterator
import pickle

#glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM10", baudrate=115200), nonBlocking=True)

path = "data/gestures/"
fileind = "triangle/triangle(17)"
#fileind = "log/log(18)"
#fileind = "rect/rect(20)"
#fileind = "triangle/triangle(20)"
#fileind = "v/v(20)"
rec = ".rec"
procpath = "data/gestures/"
procrec = ".proc"

glove = GloveHandle(SourceConfig(Sources.SIMULATION,
                                 data=bytearray(open(path + fileind + rec, "rb").read()),
                                 frametime=0.001), nonBlocking=False)
plotter = ImuPlotter(sampleInterval=0.0002, timeWindow=5.)
axgo = 0
aygo = 0
azgo = 0
t = 0
mag = MagvikFilter(beta=1)
count = 0
q = [1, 0, 0, 0]
vx = 0
vy = 0
vz = 0
sx = 0
sy = 0
sz = 0

procDict = {"ax": [], "ay": [], "az": [],
            "wx": [], "wy": [], "wz": [],
            "axg": [], "ayg": [], "azg": [],
            "vx": [], "vy": [], "vz": [],
            "sx": [], "sy": [], "sz": [],
            "q": [], "itime": [],
            "d1": [], "d2": [], "d3": [], "d4": [], "d5": [], "ftime": []}


@glove.imuFrameDecorator
def imuFrame(data):
    global mplotter, t, mag
    global axgo, aygo, azgo
    global q, count
    global vx, vy, vz
    global sx, sy, sz
    ax = data[0] / 32768 * 4 - 0.05
    ay = data[1] / 32768 * 4 - 0.00
    az = data[2] / 32768 * 4 - 0.045
    wx = (np.pi / 180) * ((data[3] + 90) / 32768 * 500)
    wy = (np.pi / 180) * ((data[4] + 0) / 32768 * 500)
    wz = (np.pi / 180) * ((data[5] + 30) / 32768 * 500)
    tm = data[-1] / 1000
    t += tm

    mag.update(ax, ay, az, wx, wy, wz, tm)
    if t < 0.8:
        return

    if t > 2.2:
        return

    q = mag.getQuat()
    #swing, twist = decompositionSwingTwist(q, np.array([0, 0, -1]))
    #q = swing
    qinv = invQuat(q)
    gla = mulQuat(mulQuat(q, np.array([0, ax, ay, az])), qinv)
    gla = gla[1:]
    gla[-1] -= 1.0
    gla[-1] = -gla[-1]

    kp = 0.35
    axgo = LPFilterIterator(gla[0] * 9.8, axgo, kp)
    aygo = LPFilterIterator(gla[1] * 9.8, aygo, kp)
    azgo = LPFilterIterator(gla[2] * 9.8, azgo, kp)
    #print(azgo)

    tr = 0.75
    kpv = 0.80

    if abs(axgo) < tr:
        axgo = 0.0
    if abs(aygo) < tr:
        aygo = 0.0
    if abs(azgo) < tr:
        azgo = 0.0

    vx = LPFilterIterator(vx, 0, kpv)
    vy = LPFilterIterator(vy, 0, kpv)
    vz = LPFilterIterator(vz, 0, kpv)

    sx = axgo * (tm * tm / 2) + vx * tm + sx
    sy = aygo * (tm * tm / 2) + vy * tm + sy
    sz = azgo * (tm * tm / 2) + vz * tm + sz

    vx = axgo * tm + vx
    vy = aygo * tm + vy
    vz = azgo * tm + vz

    procDict["ax"].append(ax)
    procDict["ay"].append(ay)
    procDict["az"].append(az)
    procDict["wx"].append(wx)
    procDict["wy"].append(wy)
    procDict["wz"].append(wz)
    procDict["axg"].append(axgo)
    procDict["ayg"].append(aygo)
    procDict["azg"].append(azgo)
    procDict["vx"].append(vx)
    procDict["vy"].append(vy)
    procDict["vz"].append(vz)
    procDict["sx"].append(sx)
    procDict["sy"].append(sy)
    procDict["sz"].append(sz)
    procDict["q"].append(q)
    procDict["itime"].append(t)

    if count > 10:
        count = 0
    count += 1

    plotter.addPoint(sx, sy, sz, t)
    #plotter.addPoint(azgo, vz, sz*100, t)


@glove.deformationFrameDecorator
def deformationFrame(data):
    procDict["d1"].append(data[0])
    procDict["d2"].append(data[1])
    procDict["d3"].append(data[2])
    procDict["d4"].append(data[3])
    procDict["d5"].append(data[4])

glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: None))
glove.connect("IMU_FRAME", imuFrame)
glove.connect("DEFORMATION_FRAME", deformationFrame)

glove.open()
glove.start()
time.sleep(11)
with open(procpath + fileind + procrec, 'xb') as f:
    pickle.dump(procDict, f)

glove.exit()
plotter.exit()
