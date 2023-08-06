import numpy as np


def phase_ratio(x):
    """

    :param x: csi data with shape:(Time,Antenna,Subcarrier)
    :return: processed csi data with shape:(Time,Antenna,Subcarrier)
    """
    x = x[:, 0, :] / x[:, 1, :]
    return x


if __name__ == "__main__":

    N_subcarrier = 30
    N_antenna = 2
    x = np.random.randn(1000, N_antenna, N_subcarrier)
    phase_ratio(x)
