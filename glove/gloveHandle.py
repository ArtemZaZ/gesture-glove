import socket
import struct

import serial
import threading
from glove import proto
from util import eventmaster
import time


class Sources:
    USB_TTL = 0
    BLUETOOTH = 1


class SourceConfig:
    def __init__(self, sourceType, **kwargs):
        self.sourceType = sourceType
        if sourceType is Sources.USB_TTL:
            try:
                self.portName = kwargs['portName']
            except KeyError:
                raise KeyError("Не указан аттрибут 'portName' ресурса")
            try:
                self.baudrate = kwargs['baudrate']
            except KeyError:
                raise KeyError("Не указан аттрибут 'baudrate' ресурса")
        elif sourceType is Sources.BLUETOOTH:
            try:
                self.host = kwargs['host']
            except KeyError:
                raise KeyError("Не указан аттрибут 'host' ресурса")
            try:
                self.port = kwargs['port']
            except KeyError:
                raise KeyError("Не указан аттрибут 'port' ресурса")
        else:
            raise AttributeError("Указан некорректный тип ресурса")


class GloveHandle(threading.Thread):
    """ Класс перчатки-джойстика """

    def __init__(self, sourceConfig, nonBlocking=True):
        threading.Thread.__init__(self, daemon=True)
        self._sourceConfig = sourceConfig
        self._nonBlocking = nonBlocking
        self.__exit = False  # метка выхода из потока
        self._eventDict = {  # словарь событий
            "FRAME": eventmaster.Event("FRAME"),  # событие новых данных с датчиков
            "IMU_FRAME": eventmaster.Event("IMU_FRAME"),
            "DEFORMATION_FRAME": eventmaster.Event("DEFORMATION_FRAME")
        }
        self._eventMaster = eventmaster.EventMaster()  # Мастер событий
        self._eventMaster.append(self._eventDict["FRAME"])
        self._eventMaster.append(self._eventDict["IMU_FRAME"])
        self._eventMaster.append(self._eventDict["DEFORMATION_FRAME"])
        self._eventMaster.start()

        self._buffer = bytearray(b'')
        self._readingThread = threading.Thread(target=self.__fillBuffer, daemon=True)

        self._port = None
        self._sock = None

    def open(self):
        """ Подключение к ресурсу source """
        if self._sourceConfig.sourceType is Sources.USB_TTL:
            self._port = serial.Serial(self._sourceConfig.portName, self._sourceConfig.baudrate)
        elif self._sourceConfig.sourceType is Sources.BLUETOOTH:
            # self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self._sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)  # on python 3.9
            self._sock.connect((self._sourceConfig.host, self._sourceConfig.port))
        else:
            raise IOError("Указан некорректный источник данных")

    def __fillBuffer(self):
        while not self.__exit:
            if self._sourceConfig.sourceType is Sources.USB_TTL:
                self._buffer.extend(self._port.read(20))
            elif self._sourceConfig.sourceType is Sources.BLUETOOTH:
                self._buffer.extend(self._sock.recv(1024))
            else:
                raise IOError("Не указан источник данных")

    def __readPackage(self):
        """ прочитать сообщение с ресурса """
        try:
            #print("1: ", self._buffer)
            startInd = self._buffer.index(proto.protocolConfig["startBytes"])
            del self._buffer[:startInd]
            if startInd != 0:
                print("В процессе чтения было отброшено: %d байт", startInd)
            #print("2: ", self._buffer, startInd, )
            frame = self._buffer[len(proto.protocolConfig["startBytes"]):]
            if len(frame) < proto.headSize:
                return
            #print("3: ", frame)
            #print("4: ", frame[:proto.headSize])
            desc, crc = struct.unpack(proto.headFormat, frame[:proto.headSize])
            frame = frame[proto.headSize:]
            #print("5: ", desc, crc)
            fmt = proto.protocolFormatDescription[desc]
            #print("6: ", fmt)
            packageSize = struct.calcsize(fmt)
            #print("7: ", packageSize)
            if len(frame) < packageSize:
                return
            #print("8: ", frame[:packageSize])
            data = struct.unpack(fmt, frame[:packageSize])
            del self._buffer[: len(proto.protocolConfig["startBytes"]) + proto.headSize + packageSize]
            #print("9: ", self._buffer)
            if proto.check(crc, data):
                self.__pushHandlers((desc, crc), data)
            else:
                print("В процессе чтения был отброшен пакет")
        except ValueError:
            return

    def __pushHandlers(self, head, data):
        self._eventDict["FRAME"].push(head, data)
        if head[0] == 0:  # если формат данных
            self._eventDict["IMU_FRAME"].push(data)
        elif head[0] == 1:
            self._eventDict["DEFORMATION_FRAME"].push(data)

    def connect(self, toEvent, foo):  # ф-ия подключения обработчика события по имени события
        event = self._eventDict.get(toEvent)
        if not event:  # если в словаре событий нет такого события - ошибка
            raise eventmaster.EventError(toEvent + ": There is no such event")
        event.connect(foo)

    def run(self):
        self._readingThread.start()
        while not self.__exit:
            self.__readPackage()

    def exit(self):
        self.__exit = True
        if self._sourceConfig.sourceType is Sources.USB_TTL:
            self._port.close()
        elif self._sourceConfig.sourceType is Sources.BLUETOOTH:
            self._sock.close()

    def newFrameDecorator(self, frame):
        """ decorator """

        def wrapper(*args, **kwargs):
            frame(*args, **kwargs)

        return wrapper

    def imuFrameDecorator(self, frame):
        """ decorator """

        def wrapper(*args, **kwargs):
            frame(*args, **kwargs)

        return wrapper

    def deformationFrameDecorator(self, frame, ):
        """ decorator """

        def wrapper(*args, **kwargs):
            frame(*args, **kwargs)

        return wrapper


if __name__ == '__main__':
    glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM7", baudrate=115200))


    @glove.imuFrameDecorator
    def imuFrame(data):
        pass
        #print("IMU data: ", data)
        #time.sleep(1)


    @glove.deformationFrameDecorator
    def deformationFrame(data):
        pass
        #print("deformation data: ", data)


    glove.connect("FRAME", glove.newFrameDecorator(lambda head, data: print(len(glove._buffer))#print("FRAME:", data)
                                                   ))
    glove.connect("IMU_FRAME", imuFrame)
    glove.connect("DEFORMATION_FRAME", deformationFrame)
    glove.open()
    glove.start()

    time.sleep(10)
    glove.exit()
