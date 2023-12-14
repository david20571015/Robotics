import argparse

import numpy as np

from robotics import kinematics


def check_out_of_range(value, upper_bound, lower_bound):
    for i, (theta, upper, lower) in enumerate(
            zip(value, upper_bound, lower_bound),
            start=1,
    ):
        if not lower <= theta <= upper:
            print(f'theta{i} is out of range!')


def forward_kinematics(dh_table, upper_bound, lower_bound):
    jv = kinematics.input_joint_variable(upper_bound, lower_bound)
    check_out_of_range(jv, upper_bound, lower_bound)
    noap, output = kinematics.forward(jv, dh_table)

    def print_mat(name, mat):
        print(name + ':')
        print(np.array2string(mat, max_line_width=500, precision=15))

    print_mat('[n o a p]', noap)
    print()
    print_mat('output', output)


def backward_kinematics(dh_table, upper_bound, lower_bound):
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

    FN_MAP = {
        'forward': forward_kinematics,
        'backward': backward_kinematics,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=FN_MAP)
    args = parser.parse_args()

    FN_MAP[args.mode](DH_TABLE, UB, LB)
