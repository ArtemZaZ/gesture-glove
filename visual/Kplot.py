import random
import time
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import mode

lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

X = np.linspace(-5, 5, 1000)
G = np.exp(-((X - 0) / 1) ** 2)
dG2 = np.gradient(np.gradient(G))
fig = plt.figure()
ax = fig.gca()
ax.plot(X, G, 'r', label='$f(t)$')
ax.plot(X, dG2*1000, 'b', label='$K(f(t))\cdot10^{3}$')
ax.legend()
ax.plot([-5, 5], [0, 0], 'k:')
ax.set_ylabel('Y')
ax.set_xlabel('X')

#############################
N = 10
a = -5
b = 5
Q = 1000
step = abs(b-a) / N
X = np.linspace(a, b, Q)
G = np.exp(-((X - 0) / 1) ** 2)
dG2 = np.gradient(np.gradient(G))
mbarData = [np.abs(np.mean(l)) for l in lol(dG2*1000, Q//N)]
mmData = [max(np.abs(l))-np.abs(np.mean(l)) for l in lol(dG2*1000, Q//N)]

fig = plt.figure()
ax = fig.gca()
r1 = ax.bar(np.linspace(a, b-step, N), mbarData, width=step/2, color='y', alpha=0.8, align='edge', label='$|\overline{K}|\cdot10^{3}$')
r2 = ax.bar(np.linspace(a+step/2, b-step/2, N), mmData, width=step/2, color='g', alpha=0.8, align='edge', label='$(|K|_{max}-|\overline{K}|)\cdot10^{3}$')
ax.plot(X, G, 'r', label='$f(t)$')
ax.plot(X, dG2*1000, 'b', label='$K(f(t))\cdot10^{3}$')
ax.legend()
ax.plot([a, b], [0, 0], 'k:')
for i in range(N+1):
    ax.plot([a + i*step, a + i*step], [min(min(G), min(dG2*1000)), max(max(G), max(dG2*1000))], 'k:')
ax.set_ylabel('Y')
ax.set_xlabel('X')


############################
X = np.linspace(0, 9, 1000)
Y = np.append(np.linspace(0, 1, 500), np.linspace(1, 0, 500))
dG2 = np.gradient(np.gradient(Y))
fig = plt.figure()
ax = fig.gca()
ax.plot(X, Y, 'r', label='$f(t)$')
ax.plot(X, dG2*1000, 'b', label='$K(f(t))\cdot10^{3}$')
ax.legend()
ax.plot([0, 9], [0, 0], 'k:')

##############################
N = 10
a = 0
b = 9
c = 1
Q = 1000
step = abs(b-a) / N
X = np.linspace(a, b, Q)
Y = np.append(np.linspace(0, c, Q//2), np.linspace(c, 0, Q//2))
dG2 = np.gradient(np.gradient(Y))
mbarData = [np.abs(np.mean(l)) for l in lol(dG2*1000, Q//N)]
mmData = [max(np.abs(l))-np.abs(np.mean(l)) for l in lol(dG2*1000, Q//N)]

fig = plt.figure()
ax = fig.gca()
r1 = ax.bar(np.linspace(a, b-step, N), mbarData, width=step/2, color='y', alpha=0.8, align='edge', label='$|\overline{K}|\cdot10^{3}$')
r2 = ax.bar(np.linspace(a+step/2, b-step/2, N), mmData, width=step/2, color='g', alpha=0.8, align='edge', label='$(|K|_{max}-|\overline{K}|)\cdot10^{3}$')
ax.plot(X, Y, 'r', label='$f(t)$')
ax.plot(X, dG2*1000, 'b', label='$K(f(t))\cdot10^{3}$')
ax.legend()
ax.plot([a, b], [0, 0], 'k:')
for i in range(N+1):
    ax.plot([a + i*step, a + i*step], [min(min(Y), min(dG2*1000)), -min(min(Y), min(dG2*1000))], 'k:')
ax.set_ylabel('Y')
ax.set_xlabel('X')

plt.show()
