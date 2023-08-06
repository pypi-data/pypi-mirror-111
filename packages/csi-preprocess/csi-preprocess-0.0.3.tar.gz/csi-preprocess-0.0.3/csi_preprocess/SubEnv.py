import numpy as np


def env_subtracting(x, env_data):
    """

    :param x: csi data with shape:(Time,Antenna,Subcarrier)
    :param env_data: csi environment data with shape:(Antenna,Subcarrier)
    :return: processed csi data with shape:(Time,Antenna,Subcarrier)
    """
    return x - env_data[None, ...]


if __name__ == "__main__":

    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1000, N_antenna, N_subcarrier)
    env_data = np.random.randn(N_antenna, N_subcarrier)
    env_subtracting(x, env_data)
