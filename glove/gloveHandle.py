import socket
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

        self._newFrameLock = False  # нужны, если включена блокировка потоков (nonBlocking=False)
        self._imuFrameLock = False
        self._deformationFrameLock = False

        self._port = None
        self._sock = None

    def newFrameDecorator(self, frame):
        """ decorator """

        def wrapper(*args, **kwargs):
            frame(*args, **kwargs)
            self._newFrameLock = False

        return wrapper

    def imuFrameDecorator(self, frame):
        """ decorator """

        def wrapper(*args, **kwargs):
            frame(*args, **kwargs)
            self._imuFrameLock = False

        return wrapper

    def deformationFrameDecorator(self, frame, ):
        """ decorator """

        def wrapper(*args, **kwargs):
            frame(*args, **kwargs)
            self._deformationFrameLock = False

        return wrapper

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

    def __readByte(self):
        """ прочитать байт с ресурса """
        if self._sourceConfig.sourceType is Sources.USB_TTL:
            return self._port.read()
        elif self._sourceConfig.sourceType is Sources.BLUETOOTH:
            return self._sock.recv(1)
        else:
            raise IOError("Не указан источник данных")

    def __readByteArray(self, size):
        if self._sourceConfig.sourceType is Sources.USB_TTL:
            return self._port.read(size)
        elif self._sourceConfig.sourceType is Sources.BLUETOOTH:
            out = b''
            for i in range(size):
                out += self._sock.recv(1)
            return out
        else:
            raise IOError("Не указан источник данных")

    def __readPackage(self):
        """ прочитать сообщение с ресурса """

        head, data = proto.readPackage(self.__readByteArray)

        if head[0] == 0:  # если формат данных
            self._eventDict["IMU_FRAME"]._f(data)
        elif head[0] == 1:
            self._eventDict["DEFORMATION_FRAME"]._f(data)


    def connect(self, toEvent, foo):  # ф-ия подключения обработчика события по имени события
        event = self._eventDict.get(toEvent)
        if not event:  # если в словаре событий нет такого события - ошибка
            raise eventmaster.EventError(toEvent + ": There is no such event")
        event.connect(foo)

    def run(self):
        while not self.__exit:
            self.__readPackage()

    def exit(self):
        self.__exit = True
        if self._sourceConfig.sourceType is Sources.USB_TTL:
            self._port.close()
        elif self._sourceConfig.sourceType is Sources.BLUETOOTH:
            self._sock.close()


if __name__ == '__main__':
    glove = GloveHandle(SourceConfig(Sources.USB_TTL, portName="COM7", baudrate=115200), nonBlocking=True)


    @glove.imuFrameDecorator
    def imuFrame(data):
        print("IMU data: ", data)
        #time.sleep(1)


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