import sys
import time

from util.extmath import *
import numpy as np
from vispy import app, scene
from glove.gloveHandle import GloveHandle, SourceConfig, Sources
from util.filers import MagvikFilter, LPFilterIterator
from util.extmath import angleFromQuat
import imageio
from plotting.glovecanvas import GloveCanvas

np.set_printoptions(suppress=True)

output_filename = '../glovecanvas.gif'
gloveCanvas = GloveCanvas()

#glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM7", baudrate=115200), nonBlocking=False)
#glove = GloveHandle(SourceConfig(Sources.BLUETOOTH, port=1, host="00:21:13:04:d9:63"), nonBlocking=False)
glove = GloveHandle(SourceConfig(Sources.SIMULATION, data=bytearray(open("../dataprocessing/data/glovetest.rec", "rb").read())), nonBlocking=False)

mag = MagvikFilter()
angles = (0, 0, 0)
flex = (0, 0, 0, 0, 0)


#@glove.imuFrameDecorator
def imuFrame(data):
    global gloveCanvas, mag, angles

    ax = data[0] / 32768 * 4 - 0.05
    ay = data[1] / 32768 * 4 - 0.00
    az = data[2] / 32768 * 4 - 0.045
    wx = (np.pi / 180) * ((data[3] + 90) / 32768 * 500)
    wy = (np.pi / 180) * ((data[4] + 0) / 32768 * 500)
    wz = (np.pi / 180) * ((data[5] + 30) / 32768 * 500)
    tm = data[-1] / 1000

    mag.update(ax, ay, az, wx, wy, wz, tm)
    q = mag.getQuat()
    yaw, pitch, roll = angleFromQuat(q)
    yaw = int(yaw)
    pitch = int(pitch)
    roll = int(roll)
    angles = (yaw, pitch, roll)


#@glove.deformationFrameDecorator
def deformationFrame(data):
    global flex
    flex = data[:5]


#glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: None))
glove.connect("IMU_FRAME", imuFrame)
glove.connect("DEFORMATION_FRAME", deformationFrame)

glove.open()
glove.start()

writer = imageio.get_writer(output_filename)
isSaving = False


def update(ev):
    global gloveCanvas, flex, angles
    global writer
    global isSaving
    if isSaving:
        image = gloveCanvas._canvas.render()
        writer.append_data(image)

    gloveCanvas.update(flex, angles)


timer = app.Timer(interval=0.1)
timer.connect(update)
timer.start()

if sys.flags.interactive != 1:
    app.run()
writer.close()
glove.exit()