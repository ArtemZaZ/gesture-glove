import math
import numpy as np


def LPFilterIterator(rawIn, oldFilteredVal, Kp):
    return (1 - Kp) * oldFilteredVal + Kp * rawIn


class MagvikFilter:
    """ фильтр Маджвика, скопирован из си, потом оптимизировать """
    def __init__(self, betta=0.9):
        self.betta = betta
        self._qw = 1
        self._qx = 0
        self._qy = 0
        self._qz = 0

    def reset(self):
        """ Сброс фильтра """
        self._qw = 1
        self._qx = 0
        self._qy = 0
        self._qz = 0

    def getAngle(self, q=None):
        if q is None:
            qw, qx, qy, qz = self._qw, self._qx, self._qy, self._qz
        else:
            qw, qx, qy, qz = q
        yaw = math.atan2(2 * (qw * qz + qx * qy), qx * qx + qw * qw - qz * qz - qy * qy) * (180 / math.pi)
        pitch = math.asin(2 * (qx * qz - qw * qy)) * (180 / math.pi)
        roll = math.atan2(2 * (qw * qx + qy * qz), qz * qz - qy * qy - qx * qx + qw * qw) * (180 / math.pi)
        return yaw, pitch, roll


    """
    def getAngle(self):
        qw, qx, qy, qz = self._qw, self._qx, self._qy, self._qz
        yaw = math.atan2(2 * (qx * qy - qw * qz), 2*qw * qw + 2*qx * qx - 1) * (180 / math.pi)
        pitch = - math.asin(2 * (qx * qz + qw * qy)) * (180 / math.pi)
        roll = math.atan2(2 * (qy * qz - qw * qx), 2*qw * qw + 2*qz * qz - 1) * (180 / math.pi)
        return yaw, pitch, roll
    """

    def getQuat(self):
        return np.array([self._qw, self._qx, self._qy, self._qz])

    def update(self, ax, ay, az, wx, wy, wz, dt):
        if (ax != 0) and (ay != 0) and (az != 0):
            qw, qx, qy, qz = self._qw, self._qx, self._qy, self._qz
            norm = (ax * ax + ay * ay + az * az) ** 0.5
            ax = ax / norm
            ay = ay / norm
            az = az / norm

            temp1 = qx * qx + qy * qy
            temp2 = qz * qz + qw * qw - 1 + 2 * temp1 + az

            qHatDotw = 4 * qw * temp1 + 2 * (qy * ax - qx * ay)
            qHatDotx = 4 * qx * temp2 - 2 * (qz * ax + qw * ay)
            qHatDoty = 4 * qy * temp2 + 2 * (qw * ax - qz * ay)
            qHatDotz = 4 * qz * temp1 - 2 * (qx * ax + qy * ay)

            norm = (qHatDotw * qHatDotw + qHatDotx * qHatDotx + qHatDoty * qHatDoty + qHatDotz * qHatDotz) ** 0.5
            qHatDotw /= norm
            qHatDotx /= norm
            qHatDoty /= norm
            qHatDotz /= norm

            qDotOmegaw = -0.5 * (qx * wx + qy * wy + qz * wz)
            qDotOmegax = 0.5 * (qw * wx + qy * wz - qz * wy)
            qDotOmegay = 0.5 * (qw * wy - qx * wz + qz * wx)
            qDotOmegaz = 0.5 * (qw * wz + qx * wy - qy * wx)

            qw += (qDotOmegaw - self.betta * qHatDotw) * dt
            qx += (qDotOmegax - self.betta * qHatDotx) * dt
            qy += (qDotOmegay - self.betta * qHatDoty) * dt
            qz += (qDotOmegaz - self.betta * qHatDotz) * dt

            norm = (qw * qw + qx * qx + qy * qy + qz * qz) ** 0.5
            qw /= norm
            qx /= norm
            qy /= norm
            qz /= norm

            self._qw = qw
            self._qx = qx
            self._qy = qy
            self._qz = qz
