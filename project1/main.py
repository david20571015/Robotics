import numpy as np


class JointVariableConstraint:
    upper_bound = np.array([160, 125, 135, 140, 100, 260], dtype=np.float32)
    lower_bound = np.array([-160, -125, -135, -140, -100, -260],
                           dtype=np.float32)

    @classmethod
    def prompt(cls):
        items = []
        for i, (upper, lower) in enumerate(
                zip(cls.upper_bound, cls.lower_bound),
                start=1,
        ):
            items.append(f'theta{i}  ({lower} ~ {upper})')
        return ', '.join(items) + ':\n'

    @classmethod
    def check(cls, joint_variable):
        return np.all(
            np.logical_and(
                cls.lower_bound <= joint_variable,
                joint_variable <= cls.upper_bound,
            ))


def q1():
    print('please enter the joint variable (in degree):')
    # print(JointVariableConstraint.display())
    joint_variable = np.array(
        np.mat(
            input(JointVariableConstraint.prompt()),
            dtype=np.float32,
        ))

    print(joint_variable)
    if JointVariableConstraint.check(joint_variable):
        print('valid')
    else:
        print('invalid')


if __name__ == '__main__':
    q1()
