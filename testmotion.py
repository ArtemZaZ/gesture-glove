import sys
import time

from madgwick.madgwickahrs import MadgwickAHRS
from madgwick.quaternion import Quaternion
from util.extmath import *
import numpy as np
from vispy import app, scene
from glove.gloveHandle import GloveHandle, SourceConfig, Sources
from util.filers import MagvikFilter, LPFilterIterator
from plotting.motionplotter import MotionPlotter
import imageio
from multiprocessing import Process

np.set_printoptions(suppress=True)

output_filename = 'animation.gif'
glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM7", baudrate=115200), nonBlocking=False)
mplotter = MotionPlotter()
axgo = 0
aygo = 0
azgo = 0
t = 0
mag = MagvikFilter()

qbase = np.array([1, 0, 0, 0])
q = np.array([1, 0, 0, 0])
qr = np.array([1, 0, 0, 0])
swing = np.array([1, 0, 0, 0])
twist = np.array([1, 0, 0, 0])
vx = 0
vy = 0
vz = 0
sx = 0
sy = 0
sz = 0


#@glove.imuFrameDecorator
def imuFrame(data):
    global mplotter, t, mag
    global axgo, aygo, azgo
    global q, qr, count
    global vx, vy, vz
    global sx, sy, sz
    global swing, twist
    ax = data[0] / 32768 * 4 + 0.015
    ay = data[1] / 32768 * 4 - 0.00
    az = data[2] / 32768 * 4 - 0.07
    wx = (np.pi / 180) * ((data[3] + 90) / 32768 * 500)
    wy = (np.pi / 180) * ((data[4] + 0) / 32768 * 500)
    wz = (np.pi / 180) * ((data[5] + 25) / 32768 * 500)
    tm = float(data[-1]) / 1000
    t += tm

    mag.update(ax, ay, az, wx, wy, wz, tm)
    q = mag.getQuat()
    qr = mulQuat(q, invQuat(qbase))
    swing, twist = decompositionSwingTwist(q, np.array([0, 0, 1]))

    qinv = invQuat(q)
    gla = mulQuat(mulQuat(q, np.array([0, ax, ay, az])), qinv)
    gla = gla[1:]
    gla[-1] -= 1
    gla[-1] = -gla[-1]

    kp = 0.2
    axgo = LPFilterIterator(gla[0] * 9.8, axgo, kp)
    aygo = LPFilterIterator(gla[1] * 9.8, aygo, kp)
    azgo = LPFilterIterator(gla[2] * 9.8, azgo, kp)

    tr = 0.2
    kpv = 0.92

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



#@glove.deformationFrameDecorator
def deformationFrame(data):
    pass
    # print("deformation data: ", data)


@mplotter.events.key_press.connect
def on_key_press(event):
    global mplotter
    global sx, sy, sz
    global vx, vy, vz
    global q, qbase, mag
    global swing, twist
    global isSaving
    if event.text == '1':
        vx, vy, vz = 0, 0, 0
        sx, sy, sz = 0, 0, 0
        qbase = mulQuat(q, invQuat(np.array([1, 0, 0, 0])))
        qbase = mulQuat(qbase, swing)
        mplotter.resetTransform()
    if event.text == '2':
        isSaving = not isSaving
        print("start saving: ", isSaving)


#glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: None))
glove.connect("IMU_FRAME", imuFrame)
glove.connect("DEFORMATION_FRAME", deformationFrame)

glove.open()
glove.start()

writer = imageio.get_writer(output_filename)
count = 0


isSaving = False
def update(ev):
    global qr, count
    global vxo, vyo, vzo
    global sx, sy, sz
    global mplotter
    global writer
    global isSaving
    if isSaving:
        image = mplotter.render()
        writer.append_data(image)

    mplotter.transformCube((sx*100, sy*100, sz*100), qr)
    mplotter.update()


timer = app.Timer(interval=0.08)
timer.connect(update)
timer.start()

if sys.flags.interactive != 1:
    app.run()
writer.close()
glove.exit()
