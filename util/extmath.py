import numpy as np
from numpy.linalg import norm
from numpy import cos, sin, pi
import math


def getRotationMatrix(axis=None, angle=0):  # Возвращает матрицу поворота в однородных координатах
    angle = angle / 180.0 * pi
    if axis == 'x':
        return np.array([[1, 0, 0],
                         [0, cos(angle), -sin(angle)],
                         [0, sin(angle), cos(angle)]])
    elif axis == 'y':
        return np.array([[cos(angle), 0, sin(angle)],
                         [0, 1, 0],
                         [-sin(angle), 0, cos(angle)]])
    elif axis == 'z':
        return np.array([[cos(angle), -sin(angle), 0],
                         [sin(angle), cos(angle), 0],
                         [0, 0, 1]])
    else:
        raise ValueError("parameter axis must be 'x', 'y', 'z' only")


def findOrthonormals(normal):
    orthoX = getRotationMatrix('x', 90)
    orthoY = getRotationMatrix('y', 90)
    w = orthoX @ normal
    dot = np.dot(normal, w)
    if abs(dot) > 0.6:
        w = orthoY @ normal
    w = w / norm(w)
    orthonormal1 = np.cross(normal, w)
    orthonormal1 = orthonormal1 / norm(orthonormal1)
    orthonormal2 = np.cross(normal, orthonormal1)
    orthonormal2 = orthonormal2 / norm(orthonormal2)
    return orthonormal1, orthonormal2


def getQuat(axis, angle):  # получение кватерниона из оси и угла(в радианах)
    w = np.cos(angle / 2)  # скалярная часть
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis * np.sin(angle / 2)  # векторная часть
    q = np.array([w, x, y, z])
    return q  # без нормировки


"""
def mulQuat(q1, q2):
    w = q1[0] * q2[0] - np.dot(q1[1:4], q2[1:4])
    x, y, z = q1[0] * q2[1:4] + q2[0] * q1[1:4] + np.cross(q1[1:4], q2[1:4])
    q = np.array([w, x, y, z])
    return q #/ norm(q)
"""


def mulQuat(q, oq):
    w = q[0] * oq[0] - q[1] * oq[1] - q[2] * oq[2] - q[3] * oq[3]
    x = q[0] * oq[1] + q[1] * oq[0] + q[2] * oq[3] - q[3] * oq[2]
    y = q[0] * oq[2] - q[1] * oq[3] + q[2] * oq[0] + q[3] * oq[1]
    z = q[0] * oq[3] + q[1] * oq[2] - q[2] * oq[1] + q[3] * oq[0]
    return np.array([w, x, y, z])


def invQuat(qv):
    qv = qv.copy()
    qv[1] = -qv[1]
    qv[2] = -qv[2]
    qv[3] = -qv[3]
    return qv  # / norm(qv)


def angleByVectors(v1, v2):
    return np.arccos(np.dot(v1, v2) / (norm(v1) * norm(v2)))


def angleFromQuat(q):
    qw, qx, qy, qz = q
    yaw = math.atan2(2 * (qw * qz + qx * qy), qx * qx + qw * qw - qz * qz - qy * qy) * (180 / math.pi)
    pitch = math.asin(2 * (qx * qz - qw * qy)) * (180 / math.pi)
    roll = math.atan2(2 * (qw * qx + qy * qz), qz * qz - qy * qy - qx * qx + qw * qw) * (180 / math.pi)
    return yaw, pitch, roll


def decompositionSwingTwist(q, direction):
    rot = q[1:4]  # rotation vector
    dot = np.dot(rot, direction)
    projection = dot * direction
    twist = np.array([q[0], *projection])
    twist = twist / norm(twist)
    swing = mulQuat(q, invQuat(twist))
    return swing, twist


def decompositionSwingTwist2(q, direction):
    qinv = invQuat(q)
    orthonormal1, orthonormal2 = findOrthonormals(direction)
    transformed = mulQuat(mulQuat(q, np.array([0, *orthonormal1])), qinv)[1:4]
    flattened = transformed - (np.dot(transformed, direction) * direction)
    flattened = flattened / norm(flattened)

    sign = np.dot(np.cross(orthonormal1, flattened), direction)
    sign = sign / abs(sign)
    twistAngle = sign * np.arccos(np.dot(orthonormal1, flattened))

    twist = getQuat(direction, twistAngle)
    swing = mulQuat(q, invQuat(twist))
    return swing, twist
