# Robotics Project 1

## Overview

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

## Usage

- Forward Kinematics

```bash
python3 main.py forward
```

- Inverse Kinematics

```bash
python3 main.py backward
```
