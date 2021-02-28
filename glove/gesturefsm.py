
class GestureStates:
    NotActivated = 0
    Activated = 1
    Deactivated = 2


class GestureFsm:
    def __init__(self, segmentation, dynamicModel=None, dynamicScope=None, handler=None):
        self._state = GestureStates.NotActivated
        self._segmentationModel = segmentation
        self._dynamicScope = dynamicScope
        self._dynamicModel = dynamicModel
        self._raiseHandler = handler

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
            self._raiseHandler(self._dynamicModel.classify(self._dynamicScope))
            self._dynamicScope.reset()
            self._dynamicModel.reset()
            self._state = GestureStates.NotActivated

