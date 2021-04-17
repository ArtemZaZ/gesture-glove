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
from plotting.linadcanvas import LinadCanvas
from glove.models.segmentation.linad import LinadModel

np.set_printoptions(suppress=True)

output_filename1 = '../glovelinad(g)(1).gif'
output_filename2 = '../glovelinad(l)(1).gif'
gloveCanvas = GloveCanvas()

test = {
    "name": "thumb-down",
    "activationList": [
        "70 <= little_flex <= 90",
        "70 <= ring_flex <= 90",
        "70 <= middle_flex <= 90",
        "70 <= index_flex <= 90",
        "0 <= thumb_flex <= 20",
        "55 <= pitch <= 80",
    ],
    "deactivationList": []
}

linad = LinadModel(rules=test)
linadCanvas = LinadCanvas(linad, view=(True, False))


#glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM7", baudrate=115200), nonBlocking=False)
#glove = GloveHandle(SourceConfig(Sources.BLUETOOTH, port=1, host="00:21:13:04:d9:63"), nonBlocking=False)
glove = GloveHandle(SourceConfig(Sources.SIMULATION, data=bytearray(open("../dataprocessing/data/thumb_down(2).rec", "rb").read()), frametime=0.01), nonBlocking=False)
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
    if pitch > 0:
        pitch -= 8
    roll = int(roll)
    angles = (yaw, pitch, roll)


#@glove.deformationFrameDecorator
def deformationFrame(data):
    global flex
    flex = (min(max(0, -int((data[0] - 200) * 1.0)), 90),
            min(max(0, int((data[4] - 74) * 1.2)), 90),
            min(max(0, int((data[3] - 130) * 1.9)), 90),
            min(max(0, int((data[2] - 45) * 1.5)), 90),
            min(max(0, int((data[1] - 130) * 3.0)), 90))


#glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: None))
glove.connect("IMU_FRAME", imuFrame)
glove.connect("DEFORMATION_FRAME", deformationFrame)

glove.open()
glove.start()

writer1 = imageio.get_writer(output_filename1)
writer2 = imageio.get_writer(output_filename2)
isSaving = False


def update(ev):
    global flex, angles
    global gloveCanvas, linad, linadCanvas
    global writer
    global isSaving
    if isSaving:
        image1 = gloveCanvas._canvas.render()
        image2 = linadCanvas._canvas.render()
        writer1.append_data(image1)
        writer2.append_data(image2)

    linad.update({"thumb_flex": flex[0], "index_flex": flex[1], "middle_flex": flex[2], "ring_flex": flex[3],
                  "little_flex": flex[4], "yaw": angles[0], "pitch": angles[1], "roll": angles[2]})
    linadCanvas.update()
    gloveCanvas.update(flex, angles)


timer = app.Timer(interval=0.05)
timer.connect(update)
timer.start()

if sys.flags.interactive != 1:
    app.run()
writer1.close()
writer2.close()
glove.exit()