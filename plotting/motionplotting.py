import time
import vispy.scene
import numpy as np
from vispy import scene, app
from vispy.scene import visuals
from vispy.util.quaternion import Quaternion
from vispy.visuals.transforms import MatrixTransform
from vispy.visuals import LinePlotVisual


class MotionPlotting(scene.SceneCanvas):
    def __init__(self, keys='interactive', size=(1024, 768), **kwargs):
        super().__init__(keys=keys, size=size, **kwargs)
        self.unfreeze()
        self._viewbox = self.central_widget.add_view(camera='turntable')
        self._baseAxis = visuals.XYZAxis(parent=self._viewbox.scene, width=5)
        self._gridLines = visuals.GridLines()
        self._viewbox.add(self._gridLines)

        self._cubeAxis = visuals.XYZAxis(parent=self._viewbox.scene, width=5)

        Plot3D = scene.visuals.create_visual_node(LinePlotVisual)
        self._plot = Plot3D(([0], [0], [0]), width=4.0, color='y',
                            edge_color='w', symbol='x',
                            face_color=(0.2, 0.2, 1, 0.8),
                            parent=self._viewbox.scene)
        self._xPos = np.array([0], dtype=np.float32)
        self._yPos = np.array([0], dtype=np.float32)
        self._zPos = np.array([0], dtype=np.float32)

        self._cube = visuals.Cube(parent=self._viewbox.scene,
                                  color=(0.5, 0.5, 1, 0.5),
                                  edge_color=(0.6, 0.2, 0.8, 1))

        self._transform = MatrixTransform()
        self._cube.transform = self._transform
        self._cubeAxis.transform = self._transform

        self.freeze()
        self.show()

    def transformCube(self, t, q):
        quaternion = Quaternion(*q)
        self._transform.reset()
        self._transform.matrix = quaternion.get_matrix()
        self._transform.translate(t)

        x, y, z = t
        self._xPos = np.append(self._xPos, x)
        self._yPos = np.append(self._yPos, y)
        self._zPos = np.append(self._zPos, z)
        self._plot.set_data((self._xPos.transpose(),
                             self._yPos.transpose(),
                             self._zPos.transpose()),
                            symbol=None)


if __name__ == '__main__':
    import sys
    mp = MotionPlotting()
    q1 = Quaternion()
    q2 = Quaternion()
    y = 0
    p = 0
    tx = 0
    ty = 0
    tz = 0
    signx = -1
    signy = -1
    signz = -1

    def update(ev):
        global y, p, tx, ty, tz, q1, q2, signx, signy, signz
        q1 = Quaternion.create_from_axis_angle(y, 0, 0, 1, degrees=True)
        q2 = Quaternion.create_from_axis_angle(p, 0, 1, 0, degrees=True)
        q = q1*q2
        mp.transformCube((tx, ty, tz), (q.w, q.x, q.y, q.z))
        mp.update()
        y += 1
        p += 3
        tx += signx*0.08
        ty += signy*0.05
        tz += signy*0.02
        if abs(tx) > 3:
            signx *= -1
        if abs(ty) > 3:
            signy *= -1
        if abs(tz) > 3:
            signz *= -1

    timer = app.Timer()
    timer.connect(update)
    timer.start(0)

    if sys.flags.interactive != 1:
        app.run()
