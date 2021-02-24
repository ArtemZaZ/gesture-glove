from vispy import app, scene, gloo
import numpy as np


class ImuCanvas(scene.SceneCanvas):
    def __init__(self, keys='interactive', size=(1024, 768), **kwargs):
        super().__init__(keys=keys, size=size, **kwargs)
        self.unfreeze()
        self._grid = self.central_widget.add_grid(spacing=0, border_color='k', border_width=2, margin=0)
        self._viewbox = self._grid.add_view(row=0, col=1, camera='panzoom',
                                            border_color='k', margin=0,
                                            border_width=2, bgcolor=(0.99, 0.99, 0.99, 1))

        # add some axes
        self._xAxis = scene.AxisWidget(orientation='bottom', axis_label='X Axis',
                                       font_size=10, axis_color='k', tick_color='k',
                                       text_color='k', tick_label_margin=20,
                                       axis_label_margin=30)
        self._xAxis.stretch = (1, 0.1)
        self._grid.add_widget(self._xAxis, row=1, col=1)
        self._xAxis.link_view(self._viewbox)
        self._yAxis = scene.AxisWidget(orientation='left', axis_label='Y Axis',
                                       font_size=10, axis_color='k', tick_color='k',
                                       text_color='k')
        self._yAxis.stretch = (0.1, 1)
        self._grid.add_widget(self._yAxis, row=0, col=0)
        self._yAxis.link_view(self._viewbox)

        self._gridLines = scene.GridLines(color=(0, 0, 0, 1), parent=self._viewbox.scene)

        self._xLine = scene.Line(color='r', width=2, parent=self._viewbox.scene)
        self._yLine = scene.Line(color='b', width=2, parent=self._viewbox.scene)
        self._zLine = scene.Line(color='g', width=2, parent=self._viewbox.scene)

        self._gridLines.set_gl_state('translucent', cull_face=False)
        self._xLine.set_gl_state(depth_test=False)
        self._yLine.set_gl_state(depth_test=False)
        self._zLine.set_gl_state(depth_test=False)

        self._pointNum = 3000
        self._timeLine = 5.0
        self._xAxisLim = [0., self._timeLine]
        self._yAxisLim = [-1., 1.]

        self._xPos = np.array([[0, 0],], dtype=np.float32)  # np.zeros((self._pointNum, 2), dtype=np.float32)
        self._yPos = np.array([[0, 0],], dtype=np.float32)
        self._zPos = np.array([[0, 0],], dtype=np.float32)

        self.freeze()
        self.show()

    def addPoints(self, x, y, z):
        self._xPos = np.append(self._xPos, np.array([x]), axis=0)
        self._yPos = np.append(self._yPos, np.array([y]), axis=0)
        self._zPos = np.append(self._zPos, np.array([z]), axis=0)

        ymax = np.max([np.max(self._xPos[-self._pointNum:, 1]),
                      np.max(self._yPos[-self._pointNum:, 1]),
                      np.max(self._zPos[-self._pointNum:, 1])])

        ymin = np.min([np.min(self._xPos[-self._pointNum:, 1]),
                      np.min(self._yPos[-self._pointNum:, 1]),
                      np.min(self._zPos[-self._pointNum:, 1])])
        self._yAxisLim = [ymin, ymax]

        xmax = self._xPos[-1, 0]
        if xmax < self._timeLine:
            xmax = self._timeLine
        xmin = xmax - self._timeLine
        self._xAxisLim = [xmin, xmax]

    def updateData(self):
        self._xLine.set_data(pos=self._xPos[-self._pointNum:])
        self._yLine.set_data(pos=self._yPos[-self._pointNum:])
        self._zLine.set_data(pos=self._zPos[-self._pointNum:])

        self._viewbox.camera.set_range(x=self._xAxisLim, y=self._yAxisLim)
        self.update()


if __name__ == '__main__':
    import sys
    count = 0

    canvas = ImuCanvas(bgcolor='w')

    def addPoints(ev):
        global count
        x, y, z, = np.random.random(size=3)
        x *= 1
        y *= 2
        z *= 3
        canvas.addPoints([count, x], [count, y], [count, z])
        count += 0.02
        canvas.updateData()

    timer = app.Timer()
    timer.connect(addPoints)
    timer.start(0)

    if sys.flags.interactive != 1:
        app.run()
