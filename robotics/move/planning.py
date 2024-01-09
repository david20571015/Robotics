import numpy as np


def straight_line(
    delta: np.ndarray,
    init_pos: np.ndarray,
    init_time: float,
    timestamps: np.ndarray,
    time: float,
):
    position = delta * (timestamps - init_time) / time + init_pos
    velocity = delta / time
    acceleration = 0
    return position, velocity, acceleration


def transition(
    delta1: np.ndarray,
    delta2: np.ndarray,
    init_pos: np.ndarray,
    timestamps: np.ndarray,
    time: float,
    time_acc: float,
):
    h = (timestamps - timestamps[0]) / (2 * time_acc)
    position = ((delta2 * time_acc / time + delta1) *
                (2 - h) * h**2 - 2 * delta1) * h + delta1 + init_pos
    velocity = ((delta2 * time_acc / time + delta1) *
                (1.5 - h) * 2 * h**2 - delta1) / time_acc
    acceleration = (delta2 * time_acc / time +
                    delta1) * (1 - h) * 3 * h / time_acc**2
    return position, velocity, acceleration


def plan(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    t_ab: float,
    t_bc: float,
    t_acc: float,
    sampling_time: float,
):
    if a.shape != b.shape or b.shape != c.shape:
        raise ValueError('The shape of a, b, c must be the same.'
                         f'Got {a.shape=}, {b.shape=}, {c.shape=}')

    position = np.empty((int((t_ab + t_bc) / sampling_time) + 1, len(a)))
    velocity = np.empty_like(position)
    acceleration = np.empty_like(position)

    t = 0
    # A -> A'
    delta_ab = b - a
    timestamps = np.arange(0.0, t_ab - t_acc + sampling_time,
                           sampling_time).reshape(-1, 1)

    (
        position[t:t + len(timestamps)],
        velocity[t:t + len(timestamps)],
        acceleration[t:t + len(timestamps)],
    ) = straight_line(delta_ab, a, 0, timestamps, t_ab)

    t += len(timestamps)

    # A' -> B -> B'
    delta_trans = (b - a) * timestamps[-1] / t_ab + a - b
    delta_bc = c - b
    timestamps = np.arange(t_ab - t_acc + sampling_time, t_bc + t_acc,
                           sampling_time).reshape(-1, 1)

    (
        position[t:t + len(timestamps)],
        velocity[t:t + len(timestamps)],
        acceleration[t:t + len(timestamps)],
    ) = transition(delta_trans, delta_bc, b, timestamps, t_ab, t_acc)

    t += len(timestamps)

    # B' -> C
    timestamps = np.arange(t_bc + t_acc, t_ab + t_bc,
                           sampling_time).reshape(-1, 1)

    (
        position[t:t + len(timestamps)],
        velocity[t:t + len(timestamps)],
        acceleration[t:t + len(timestamps)],
    ) = straight_line(delta_bc, b, t_ab, timestamps, t_bc)

    return position, velocity, acceleration
