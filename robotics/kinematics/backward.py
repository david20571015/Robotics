from itertools import product

import numpy as np


def input_cartesian_point():
    prompt = 'Please enter Cartesian point:\n'
    cartesian_coordinate = np.array(np.mat(input(prompt), dtype=np.float64))
    return cartesian_coordinate


def kinematics(cartesian_coordinate: np.ndarray, dh_table: np.ndarray):
    [
        [n_x, o_x, a_x, p_x],
        [n_y, o_y, a_y, p_y],
        [n_z, o_z, a_z, p_z],
        [_, _, _, _],
    ] = cartesian_coordinate

    [
        [d_1, a_1, alpha_1],
        [d_2, a_2, alpha_2],
        [d_3, a_3, alpha_3],
        [d_4, a_4, alpha_4],
        [d_5, a_5, alpha_5],
        [d_6, a_6, alpha_6],
    ] = dh_table

    # Compute theta1
    tmp = np.sqrt(p_x**2 + p_y**2 - d_3**2)
    tmp = np.array([tmp, -tmp])
    theta1 = (np.arctan2(p_y, p_x) - np.arctan2(d_3, tmp))

    # Compute theta3
    tmp = ((p_x**2 + p_y**2 + p_z**2 - a_2**2 - a_3**2 - d_3**2 - d_4**2) /
           (2 * a_2))
    tmp2 = np.sqrt(a_3**2 + d_4**2 - tmp**2)
    tmp2 = np.array([tmp2, -tmp2])
    theta3 = (-np.arctan2(a_3, d_4) + np.arctan2(tmp, tmp2))

    # Compute theta2
    def compute_theta2(theta1, theta3):
        s_1, c_1 = np.sin(theta1), np.cos(theta1)
        s_3, c_3 = np.sin(theta3), np.cos(theta3)
        theta23 = np.arctan2(
            (-a_3 - a_2 * c_3) * p_z + (c_1 * p_x + s_1 * p_y) *
            (d_4 + a_2 * s_3),
            (a_2 * s_3 + d_4) * p_z + (a_3 + a_2 * c_3) *
            (c_1 * p_x + s_1 * p_y),
        )
        theta2 = theta23 - theta3
        return theta2

    theta123 = np.array([
        [t1, compute_theta2(t1, t3), t3] for t1, t3 in product(theta1, theta3)
    ])

    s_1, c_1 = np.sin(theta123[:, 0]), np.cos(theta123[:, 0])
    s_23, c_23 = (np.sin(theta123[:, 1] + theta123[:, 2]),
                  np.cos(theta123[:, 1] + theta123[:, 2]))

    # Compute theta4
    theta4 = np.arctan2(
        -a_x * s_1 + a_y * c_1,
        a_x * c_1 * c_23 + a_y * s_1 * c_23 - a_z * s_23,
    )
    s_4, c_4 = np.sin(theta4), np.cos(theta4)

    # Compute theta5
    theta5 = np.arctan2(
        a_x * (c_1 * c_23 * c_4 - s_1 * s_4) + a_y *
        (s_1 * c_23 * c_4 + c_1 * s_4) - a_z * s_23 * c_4,
        a_x * c_1 * s_23 + a_y * s_1 * s_23 + a_z * c_23,
    )

    # Compute theta6
    theta6 = np.arctan2(
        o_x * c_1 * s_23 + o_y * s_1 * s_23 + o_z * c_23,
        -n_x * c_1 * s_23 - n_y * s_1 * s_23 - n_z * c_23,
    )

    # Combine all theta
    theta456 = np.stack([theta4, theta5, theta6], axis=1)
    theta456_ = np.stack([theta4 + np.pi, -theta5, theta6 + np.pi], axis=1)
    theta456_[theta456_ > np.pi] -= 2 * np.pi
    theta456_[theta456_ < -np.pi] += 2 * np.pi
    theta456 = np.concatenate([*zip(theta456, theta456_)], axis=0)

    theta123 = np.repeat(theta123, 2, axis=0)

    theta123465 = np.concatenate([theta123, theta456], axis=1)

    return np.rad2deg(theta123465)
