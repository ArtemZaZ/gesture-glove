import sys

from vispy import scene, app
from vispy.scene import Text


class LinadCanvas:
    def __init__(self, linad, view=(True, True), keys='interactive', size=(1024, 400), bgcolor='#e0e0e0', **kwargs):
        self._model = linad
        self._view = view

        self._activationRules = self._model.rules["activationList"]
        self._deactivationRules = self._model.rules["deactivationList"]
        rows = (len(self._activationRules), len(self._deactivationRules))

        self._widgets = {"service": [], "a_rules": [], "d_rules": [], "a_result": None, "d_result": None}
        self._canvas = scene.SceneCanvas(keys=keys, size=size, bgcolor=bgcolor, **kwargs)
        self._grid = self._canvas.central_widget.add_grid()

        endrow = max(rows) + 1

        if self._view[0]:
            voidLabel = self._grid.add_widget(row=0, col=0, bgcolor="#e0e0e0", border_color='k')
            head = self._grid.add_widget(row=0, col=1, col_span=5, bgcolor="#e0e0e0", border_color='k')
            Text("activation", parent=head, color='black')
            self._widgets["service"].append(head)
            for row in range(rows[0]):
                widget = self._grid.add_widget(row=row + 1, col=1, col_span=5, bgcolor="#ffbebe", border_color='k')
                self._widgets["a_rules"].append(widget)
                Text(self._activationRules[row], parent=widget, color='black')

                label = self._grid.add_widget(row=row + 1, col=0, bgcolor="#e0e0e0", border_color='k')
                Text(str(row + 1), parent=label, color='black')
                self._widgets["service"].append(label)

            result = self._grid.add_widget(row=endrow, col=1, col_span=5, bgcolor="#ff2000", border_color='k')
            Text("result", parent=result, color='black')
            self._widgets.update({"a_result": result})

        if self._view[1]:
            voidLabel = self._grid.add_widget(row=0, col=6, bgcolor="#e0e0e0", border_color='k')
            head = self._grid.add_widget(row=0, col=7, col_span=5, bgcolor="#e0e0e0", border_color='k')
            Text("deactivation", parent=head, color='black')
            self._widgets["service"].append(head)
            for row in range(rows[1]):
                widget = self._grid.add_widget(row=row + 1, col=7, col_span=5, bgcolor="#e0e0e0", border_color='k')
                self._widgets["d_rules"].append(widget)
                Text(self._deactivationRules[row], parent=widget, color='black')

                label = self._grid.add_widget(row=row + 1, col=6, bgcolor="#e0e0e0", border_color='k')
                Text(str(row + 1), parent=label, color='black')
                self._widgets["service"].append(label)

            result = self._grid.add_widget(row=endrow, col=7, col_span=5, bgcolor="#ff2000", border_color='k')
            self._widgets.update({"d_result": result})

        self._canvas.update()
        self._canvas.show()

    def update(self):
        aar = self._model.actualActivateRule
        adr = self._model.actualDeactivateRule

        for i, widget in enumerate(self._widgets["a_rules"]):
            text = widget.children[0]
            text.pos = widget.size[0] // 2, widget.size[1] // 2

            if aar[i] is True:
                widget.bgcolor = "#d5e8d5"
            else:
                widget.bgcolor = "#ffbebe"

        for i, widget in enumerate(self._widgets["d_rules"]):
            text = widget.children[0]
            text.pos = widget.size[0] // 2, widget.size[1] // 2

            if adr[i] is True:
                widget.bgcolor = "#d5e8d5"
            else:
                widget.bgcolor = "#ffbebe"

        for widget in self._widgets["service"]:
            text = widget.children[0]
            text.pos = widget.size[0] // 2, widget.size[1] // 2

        try:
            widget = self._widgets["a_result"]
            text = widget.children[0]
            text.pos = widget.size[0] // 2, widget.size[1] // 2

            if self._model.isActivate():
                widget.bgcolor = "#00a000"
            else:
                self._widgets["a_result"].bgcolor = "#ff2000"

            widget = self._widgets["d_result"]
            text = widget.children[0]
            text.pos = widget.size[0] // 2, widget.size[1] // 2

            if self._model.isDeactivate():
                self._widgets["d_result"].bgcolor = "#00a000"
            else:
                self._widgets["d_result"].bgcolor = "#ff2000"
        except:
            pass

        self._canvas.update()


if __name__ == '__main__' and sys.flags.interactive == 0:
    from glove.models.segmentation.linad import LinadModel
    test = {
        "name": "key",
        "activationList": [
            "x < 6",
            "safepass(x < 1)",
            "x > 3"
        ],
        "deactivationList": [
            "x > 6",
            "safepass(x < 1)",
        ]
    }

    linad = LinadModel(rules=test)
    vis = LinadCanvas(linad, view=(True, False))

    def on_timer(event):
        vis.update()

    timer = app.Timer(0.2, connect=on_timer, start=True)

    from pynput import keyboard

    def on_press(key):
        try:
            pass
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        if key == keyboard.Key.space:
            linad.reset()
            return None
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        x = int(key.char)
        print(x)
        linad.update({"x": x})


    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    app.run()

