import time
from pynput import keyboard
from glove.gloveHandle import GloveHandle, SourceConfig, Sources

filename = "data/glovetest.rec"
file = open(filename, 'rb')

glove = GloveHandle(SourceConfig(Sources.SIMULATION, data=bytearray(file.read())), nonBlocking=False)


@glove.imuFrameDecorator
def imuFrame(data):
    print("IMU data: ", data)
    time.sleep(0.5)


@glove.deformationFrameDecorator
def deformationFrame(data):
    print("deformation data: ", data)


glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: print("FRAME:", data)
                                               ))
glove.connect("IMU_FRAME", imuFrame)
glove.connect("DEFORMATION_FRAME", deformationFrame)
glove.open()
glove.start()
time.sleep(10)
glove.exit()