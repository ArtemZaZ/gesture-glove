
class GestureStates:
    NotActivated = 0
    Activated = 0
    Deactivated = 0


class GestureFsm:
    def __init__(self):
        self._state = GestureStates.NotActivated
        self._segmentationModel = None
        self._dynamicScope = None
        self._dynamicModel = None
        self._raiseHandler = None

    def update(self, frame):
        if self._state is GestureStates.NotActivated:
            self._segmentationModel.update(frame)

            if self._segmentationModel.isActivate():
                self._segmentationModel.reset()
                self._state = GestureStates.Activated

        elif self._state is GestureStates.Activated:
            self._dynamicScope.update(frame)
            self._segmentationModel.update(frame)

            if self._segmentationModel.isDeactivate():
                self._segmentationModel.reset()
                self._state = GestureStates.Deactivated

        elif self._state is GestureStates.Deactivated:
            self._dynamicModel.update(frame)
            self._raiseHandler(self._dynamicModel.classificate())
            self._dynamicScope.reset()
            self._dynamicModel.reset()
            self._state = GestureStates.NotActivated

