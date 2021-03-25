# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class FlexPlotter:
    def __init__(self, sampleInterval=0.002, timeWindow=5.):
        self.app = QtGui.QApplication([])
        self._sampleInterval = sampleInterval
        self._timeWindow = timeWindow

        pg.setConfigOption('background', 'w')
        self._win = pg.GraphicsWindow(title="Test")  # creates a window
        self._plot = self._win.addPlot(title="",
                                       background='w')  # creates empty space for the plot in the window
        self._plot.showGrid(x=True, y=True)
        self._plot.setLabel('left', 'a, м/с^2')
        self._plot.setLabel('bottom', 't, с')

        self._firstLine = self._plot.plot(pen=pg.mkPen(width=4, color='r'))  # create an empty "plot" (a curve to plot)
        self._secondLine = self._plot.plot(pen=pg.mkPen(width=4, color='b'))  # create an empty "plot" (a curve to plot)
        self._thirdLine = self._plot.plot(pen=pg.mkPen(width=4, color='g'))  # create an empty "plot" (a curve to plot)
        self._fourthLine = self._plot.plot(pen=pg.mkPen(width=4, color='y'))  # create an empty "plot" (a curve to plot)
        self._fifthLine = self._plot.plot(pen=pg.mkPen(width=4, color='k'))  # create an empty "plot" (a curve to plot)

        self._windowWidth = int(timeWindow/sampleInterval)  # width of the window displaying the curve

        self._firstPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._secondPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._thirdPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._fourthPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._fifthPos = linspace(0, 0, self._windowWidth)  # create array that will contain the relevant time series
        self._time = linspace(-self._timeWindow, 0, self._windowWidth)

    def addPoint(self, first, second, third, fourth, fifth, t):
        self._firstPos[: -1] = self._firstPos[1:]
        self._secondPos[: -1] = self._secondPos[1:]
        self._thirdPos[: -1] = self._thirdPos[1:]
        self._fourthPos[: -1] = self._fourthPos[1:]
        self._fifthPos[: -1] = self._fifthPos[1:]
        self._time[: -1] = self._time[1:]

        self._firstPos[-1] = first
        self._secondPos[-1] = second
        self._thirdPos[-1] = third
        self._fourthPos[-1] = fourth
        self._fifthPos[-1] = fifth
        self._time[-1] = t

        self._firstLine.setData(self._time, self._firstPos)
        self._secondLine.setData(self._time, self._secondPos)
        self._thirdLine.setData(self._time, self._thirdPos)
        self._fourthLine.setData(self._time, self._fourthPos)
        self._fifthLine.setData(self._time, self._fifthPos)

    def update(self):
        self.app.processEvents()

    def exit(self):
        self.app.exec_()


if __name__ == '__main__':
    import time
    plotter = FlexPlotter()
    t = 0
    for i in range(2500):
        x = np.random.randn(1)[0]
        print(x)
        y = np.random.randn(1)[0]
        z = np.random.randn(1)[0]
        plotter.addPoint(x, y, z, x+z, y+z, t)
        plotter.update()
        t += 0.002
        time.sleep(0.002)

    plotter.exit()

