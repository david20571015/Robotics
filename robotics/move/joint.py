import itertools

import matplotlib.pyplot as plt
import numpy as np

from robotics import kinematics


def plot_joint(title: str, timestamp: np.ndarray, values: np.ndarray):
    fig, ax = plt.subplots(3, 2, figsize=(10, 8))

    ax[1, 0].set_ylabel(title)
    ax[2, 0].set_xlabel('time(s)')
    ax[2, 1].set_xlabel('time(s)')

    for i, j in itertools.product(range(3), range(2)):
        ax[i, j].plot(timestamp, values[:, i * 2 + j])
        ax[i, j].set_title(f'Joint {i*2 + j + 1}')

    fig.tight_layout()
    return fig


def plot_joint_move(title: str, a: np.ndarray, b: np.ndarray, c: np.ndarray,
                    position: np.ndarray, dh_table: np.ndarray):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')

    ax.set_title(title)
    ax.set_xlabel('x(m)')
    ax.set_ylabel('y(m)')
    ax.set_zlabel('z(m)')

    for point, label in zip([a[:3, 3], b[:3, 3], c[:3, 3]], ['A', 'B', 'C']):
        x, y, z = point[:3]
        ax.scatter(x, y, z, s=80, facecolors='none', edgecolors='black')
        ax.text(x, y, z, s=f'{label}({x}, {y}, {z})')

    def vforward(joint_variable, dh_table):
        T, trans = zip(*list(
            kinematics.forward(jv, dh_table) for jv in joint_variable))
        T, trans = map(np.array, (T, trans))
        return T, trans

    T, trans = vforward(position, dh_table)
    x, y, z = np.moveaxis(trans, 0, -1)[:3]
    u, v, w = np.moveaxis(T, 0, -1)[:3, 2]
    ax.plot(x, y, z)
    ax.quiver(x, y, z, u, v, w, length=0.05, color='cyan')

    ax.view_init(20, 160)
    fig.tight_layout()
    return fig
