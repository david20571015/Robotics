import argparse
from functools import partial
from typing import cast

import matplotlib.pyplot as plt
import numpy as np

from robotics import kinematics
from robotics import move
from robotics.utils import check_out_of_range


def forward_kinematics(dh_table: np.ndarray, upper_bound: np.ndarray,
                       lower_bound: np.ndarray):
    jv = kinematics.input_joint_variable(upper_bound, lower_bound)
    check_out_of_range(jv, upper_bound, lower_bound)
    noap, output = kinematics.forward(jv, dh_table)

    def print_mat(name, mat):
        print(name + ':')
        print(np.array2string(mat, max_line_width=500, precision=15))

    print_mat('[n o a p]', noap)
    print()
    print_mat('output', output)


def backward_kinematics(dh_table: np.ndarray, upper_bound: np.ndarray,
                        lower_bound: np.ndarray):
    cartesian_coordinate = kinematics.input_cartesian_point()
    jvs = kinematics.backward(cartesian_coordinate, dh_table)

    # Normalize theta to (-180, 180]
    jvs = (jvs + 180) % 360 - 180

    for jv in jvs:
        print(
            f'Corresponding variable ({", ".join(f"theta{i}"for i in range(1, 7))})'
        )
        check_out_of_range(jv, upper_bound, lower_bound)
        print(np.array2string(jv, max_line_width=200, precision=4))
        print()


def joint_move(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    t_ab: float,
    t_bc: float,
    t_acc: float,
    sampling_time: float,
    dh_table: np.ndarray,
    upper_bound: np.ndarray,
    lower_bound: np.ndarray,
):

    def trans_to_joint(trans: np.ndarray):
        check = partial(check_out_of_range,
                        upper_bound=upper_bound,
                        lower_bound=lower_bound,
                        verbose=False)
        joint = list(filter(check, kinematics.backward(trans, dh_table)))[-1]
        return cast(np.ndarray, joint)

    a_joint, b_joint, c_joint = map(trans_to_joint, (a, b, c))
    position, velocity, acceleration = move.plan(a_joint, b_joint, c_joint,
                                                 t_ab, t_bc, t_acc,
                                                 sampling_time)

    titles = [
        'angle(degree)',
        'angle velocity(degree/s)',
        'angle acceleration(degree/s^2)',
    ]
    datas = [position, velocity, acceleration]
    file_names = ['joint_position', 'joint_velocity', 'joint_acceleration']
    timestamp = np.arange(0, len(position)) * sampling_time

    for title, data, file_name in zip(titles, datas, file_names):
        fig = move.plot_joint(title, timestamp, data)
        fig.savefig(f'{file_name}.png')
        plt.close(fig)

    fig = move.plot_joint_move('3D path of joint move', a, b, c, position,
                               dh_table)
    fig.savefig('joint_move.png')
    plt.close(fig)


def cartesian_move(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    t_ab: float,
    t_bc: float,
    t_acc: float,
    sampling_time: float,
):

    def trans_to_pos_and_angle(trans: np.ndarray):
        [
            [n_x, o_x, a_x, p_x],
            [n_y, o_y, a_y, p_y],
            [n_z, o_z, a_z, p_z],
            [_, _, _, _],
        ] = trans

        phi = np.arctan2(a_y, a_x)
        theta = np.arctan2(np.cos(phi) * a_x + np.sin(phi) * a_y, a_z)
        psi = np.arctan2(
            -np.sin(phi) * n_x + np.cos(phi) * n_y,
            -np.sin(phi) * o_x + np.cos(phi) * o_y,
        )

        return np.concatenate([trans[:3, 3], np.rad2deg([phi, theta, psi])])

    a_pa, b_pa, c_pa = map(trans_to_pos_and_angle, (a, b, c))
    position, velocity, acceleration = move.plan(a_pa, b_pa, c_pa, t_ab, t_bc,
                                                 t_acc, sampling_time)

    titles = ['position(m)', 'velocity(m/s)', 'acceleration(m/s^2)']
    datas = [position, velocity, acceleration]
    file_names = [
        'cartesian_position', 'cartesian_velocity', 'cartesian_acceleration'
    ]
    timestamp = np.arange(0, len(position)) * sampling_time

    for title, data, file_name in zip(titles, datas, file_names):
        fig = move.plot_cartesian(title, timestamp, data)
        fig.savefig(f'{file_name}.png')
        plt.close(fig)

    fig = move.plot_cartesian_move('3D path of cartesian move', a_pa, b_pa,
                                   c_pa, position)
    fig.savefig('cartesian_move.png')
    plt.close(fig)


if __name__ == '__main__':
    # d, a, alpha
    DH_TABLE = np.array(
        [
            [0, 0, -np.pi / 2],
            [0, 0.432, 0],
            [0.149, -0.02, np.pi / 2],
            [0.433, 0, -np.pi / 2],
            [0, 0, np.pi / 2],
            [0, 0, 0],
        ],
        dtype=np.float64,
    )

    UB = np.array([160.0, 125.0, 135.0, 140.0, 100.0, 260.0])
    LB = np.array([-160.0, -125.0, -135.0, -140.0, -100.0, -260.0])

    A = np.array(
        [
            [0.64, 0.77, 0, 5 / 100],
            [0.77, -0.64, 0, -55 / 100],
            [0, 0, -1, -60 / 100],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    B = np.array(
        [
            [0.87, -0.1, 0.48, 50 / 100],
            [0.29, 0.9, -0.34, -40 / 100],
            [-0.4, 0.43, 0.81, 40 / 100],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    C = np.array(
        [
            [0.41, -0.29, 0.87, 60 / 100],
            [0.69, 0.71, -0.09, 15 / 100],
            [-0.6, 0.64, 0.49, -30 / 100],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )
    T_AB = 0.5
    T_BC = 0.5

    T_ACC = 0.2
    SAMPLING_TIME = 0.002

    FN_MAP = {
        'kinematics': {
            'forward': forward_kinematics,
            'backward': backward_kinematics,
        },
        'move': {
            'joint':
                partial(joint_move,
                        dh_table=DH_TABLE,
                        upper_bound=UB,
                        lower_bound=LB),
            'cartesian':
                cartesian_move,
        },
    }

    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(dest='mode', required=True)

    for mode, fn_map in FN_MAP.items():
        sp = sub_parser.add_parser(mode)
        sp.add_argument('func', choices=fn_map)

    args = parser.parse_args()

    func = FN_MAP[args.mode][args.func]
    match args.mode:
        case 'kinematics':
            func(DH_TABLE, UB, LB)
        case 'move':
            func(A, B, C, T_AB, T_BC, T_ACC, SAMPLING_TIME)
