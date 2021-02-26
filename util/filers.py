import math
import numpy as np
from numpy.linalg import norm


def LPFilterIterator(rawIn, oldFilteredVal, Kp):
    return (1 - Kp) * oldFilteredVal + Kp * rawIn


class MagvikFilter:
    """ фильтр Маджвика, скопирован из си, потом оптимизировать """
    def __init__(self, beta=1):
        self.beta = beta
        self._q = np.array([1, 0, 0, 0])

    def reset(self):
        """ Сброс фильтра """
        self._q = np.array([1, 0, 0, 0])

    def getQuat(self):
        return self._q

    def update(self, ax, ay, az, wx, wy, wz, dt):
        q = self._q

        gyroscope = np.array([wx, wy, wz], dtype=float).flatten()
        accelerometer = np.array([ax, ay, az], dtype=float).flatten()

        if norm(accelerometer) is 0:
            raise ValueError("accelerometer is zero")
        accelerometer /= norm(accelerometer)

        f = np.array([
            2 * (q[1] * q[3] - q[0] * q[2]) - accelerometer[0],
            2 * (q[0] * q[1] + q[2] * q[3]) - accelerometer[1],
            2 * (0.5 - q[1] ** 2 - q[2] ** 2) - accelerometer[2]
        ])
        j = np.array([
            [-2 * q[2], 2 * q[3], -2 * q[0], 2 * q[1]],
            [2 * q[1], 2 * q[0], 2 * q[3], 2 * q[2]],
            [0, -4 * q[1], -4 * q[2], 0]
        ])
        step = j.T.dot(f)
        step /= norm(step)  # normalise step magnitude

        qw = np.array([0, *gyroscope])
        wd = q[0] * qw[0] - q[1] * qw[1] - q[2] * qw[2] - q[3] * qw[3]
        xd = q[0] * qw[1] + q[1] * qw[0] + q[2] * qw[3] - q[3] * qw[2]
        yd = q[0] * qw[2] - q[1] * qw[3] + q[2] * qw[0] + q[3] * qw[1]
        zd = q[0] * qw[3] + q[1] * qw[2] - q[2] * qw[1] + q[3] * qw[0]

        qdot = np.array([wd, xd, yd, zd]) * 0.5 - self.beta * step.T

        # Integrate to yield quaternion
        q = q + qdot * float(dt)
        self._q = q / norm(q)

