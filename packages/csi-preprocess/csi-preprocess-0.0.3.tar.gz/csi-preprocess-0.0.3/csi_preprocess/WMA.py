import numpy as np
from numba import float64
from numba import int64
from numba import jit


@jit((float64[:], int64), nopython=True, nogil=True)
def wma(arr_in, window):
    """

    :param arr_in: csi data with shape:(Time,)
    :param window: size of sliding window
    :return: processed csi data with shape:(Time,)
    """
    n = arr_in.shape[0]
    wma_arr = np.empty(n, dtype=np.float64)
    arr_in = np.concatenate((np.ones(window - 1) * arr_in[0], arr_in))
    weight = np.arange(1, window + 1)
    sw = weight.sum()
    for i in range(n):
        wma_arr[i] = (weight * arr_in[i : i + window]).sum() / sw
    return wma_arr


@jit((float64[:], int64), nopython=True, nogil=True)
def ewma(arr_in, window):
    """

    :param arr_in: csi data with shape:(Time,)
    :param window: size of sliding window
    :return: processed csi data with shape:(Time,)
    """
    n = arr_in.shape[0]
    ewma_arr = np.empty(n, dtype=float64)
    alpha = 2 / float(window + 1)
    w = 1
    ewma_old = arr_in[0]
    ewma_arr[0] = ewma_old
    for i in range(1, n):
        w += (1 - alpha) ** i
        ewma_old = ewma_old * (1 - alpha) + arr_in[i]
        ewma_arr[i] = ewma_old / w
    return ewma_arr


@jit((float64[:], int64), nopython=True, nogil=True)
def ewma_infinite_hist(arr_in, window):
    """

    :param arr_in: csi data with shape:(Time,)
    :param window: size of sliding window
    :return: processed csi data with shape:(Time,)
    """
    n = arr_in.shape[0]
    ewma_arr = np.empty(n, dtype=float64)
    alpha = 2 / float(window + 1)
    ewma_arr[0] = arr_in[0]
    for i in range(1, n):
        ewma_arr[i] = arr_in[i] * alpha + ewma_arr[i - 1] * (1 - alpha)
    return ewma_arr


if __name__ == "__main__":

    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1000, N_antenna, N_subcarrier)
    wma(x[:, 0, 0], 30)
