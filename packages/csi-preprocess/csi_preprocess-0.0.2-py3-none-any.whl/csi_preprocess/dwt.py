import numpy as np
import pywt


def dwt(x, level, wavelet="db2"):
    """
    :param x: csi data with shape:(Time,*)
    :param level: dwt decomposition level (must be >= 0). If level is None then it will be calculated automatically.
    :param wavelet: wavelet name, check the pywt package for more details.
    :return:     [cA_n, cD_n, cD_n-1, ..., cD2, cD1] : list
        Ordered list of coefficients arrays
        where ``n`` denotes the level of decomposition. The first element
        (``cA_n``) of the result is approximation coefficients array and the
        following elements (``cD_n`` - ``cD_1``) are details coefficients
        arrays.
    """
    db = pywt.Wavelet(wavelet)
    return pywt.wavedec(x, db, level=level, axis=0)


if __name__ == "__main__":
    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1234, N_antenna, N_subcarrier)
    dwt(x, level=None)
