import numpy as np


def linear_transform(x, subc_n):
    """
    You are Facing the Mona Lisa:Spot Localization using PHY Layer Information
        4.1 Data Sanitization
    :param x: csi data with shape:(Time,Antenna,Subcarrier)
    :param subc_n: number of subcarriers
    :return: processed csi data with shape:(Time,Antenna,Subcarrier)
    """
    subcarrier_index = np.arange(subc_n)
    a = (x[:, :, N_subcarrier - 1] - x[:, :, 0]) / (2 * np.pi * N_subcarrier)
    b = np.mean(x, axis=2)
    x_post = x - a[:, :, None] * subcarrier_index[None, None, :] - b[:, :, None]
    return x_post


if __name__ == "__main__":
    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1000, N_antenna, N_subcarrier)
    linear_transform(x, N_subcarrier)
