import struct

protocolConfig = {
    "startBytes": b'\xAA\xAA',
    "checksum": "crc8",
    "formatDesc": 'B',      # дескриптор пакета, определяет, как будет читаться пакет
    "formatChecksum": 'B',  # 1 байт
}

protocolFormatDescription = {   # описание форматов пакетов по дескриптору
    0: '=6hh',   #
    1: '=6hh'    #
}

headFormat = '=' + protocolConfig["formatDesc"] + protocolConfig["formatChecksum"]
headSize = struct.calcsize(headFormat)

"""
def readPackage(readArrFun):
    try:
        temp = bytearray(len(protocolConfig["startBytes"]))
        while temp != protocolConfig["startBytes"]:  # ищем вхождение
            temp.pop(0)
            temp += readArrFun(1)

        head = struct.unpack(_headFormat, readArrFun(_headSize))    # читаем заголовок
        fmt = protocolFormatDescription[head[0]]   # получаем пакет пакета
        data = struct.unpack(fmt, readArrFun(struct.calcsize(fmt)))     # читаем данные
        if check(head[1], data):    # проверяем данные
            return head, data
        else:
            return None
    except Exception as e:
        print("error proto: ", e.__repr__())
"""

def check(checksum, data):
    return True  # TODO: доделать

