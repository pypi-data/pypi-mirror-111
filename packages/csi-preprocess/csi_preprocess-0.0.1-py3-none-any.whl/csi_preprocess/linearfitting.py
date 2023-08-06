import numpy as np

import scipy.optimize

from numba import float64, njit, int32


@njit(float64(float64[:], float64[:, :], int32[:, :]))
def __cost_f(args, d, t):  # d:(30,3)
    p = args[0]
    w = args[1]
    return np.sum((d + p * t + w) ** 2)


@njit(float64[:](float64[:], float64[:, :], int32[:, :]))
def __jac(args, d, t):
    p = args[0]
    w = args[1]

    dp = np.sum(2 * (d + p * t + w) * t)
    dw = np.sum(2 * (d + p * t + w))
    return np.array((dp, dw))


def linear_fitting(x, subc_n):
    """
    SpotFi: Decimeter Level Localization Using WiFi
        Algorithm 1:SpotFi’s ToF sanitization algorithm
    :param x: csi data with shape:(Time,Antenna,Subcarrier)
    :param subc_n: number of subcarriers
    :return: processed csi data with shape:(Time,Antenna,Subcarrier)
    """
    t = np.arange(subc_n)[None, :]
    for i in range(x.shape[0]):
        ret0 = scipy.optimize.fmin_bfgs(
            __cost_f,
            x0=np.array([0.0, 0.0]),
            fprime=__jac,
            args=(
                x[i, ...],
                t,
            ),
            disp=False,
        )
        p = ret0[0]
        w = ret0[1]
        x[i, ...] = x[i, ...] + p * t
    return x


if __name__ == "__main__":
    N_subcarrier = 30
    N_antenna = 3
    N_time = 1000
    x = np.random.randn(N_time, N_antenna, N_subcarrier)
    linear_fitting(x, N_subcarrier)
