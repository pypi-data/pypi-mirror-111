import numpy as np


def antenna_selection(x, w, step):
    """
    Framework for Human Activity Recognition Based on WiFi CSI Signal Enhancement
    ALGORITHM1:Antenna selection
    :param x: csi data with shape:(Time,Antenna,Subcarrier)
    :param w: window size
    :param stride: stride of sliding window
    :return: index of selected antenna
    """
    assert step < w
    R = [0, 0, 0]
    for i in range(N_antenna):
        m = np.mean(x[:, i, :], 1)
        var_l = []
        for j in range(0, len(m) - w, step):
            var_l.append(np.var(m[j : j + w]))
        R[i] = np.max(var_l) - min(var_l)
    return np.argmax(R)


if __name__ == "__main__":
    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1234, N_antenna, N_subcarrier)
    w = 10
    step = 3
    antenna_selection(x, w, step)
