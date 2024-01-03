import numpy as np


def check_out_of_range(value: np.ndarray,
                       upper_bound: np.ndarray,
                       lower_bound: np.ndarray,
                       verbose=True):
    is_out_of_range = (lower_bound > value) | (value > upper_bound)

    if verbose:
        for i in np.nonzero(is_out_of_range)[0]:
            print(f'theta{i+1} is out of range!')

    return not np.any(is_out_of_range)
