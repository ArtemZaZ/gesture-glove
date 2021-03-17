import sys
import time
from util.extmath import *
import numpy as np
from vispy import app, scene
from glove.gloveHandle import GloveHandle, SourceConfig, Sources
from plotting.imuplotter import ImuPlotter
from util.filers import MagvikFilter, LPFilterIterator

glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM10", baudrate=115200), nonBlocking=True)
plotter = ImuPlotter(sampleInterval=0.002, timeWindow=5.)
axgo = 0
aygo = 0
azgo = 0
kp = 0.2
t = 0
mag = MagvikFilter()


@glove.imuFrameDecorator
def imuFrame(data):
    global plotter, t, mag
    global axgo, aygo, azgo
    ax = data[0] / 32768 * 4 + 0.015
    ay = data[1] / 32768 * 4 - 0.00
    az = data[2] / 32768 * 4 - 0.045
    wx = (np.pi / 180) * ((data[3] + 90) / 32768 * 500)
    wy = (np.pi / 180) * ((data[4] + 0) / 32768 * 500)
    wz = (np.pi / 180) * ((data[5] + 25) / 32768 * 500)
    tm = data[-1] / 1000
    t += tm
    print(tm)

    mag.update(ax, ay, az, wx, wy, wz, tm)
    q = mag.getQuat()

    qinv = invQuat(q)
    gla = mulQuat(mulQuat(q, np.array([0, ax, ay, az])), qinv)
    gla = gla[1:]
    gla[-1] -= 1
    gla[-1] = -gla[-1]

    axg = LPFilterIterator(gla[0] * 9.8, axgo, kp)
    ayg = LPFilterIterator(gla[1] * 9.8, aygo, kp)
    azg = LPFilterIterator(gla[2] * 9.8, azgo, kp)
    axgo = axg
    aygo = ayg
    azgo = azg

    plotter.addPoint(axg, ayg, azg, t)


@glove.deformationFrameDecorator
def deformationFrame(data):
    pass
    #print("deformation data: ", data)


glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: None))
glove.connect("IMU_FRAME", imuFrame)
glove.connect("DEFORMATION_FRAME", deformationFrame)

glove.open()
glove.start()
while True:
    plotter.update()
    time.sleep(0.02)
glove.exit()
plotter.exit()
