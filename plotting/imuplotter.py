# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class ImuPlotter:
    def __init__(self, sampleInterval=0.002, timeWindow=5.):
        self.app = QtGui.QApplication([])
        self._sampleInterval = sampleInterval
        self._timeWindow = timeWindow

        pg.setConfigOption('background', 'w')
        self._win = pg.GraphicsWindow(title="Test")  # creates a window
        self._plot = self._win.addPlot(title="Realtime plot",
                                       background='w')  # creates empty space for the plot in the window
        self._plot.showGrid(x=True, y=True)
        self._plot.setLabel('left', 'accel', 'm*s^2')
        self._plot.setLabel('bottom', 'time', 's')

        self._xLine = self._plot.plot(pen=pg.mkPen(width=1, color='r'))  # create an empty "plot" (a curve to plot)
        self._yLine = self._plot.plot(pen=pg.mkPen(width=1, color='b'))  # create an empty "plot" (a curve to plot)
        self._zLine = self._plot.plot(pen=pg.mkPen(width=1, color='g'))  # create an empty "plot" (a curve to plot)

        self._windowWidth = int(timeWindow/sampleInterval)  # width of the window displaying the curve

        self._xPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._yPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._zPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._time = linspace(-self._timeWindow, 0, self._windowWidth)

    def addPoint(self, x, y, z, t):
        self._xPos[: -1] = self._xPos[1:]
        self._yPos[: -1] = self._yPos[1:]
        self._zPos[: -1] = self._zPos[1:]
        self._time[: -1] = self._time[1:]

        self._xPos[-1] = x
        self._yPos[-1] = y
        self._zPos[-1] = z
        self._time[-1] = t

        self._xLine.setData(self._time, self._xPos)
        self._yLine.setData(self._time, self._yPos)
        self._zLine.setData(self._time, self._zPos)

    def update(self):
        self.app.processEvents()

    def exit(self):
        self.app.exec_()


if __name__ == '__main__':
    import time
    plotter = ImuPlotter()
    t = 0
    for i in range(2500):
        x = np.random.randn(1)[0]
        print(x)
        y = np.random.randn(1)[0]
        z = np.random.randn(1)[0]
        plotter.addPoint(x, y, z, t)
        plotter.update()
        t += 0.002
        time.sleep(0.002)

    plotter.exit()

