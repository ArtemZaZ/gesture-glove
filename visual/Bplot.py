import pickle

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

data = pickle.load(open("triangle(4).seq", 'rb'))
seq = data["seq"]
t, sx, sy, sz = seq
t = np.array(t) - t[0]
bounds = data["bounds"]
x = np.linspace(0, 1, 1000)


"""
plt.plot(t, sx, 'r:')
plt.plot(t, sy, 'g:')
plt.plot(t, sz, 'b:')

for i, dim in enumerate(bounds):
    color = ['r', 'g', 'b']
    for dir in dim:
        plt.plot(x, dir, color[i])

plt.show()
"""

fig, ax = plt.subplots()
ax.set_ylabel('$S, м$')
ax.set_xlabel('$t, с$')
ax.plot([0, 1.4], [0, 0], 'k:')

linesx, = ax.plot(t, sx, 'r', label="$S_x$")
linesy, = ax.plot(t, sy, 'g', label="$S_y$")
linesz, = ax.plot(t, sz, 'b', label="$S_z$")

frames = [[t[i], sx[i], sy[i], sz[i]] for i in range(len(t))]
ax.legend()


def animate(i):
    global linesx, linesy, linesz
    linesx.set_data(t[:i], sx[:i])
    linesy.set_data(t[0:i], sy[0:i])
    linesz.set_data(t[0:i], sz[0:i])
    return linesx, linesy, linesz

# create animation using the animate() function with no repeat
myAnimation = animation.FuncAnimation(fig, animate, interval=10, blit=True, save_count=len(t)+5)

# save animation at 30 frames per second
myAnimation.save('../triangleplot.gif', writer='pillow', fps=30)
plt.show()

fig1 = plt.figure()

ax_1 = fig1.add_subplot(3, 1, 1)
ax_1.set(xlabel="points", ylabel="$\Delta{S_x}/S_{max}$")
ax_1.plot([0, 1.0], [0, 0], 'k:')
ax_1.set_ylim((-1.1, 1.1))
ax_2 = fig1.add_subplot(3, 1, 2)
ax_2.set(xlabel="points", ylabel="$\Delta{S_y}/S_{max}$")
ax_2.plot([0, 1.0], [0, 0], 'k:')
ax_2.set_ylim((-1.1, 1.1))
ax_3 = fig1.add_subplot(3, 1, 3)
ax_3.set(xlabel="points", ylabel="$\Delta{S_z}/S_{max}$")
ax_3.plot([0, 1.0], [0, 0], 'k:')
ax_3.set_ylim((-1.1, 1.1))

ax_1.plot(x, bounds[0][0], 'r', label="$m_x | M_x$")
ax_1.plot(x, bounds[0][1], 'r')
ax_2.plot(x, bounds[1][0], 'g', label="$m_y | M_y$")
ax_2.plot(x, bounds[1][1], 'g')
ax_3.plot(x, bounds[2][0], 'b', label="$m_z | M_z$")
ax_3.plot(x, bounds[2][1], 'b')

ax_1.legend()
ax_2.legend()
ax_3.legend()
plt.draw()
plt.pause(1)

t = np.array(t) - t[0]
t = t / t[-1]
sx = np.interp(x, t, sx)
sy = np.interp(x, t, sy)
sz = np.interp(x, t, sz)
seq = np.array([sx, sy, sz])
maxarg = np.amax(np.abs(seq))
seq = seq / maxarg
sx, sy, sz = seq

ax_1.plot(x, sx, 'r:', label='gesture_x')
ax_2.plot(x, sy, 'g:', label='gesture_y')
ax_3.plot(x, sz, 'b:', label='gesture_z')
ax_1.legend()
ax_2.legend()
ax_3.legend()


fig2, ax = plt.subplots()
ax.set(xlabel="points", ylabel="$\Delta{S}/S_{max}$")
ax.plot([0, 1.0], [0, 0], 'k:')
ax.set_ylim((-1.1, 1.1))
ax.plot(x, bounds[0][0], 'r', linewidth=3, label="$m_x | M_x$")
ax.plot(x, bounds[0][1], 'r', linewidth=3)
ax.plot(x, bounds[1][0], 'g', linewidth=3, label="$m_y | M_y$")
ax.plot(x, bounds[1][1], 'g', linewidth=3)
ax.plot(x, bounds[2][0], 'b', linewidth=3, label="$m_z | M_z$")
ax.plot(x, bounds[2][1], 'b', linewidth=3)
ax.legend()

plt.draw()
plt.pause(1)

ax.plot(x, sx, 'r:', linewidth=3, label='$gesture_x$')
ax.plot(x, sy, 'g:', linewidth=3, label='$gesture_y$')
ax.plot(x, sz, 'b:', linewidth=3, label='$gesture_z$')
plt.text(0.66, 0.75, r'$match=0.98$', fontsize=16)
ax.legend()

plt.show()
