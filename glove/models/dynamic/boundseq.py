import pickle
import matplotlib.pyplot as plt
import numpy as np


class BoundingSequencesModel:
    def __init__(self, rules):
        self._rules = rules

        with open(self._rules["boundSecPath"], 'rb') as f:
            self._x, self._bounds = pickle.load(f)

    def reset(self):
        pass

    def update(self, frame):
        pass

    def classify(self, scope):
        results = []
        for i, dim in enumerate(self._bounds):
            res = ((scope.data["seq"][i] >= dim[0]) & (scope.data["seq"][i] <= dim[1]))
            results.append(res.sum() / len(self._x))
        return sum(results) / len(results)


if __name__ == '__main__':
    test = {
        "name": "bsmtest",
        "boundSecPath": "../../../dataprocessing/data/bound/bsmtest.pickle"
    }

    with open(test["boundSecPath"], 'rb') as f:
        x, bounds = pickle.load(f)

    base = [0, 1, 2, 2, 1, 0, -1, -2, -1, 0, 1, 2]
    base = np.interp(x, np.linspace(0, 1, len(base)), base)
    tests = []

    for seqInd in range(3):
        seq = []
        for i in range(len(base)):
            seq.append(base[i] + (np.random.random() - 0.5) * 1.9)
        tests.append(np.array(seq))

    tests[0] = tests[0]
    tests[1] = tests[1] * 5
    tests[2] = tests[2] * -10

    maxarg = np.max(np.abs(tests))
    tests = tests / maxarg

    class scope:
        data = {"seq": tests}

    bsm = BoundingSequencesModel(rules=test)
    result = bsm.classify(scope)
    print(result)

    fig, ax = plt.subplots()

    for dim in bounds:
        for dir in dim:
            ax.plot(x, dir)

    ax.plot(x, tests[0])
    ax.plot(x, tests[1])
    ax.plot(x, tests[2])

    plt.show()