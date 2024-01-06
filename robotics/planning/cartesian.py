import numpy as np

A = np.array(
    [
        [0.64, 0.77, 0, 5],
        [0.77, -0.64, 0, -55],
        [0, 0, -1, -60],
        [0, 0, 0, 1],
    ],
    dtype=np.float64,
)


B = np.array(
    [
        [0.87, -0.1, 0.48, 50],
        [0.29, 0.9, -0.34, -40],
        [-0.4, 0.43, 0.81, 40],
        [0, 0, 0, 1],
    ],
    dtype=np.float64,
)


C = np.array(
    [
        [0.41, -0.29, 0.87, 60],
        [0.69, 0.71, -0.09, 15],
        [-0.6, 0.64, 0.49, -30],
        [0, 0, 0, 1],
    ],
    dtype=np.float64,
)
t_AB = 0.5
t_BC = 0.5

t_acc = 0.2
sample_rate = 0.002


def pose(trans_mats: np.ndarray):
    [
        [n_x, o_x, a_x, p_x],
        [n_y, o_y, a_y, p_y],
        [n_z, o_z, a_z, p_z],
        [_, _, _, _],
    ] = trans_mats

    phi = np.arctan2(a_y, a_x)
    theta = np.arctan2(np.cos(phi) * a_x + np.sin(phi) * a_y, a_z)
    psi = np.arctan2(
        -np.sin(phi) * n_x + np.cos(phi) * n_y,
        -np.sin(phi) * o_x + np.cos(phi) * o_y,
    )

    return np.concatenate([trans_mats[0:3, 3], np.rad2deg([phi, theta, psi])])


A_pose = pose(A)
B_pose = pose(B)
C_pose = pose(C)