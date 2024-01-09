import matplotlib.pyplot as plt
import numpy as np


def plot_cartesian(title: str, timestamp: np.ndarray, values: np.ndarray):
    fig, ax = plt.subplots(3, 1, figsize=(10, 8))

    ax[1].set_ylabel(title)
    ax[2].set_xlabel('time(s)')

    for i, label in enumerate(['x', 'y', 'z']):
        ax[i].plot(timestamp, values[:, i])
        ax[i].set_title(label)

    fig.tight_layout()
    return fig


def plot_cartesian_move(title: str, a: np.ndarray, b: np.ndarray, c: np.ndarray,
                        position: np.ndarray):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection='3d')

    ax.set_title(title)
    ax.set_xlabel('x(m)')
    ax.set_ylabel('y(m)')
    ax.set_zlabel('z(m)')

    for point, label in zip([a, b, c], ['A', 'B', 'C']):
        x, y, z = point[:3]
        ax.scatter(x, y, z, s=80, facecolors='none', edgecolors='black')
        ax.text(x, y, z, s=f'{label}({x}, {y}, {z})')

    # x, y, z = np.moveaxis(position[:, :3], -1, 0)
    x, y, z = position[:, 0], position[:, 1], position[:, 2]
    u = np.cos(np.deg2rad(position[:, 3])) * np.sin(np.deg2rad(position[:, 4]))
    v = np.sin(np.deg2rad(position[:, 3])) * np.sin(np.deg2rad(position[:, 4]))
    w = np.cos(np.deg2rad(position[:, 4]))
    ax.plot(x, y, z)
    ax.quiver(x, y, z, u, v, w, length=0.05, color='cyan')

    ax.view_init(20, 65)
    fig.tight_layout()
    return fig
