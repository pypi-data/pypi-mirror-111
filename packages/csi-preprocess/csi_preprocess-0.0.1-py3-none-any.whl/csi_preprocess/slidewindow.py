import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def slide_aug(x, window):
    """
    SlideAugment: A Simple Data Processing Method to Enhance Human Activity Recognition Accuracy Based on WiFi

    :param x: csi data with shape:(Time,Antenna,Subcarrier)
    :param window: size of sliding window
    :return: processed csi data with shape:(Time,Antenna,Subcarrier)
    """
    return np.ascontiguousarray(
        np.moveaxis(sliding_window_view(x, window, axis=0), -1, 1)
    )


if __name__ == "__main__":

    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1000, N_antenna, N_subcarrier)
    x = slide_aug(x, 900)
