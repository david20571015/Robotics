# Robotics

## Environment

- Ubuntu 22.04
- Python 3.11.0

- Use [poetry](https://python-poetry.org/) (recommended)

```bash
poetry install
poetry shell
```

- Or use pip

```bash
pip install -r requirements.txt
```

## Project 1

### Overview

For a PUMA 560 robot manipulator with the following DH parameters:

| Joint | d(m)  | a(m)  | $\alpha$ | $\theta$   |
| ----- | ----- | ----- | -------- | ---------- |
| 1     | 0     | 0     | -90      | $\theta_1$ |
| 2     | 0     | 0.432 | 0        | $\theta_2$ |
| 3     | 0.149 | -0.02 | 90       | $\theta_3$ |
| 4     | 0.433 | 0     | -90      | $\theta_4$ |
| 5     | 0     | 0     | 90       | $\theta_5$ |
| 6     | 0     | 0     | 0        | $\theta_6$ |

$$
-160^{\circ} \leq \theta_1 \leq 160^{\circ}, -125^{\circ} \leq \theta_2 \leq 125^{\circ}
\newline
-135^{\circ} \leq \theta_3 \leq 135^{\circ}, -140^{\circ} \leq \theta_4 \leq 140^{\circ}
\newline
-100^{\circ} \leq \theta_5 \leq 100^{\circ}, -260^{\circ} \leq \theta_6 \leq 260^{\circ}
$$

write a program to for the following transformations:

1. Forward Kinematics
   - input: Joint angles $(\theta_1, \theta_2, \theta_3, \theta_4, \theta_5, \theta_6)$
   - output: Cartesian point $(n, o, a, p)$ and $(x ,y, z, \phi, \theta, \psi)$
2. Inverse Kinematics
   - input: Cartesian point $(n, o, a, p)$
   - output: Joint angles $(\theta_1, \theta_2, \theta_3, \theta_4, \theta_5, \theta_6)$

### Usage

- Forward Kinematics

```bash
python3 main.py kinematics forward
```

- Inverse Kinematics

```bash
python3 main.py kinematics backward
```

## Project 2

### Overview

For a PUMA 560 robot manipulator in Project 1, write a program to plan a path.

- Start point:

$$
A = \begin{bmatrix}
   0.64 & 0.77  & 0  & 0.05  \\
   0.77 & -0.64 & 0  & -0.55 \\
   0    & 0     & -1 & -0.6  \\
   0    & 0     & 0  & 1
\end{bmatrix}
$$

- Via point:

$$
B = \begin{bmatrix}
   0.87 & -0.1 & 0.48  & 0.5  \\
   0.29 & 0.9  & -0.34 & -0.4 \\
   -0.4 & 0.43 & 0.81  & 0.4  \\
   0    & 0    & 0     & 1
\end{bmatrix}
$$

- End point:

$$
C = \begin{bmatrix}
   0.41 & -0.29 & 0.87  & 0.6  \\
   0.69 & 0.71  & -0.09 & 0.15 \\
   -0.6 & 0.64  & 0.49  & -0.3 \\
   0    & 0     & 0     & 1
\end{bmatrix}
$$

The time to move from $A$ to $B$ is 0.5 seconds, and the time to move from $B$ to $C$ is 0.5 seconds.
The $t_{acc}$ for transition portion is 0.2 seconds and the sampling time is 0.002 seconds.

Write a program for the following movements:

1. Joint move
   1. Position of each joint
   2. Velocity of each joint
   3. Acceleration of each joint
   4. 3D trajectory
2. Cartesian move
   1. Position of each x, y, z
   2. Velocity of each x, y, z
   3. Acceleration of each x, y, z
   4. 3D trajectory

### Usage

- Joint move

```bash
python3 main.py move joint
```

- Cartesian move

```bash
python3 main.py move cartesian
```
