import sys
import colorsys
from vispy import scene, app
from vispy.scene import Text
from vispy.io import read_png


class GloveCanvas:
    def __init__(self, keys='interactive', size=(400, 550), **kwargs):
        self._canvas = scene.SceneCanvas(keys=keys, size=size, **kwargs)
        self._view = self._canvas.central_widget.add_view()

        self._gloveImage = scene.visuals.Image(read_png("../plotting/img/glove.png"), interpolation='nearest',
                                               parent=self._view.scene, method='subdivide')

        self._thumb = Text("flex:\n0", pos=(104, 261), color='k', font_size=10, bold=True, parent=self._gloveImage)
        self._index = Text("flex:\n0", pos=(166, 171), color='k', font_size=10, bold=True, parent=self._gloveImage)
        self._middle = Text("flex:\n0", pos=(225, 171), color='k', font_size=10, bold=True, parent=self._gloveImage)
        self._ring = Text("flex:\n0", pos=(283, 171), color='k', font_size=10, bold=True, parent=self._gloveImage)
        self._little = Text("flex:\n0", pos=(342, 171), color='k', font_size=10, bold=True, parent=self._gloveImage)

        Text("yaw:  ", pos=(40, 400), color='b', font_size=10, bold=True, parent=self._gloveImage)
        Text("pitch:", pos=(40, 425), color='#00d200', font_size=10, bold=True, parent=self._gloveImage)
        Text("roll:   ", pos=(40, 450), color='r', font_size=10, bold=True, parent=self._gloveImage)

        self._yaw = Text("0", pos=(100, 400), color='b', font_size=10, bold=True, parent=self._gloveImage)
        self._pitch = Text("0", pos=(100, 425), color='#00d200', font_size=10, bold=True, parent=self._gloveImage)
        self._roll = Text("0", pos=(100, 450), color='r', font_size=10, bold=True, parent=self._gloveImage)

        self._canvas.show()

    def update(self, flex, angle):
        d = [0.4, 0]
        self._thumb.text = "flex:\n%s" % str(flex[0])
        self._thumb.color = colorsys.hsv_to_rgb((flex[0]/90)*(d[1]-d[0])+d[0], 0.93, 0.8)

        self._index.text = "flex:\n%s" % str(flex[1])
        self._index.color = colorsys.hsv_to_rgb((flex[1] / 90) * (d[1] - d[0]) + d[0], 0.93, 0.8)

        self._middle.text = "flex:\n%s" % str(flex[2])
        self._middle.color = colorsys.hsv_to_rgb((flex[2] / 90) * (d[1] - d[0]) + d[0], 0.93, 0.8)

        self._ring.text = "flex:\n%s" % str(flex[3])
        self._ring.color = colorsys.hsv_to_rgb((flex[3] / 90) * (d[1] - d[0]) + d[0], 0.93, 0.8)

        self._little.text = "flex:\n%s" % str(flex[4])
        self._little.color = colorsys.hsv_to_rgb((flex[4] / 90) * (d[1] - d[0]) + d[0], 0.93, 0.8)

        self._yaw.text = str(angle[0])
        self._pitch.text = str(angle[1])
        self._roll.text = str(angle[2])
        self._canvas.update()


if __name__ == '__main__' and sys.flags.interactive == 0:
    from numpy import random

    glove = GloveCanvas()

    def on_timer(event):
        glove.update(random.randint(0, 90, 5), random.randint(0, 360, 3))

    timer = app.Timer(0.1, connect=on_timer, start=True)
    app.run()
