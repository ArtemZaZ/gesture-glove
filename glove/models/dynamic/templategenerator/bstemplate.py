import numpy as np


class BsTemplateGenerator:
    def __init__(self, interpPoints=1000, delta=0.1):
        self._interpPoints = interpPoints
        self._delta = delta
        self._rawSequences = []
        self._x = np.linspace(0.0, 1.0, self._interpPoints)
        self._upLimit = None
        self._downLimit = None

    def fit(self, t, seqlist):
        self._rawSequences.append([np.array(t), np.array(seqlist)])

    def getProcSeq(self):
        procSeq = []
        for t, seq in self._rawSequences:
            t = t - t[0]  # нормализуем t
            t = t / t[-1]

            maxarg = np.amax(np.abs(seq))
            seq = seq / maxarg

            lseq = []
            for seqdim in seq:
                interpseq = np.interp(self._x, t, seqdim)
                lseq.append(interpseq)
            procSeq.append(lseq)

        return self._x, np.array(procSeq)

    def getBounds(self):
        bounds = []
        _, proc = self.getProcSeq()
        proc = proc.transpose(1, 2, 0)
        for dim in proc:
            up = []
            down = []
            for points in dim:
                down.append(min(points) - self._delta)
                up.append(max(points) + self._delta)
            bounds.append([down, up])
        return self._x, np.array(bounds)


if __name__ == '__main__':
    bstg = BsTemplateGenerator()

    base = [0, 1, 2, 2, 1, 0, -1, -2, -1, 0, 1, 2]
    data = []
    for seqInd in range(20):
        seq = []
        for i in range(len(base)):
            seq.append(base[i] + (np.random.random() - 0.5) * 1)
        data.append(seq)

    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pickle


    def plot(title, t, lseq):
        fig, ax = plt.subplots()
        for i in range(len(lseq)):
            ax.plot(t[i], lseq[i])
        ax.set(title=title)
        ax.grid()


    tb = np.linspace(0, 1, len(base))
    t = []

    data1 = np.array(data)
    data2 = data1 * 5
    data3 = data1 * -10

    for i in range(len(data)):
        scale = np.random.random() * 3
        offset = np.random.random() * 2
        tm = scale * tb + offset
        t.append(tm)
        bstg.fit(tm, [data1[i], data2[i], data3[i]])  ####################

    x, proc = bstg.getProcSeq()  ####################
    _, bounds = bstg.getBounds()    ##############

    #with open('../../../../dataprocessing/data/bound/bsmtest.pickle', 'xb') as f:
    #    pickle.dump([x, bounds], f)

    #### plotting ####
    ptx = np.array(list(x) * len(data) * 3)
    ptx.shape = (len(data) * 3, 1000)

    plseq = []
    for seq in proc:
        for seqdim in seq:
            plseq.append(seqdim)

    bds = []
    for dim in bounds:
        for dir in dim:
            bds.append(dir)

    bx = list(ptx[:6])

    ### test
    test = data3[0]
    tt = t[0]

    tt = tt - tt[0]  # нормализуем t
    tt = tt / tt[-1]

    maxarg = max(abs(test))
    test = test / maxarg

    bx.append(tt)
    bds.append(test)
    plot("raw", [*t, *t, *t], [*data1, *data2, *data3])
    plot("interp+norm", ptx, plseq)
    plot("bounds", bx, bds)

    plt.show()
