import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib
import matplotlib.pyplot as plt


class _FuzzySubModel:
    def __init__(self, owner):
        self._owner = owner
        self._isActivate = False
        self._isDeactivate = False

    def reset(self):
        pass

    def update(self, frame):
        pass

    def isActivate(self):
        return self._isActivate

    def isDeactivate(self):
        return self._isDeactivate


class FuzzyModel:
    def __init__(self, source):
        self._source = source


    def submodel(self, gestureName):
        return self