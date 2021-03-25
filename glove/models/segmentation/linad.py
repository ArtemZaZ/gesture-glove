import math


_baseLocals = {"sqrt": math.sqrt,
               "_wrapper": None,
               "safepass": None,
               "isSafepass": False,
               "result": False}


class LinadModel:
    def __init__(self, rules=None):
        self._rules = rules
        self.reset()

    def reset(self):
        self._actualActivateRule = [False] * len(self._rules["activationList"])
        self._actualDeactivateRule = [False] * len(self._rules["deactivationList"])
        self._baseActivateRule = -1  # если используется safepass
        self._baseDeactivateRule = -1
        self._activateLocals = dict(_baseLocals)
        self._deactivateLocals = dict(_baseLocals)

        self._activateLocals["safepass"] = self.__activateSafepass
        self._deactivateLocals["safepass"] = self.__deactivateSafepass

        self._activateLocals["_wrapper"] = self.__activateWrapper
        self._deactivateLocals["_wrapper"] = self.__deactivateWrapper

        self._isActivate = False
        self._isDeactivate = False

    def update(self, frame):
        self.__resetLocals(self._activateLocals)
        self.__resetLocals(self._deactivateLocals)

        self._activateLocals.update(frame)
        self._deactivateLocals.update(frame)

        for index, rule in enumerate(self._rules["activationList"]):
            if self._baseActivateRule >= index:
                continue

            exec("_wrapper({rule})".format(rule=rule), self._activateLocals)

            if self._activateLocals["result"] is True:
                if self._activateLocals["isSafepass"] is True:
                    self._baseActivateRule = index
                self._actualActivateRule[index] = True

                if False not in self._actualActivateRule:
                    self._isActivate = True
            else:
                self._actualActivateRule = [True]*index + [False]*(len(self._actualActivateRule) - index)
                self._isActivate = False
                break

        for index, rule in enumerate(self._rules["deactivationList"]):
            if self._baseDeactivateRule >= index:
                continue

            exec("_wrapper({rule})".format(rule=rule), self._deactivateLocals)

            if self._deactivateLocals["result"] is True:
                if self._deactivateLocals["isSafepass"] is True:
                    self._baseDeactivateRule = index
                self._actualDeactivateRule[index] = True

                if False not in self._actualDeactivateRule:
                    self._isDeactivate = True
            else:
                self._actualDeactivateRule = [True]*index + [False]*(len(self._actualDeactivateRule) - index)
                self._isDeactivate = False
                break

    def isActivate(self):
        return self._isActivate

    def isDeactivate(self):
        return self._isDeactivate

    def __resetLocals(self, d):
        d["isSafepass"] = False
        d["result"] = False

    def __activateSafepass(self, rule):
        self._activateLocals["isSafepass"] = True
        return rule

    def __deactivateSafepass(self, rule):
        self._deactivateLocals["isSafepass"] = True
        return rule

    def __activateWrapper(self, rule):
        self._activateLocals["result"] = rule
        return rule

    def __deactivateWrapper(self, rule):
        self._deactivateLocals["result"] = rule
        return rule

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules):
        self._rules = rules

    @property
    def actualActivateRule(self):
        return self._actualActivateRule

    @property
    def actualDeactivateRule(self):
        return self._actualDeactivateRule


if __name__ == '__main__':
    test = {
        "name": "key",
        "activationList": [
            "x < 6",
            "safepass(x < 1)",
            "x > 3"
        ],
        "deactivationList": [
            "x < 6",
            "safepass(x < 1)",
            "x > 3"
        ]
    }

    linad = LinadModel(rules=test)
    """
    linad.update({"x": 2})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    linad.update({"x": 0})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    linad.update({"x": 1})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    linad.update({"x": 0})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    linad.update({"x": -2})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    linad.update({"x": 2})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    linad.update({"x": 4})
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    print(linad.isActivate())
    print(linad.isDeactivate())

    linad.reset()
    print("A: ", linad._actualActivateRule)
    print("D: ", linad._actualDeactivateRule)
    print(linad.isActivate())
    """
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
        print("A: ", linad._actualActivateRule)
        print("D: ", linad._actualDeactivateRule)
        print(linad.isActivate())



    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()



