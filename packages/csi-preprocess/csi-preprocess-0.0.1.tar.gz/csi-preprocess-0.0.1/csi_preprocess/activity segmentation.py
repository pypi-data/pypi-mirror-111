import numpy as np


def act_seg(x, w, stride):
    """
        Framework for Human Activity Recognition Based on WiFi CSI Signal Enhancement
            ALGORITHM4:Activity segmentation
    :param x: csi data with shape:(Time,Subcarrier)
    :param w: window size
    :param stride: stride of sliding window
    :return: Tuple : (Start_Time,End_Time)
    """
    start_t = []
    end_t = []
    for i in range(N_subcarrier):
        v = []
        for j in range(0, len(x) - w, stride):
            v.append(np.mean(x[j : j + w, i]))
        v = np.array(v)
        t = np.quantile(v, 0.75)

        vv = np.where(v > t)[0]
        vv = np.split(vv, np.where(np.diff(vv) != 1)[0] + 1)
        vv = sorted(vv, key=lambda x: len(x))[-1]

        start_t.append(vv[0])
        end_t.append(vv[-1])
    start_t = np.min(start_t)
    end_t = np.max(end_t)

    return start_t, end_t


if __name__ == "__main__":
    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1234, N_subcarrier)
    w = 10
    step = 3
    act_seg(x, w, step)
