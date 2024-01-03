from functools import reduce

import numpy as np


def input_joint_variable(upper_bound: np.ndarray, lower_bound: np.ndarray):
    prompt = 'please enter the joint variable (in degree):\n'

    items = []
    for i, (upper, lower) in enumerate(
            zip(upper_bound, lower_bound),
            start=1,
    ):
        items.append(f'theta{i}  ({lower} ~ {upper})')
    prompt += ', '.join(items) + ':\n'

    joint_variable = np.array(np.mat(input(prompt), dtype=np.float64))
    joint_variable = joint_variable.reshape(-1)
    return joint_variable


def dh2trans(d: np.ndarray, a: np.ndarray, alpha: np.ndarray,
             theta: np.ndarray):
    return np.array(
        [
            [
                np.cos(theta),
                -np.sin(theta) * np.cos(alpha),
                np.sin(theta) * np.sin(alpha),
                a * np.cos(theta),
            ],
            [
                np.sin(theta),
                np.cos(theta) * np.cos(alpha),
                -np.cos(theta) * np.sin(alpha),
                a * np.sin(theta),
            ],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )


def kinematics(joint_variable: np.ndarray, dh_table: np.ndarray):
    jv = np.deg2rad(joint_variable)

    dh_table = np.concatenate([dh_table, jv[:, np.newaxis]], axis=1)

    trans_mats = [dh2trans(*dh) for dh in dh_table]
    T6 = reduce(np.matmul, trans_mats)

    [
        [n_x, o_x, a_x, p_x],
        [n_y, o_y, a_y, p_y],
        [n_z, o_z, a_z, p_z],
        [_, _, _, _],
    ] = T6

    phi = np.arctan2(a_y, a_x)
    theta = np.arctan2(np.cos(phi) * a_x + np.sin(phi) * a_y, a_z)
    psi = np.arctan2(
        -np.sin(phi) * n_x + np.cos(phi) * n_y,
        -np.sin(phi) * o_x + np.cos(phi) * o_y,
    )

    return T6, np.concatenate([T6[0:3, 3], np.rad2deg([phi, theta, psi])])
