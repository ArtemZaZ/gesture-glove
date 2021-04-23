from scipy.stats import mode

import numpy as np


class MlcTemplateGenerator:
    def __init__(self, interpPoints=1000, part=10):
        self.__paramDict = {}
        self._part = part
        self._interpPoints = interpPoints
        self._rawSequences = []
        self._x = np.linspace(0.0, 1.0, self._interpPoints)

    def __keyGen(self):
        keys = []
        for i in range(self._part):
            keys.append("mean_Kx" + str(i))  # создаем список ключей
            keys.append("mean_Ky" + str(i))
            keys.append("mean_Kz" + str(i))
            keys.append("abs_mean_Kx" + str(i))
            keys.append("abs_mean_Ky" + str(i))
            keys.append("abs_mean_Kz" + str(i))
            keys.append("max_abs_Kx" + str(i))
            keys.append("max_abs_Ky" + str(i))
            keys.append("max_abs_Kz" + str(i))
            keys.append("mode_Kx" + str(i))  # создаем список ключей
            keys.append("mode_Ky" + str(i))
            keys.append("mode_Kz" + str(i))
            keys.append("max_abs_abs_mean_Kx" + str(i))
            keys.append("max_abs_abs_mean_Ky" + str(i))
            keys.append("max_abs_abs_mean_Kz" + str(i))

        attributes = dict.fromkeys(keys)  # bиз списка ключей создаем словарь
        return attributes

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

    def getRawSeq(self):
        return self._rawSequences

    def getParam(self):
        params = []
        x, proc = self.getProcSeq()
        steps = [p * len(x) // self._part for p in range(self._part)]
        for seq in proc:
            self.__paramDict = self.__keyGen()
            scale = 1
            Kx = seq[0] * scale
            Ky = seq[1] * scale
            Kz = seq[2] * scale
            for p in range(self._part):
                sl = p * len(x) // self._part
                #print(sl, sl + len(x) // self._part)
                Kxsl = Kx[sl:sl + len(x) // self._part]
                Kysl = Ky[sl:sl + len(x) // self._part]
                Kzsl = Kz[sl:sl + len(x) // self._part]

                Kxsl_mode, _ = mode(Kxsl)
                Kysl_mode, _ = mode(Kysl)
                Kzsl_mode, _ = mode(Kzsl)

                Kxsl_mean = np.mean(Kxsl)
                Kysl_mean = np.mean(Kysl)
                Kzsl_mean = np.mean(Kzsl)

                Kxsl_abs_mean = np.abs(np.mean(Kxsl))
                Kysl_abs_mean = np.abs(np.mean(Kysl))
                Kzsl_abs_mean = np.abs(np.mean(Kzsl))

                Kxsl_max_abs = max(np.abs(Kxsl))
                Kysl_max_abs = max(np.abs(Kysl))
                Kzsl_max_abs = max(np.abs(Kzsl))

                Kxsl_max_abs_abs_mean = Kxsl_max_abs - np.abs(np.mean(Kxsl))
                Kysl_max_abs_abs_mean = Kysl_max_abs - np.abs(np.mean(Kysl))
                Kzsl_max_abs_abs_mean = Kzsl_max_abs - np.abs(np.mean(Kzsl))

                self.__paramDict["mean_Kx" + str(p)] = Kxsl_mean
                self.__paramDict["mean_Ky" + str(p)] = Kysl_mean
                self.__paramDict["mean_Kz" + str(p)] = Kzsl_mean

                self.__paramDict["abs_mean_Kx" + str(p)] = Kxsl_abs_mean
                self.__paramDict["abs_mean_Ky" + str(p)] = Kysl_abs_mean
                self.__paramDict["abs_mean_Kz" + str(p)] = Kzsl_abs_mean

                self.__paramDict["mode_Kx" + str(p)] = Kxsl_mode
                self.__paramDict["mode_Ky" + str(p)] = Kysl_mode
                self.__paramDict["mode_Kz" + str(p)] = Kzsl_mode

                self.__paramDict["max_abs_Kx" + str(p)] = Kxsl_max_abs
                self.__paramDict["max_abs_Ky" + str(p)] = Kysl_max_abs
                self.__paramDict["max_abs_Kz" + str(p)] = Kzsl_max_abs

                self.__paramDict["max_abs_abs_mean_Kx" + str(p)] = Kxsl_max_abs_abs_mean
                self.__paramDict["max_abs_abs_mean_Ky" + str(p)] = Kysl_max_abs_abs_mean
                self.__paramDict["max_abs_abs_mean_Kz" + str(p)] = Kzsl_max_abs_abs_mean

            params.append(self.__paramDict.copy())

        return steps, params
