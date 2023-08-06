import numpy as np


def conj_multi_antenna_pair(x1, x2):
    """
    IndoTrack: Device-Free Indoor Human Tracking with Commodity Wi-Fi
        4.3 Addressing Random CSI Phase Offset
    :param x1: csi first antenna data with shape:(Time,Subcarrier)
    :param x2: csi second antenna data with shape:(Time,Subcarrier)
    :return: processed csi data with shape:(Time,Subcarrier)
    """
    amp_x1 = np.abs(x1)
    amp_x2 = np.abs(x2)

    tmp = amp_x1.ravel()
    alpha = np.min(tmp[tmp != 0]) - 1e-1
    beta = 1000 * alpha

    x1_adj = (amp_x1 - alpha) * np.exp(1j * np.angle(x1))

    x2_adj = (amp_x2 + beta) * np.exp(1j * np.angle(x2))

    x_conj = x1_adj * x2_adj.conj()

    x_conj = x_conj - x_conj.mean()

    x_conj = x_conj / 1000
    return x_conj


if __name__ == "__main__":
    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1000, N_subcarrier, N_antenna)
    x_antenna12_result = conj_multi_antenna_pair(x[:, 0, :], x[:, 1, :])
