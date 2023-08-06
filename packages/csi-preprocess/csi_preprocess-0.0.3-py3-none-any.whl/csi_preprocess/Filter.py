import numpy as np
import scipy.signal
import scipy.ndimage


def bandpass_filter(x, sample_rate):
    """

    :param x: csi data with shape:(Time,*)
    :param sample_rate: csi data sample rate
    :return: csi data with shape:(Time,*)
    """
    sample_rate -= sample_rate % 2
    half_rate = sample_rate / 2
    uppe_orde = 6
    uppe_stop = 60
    lowe_orde = 3
    lowe_stop = 2

    sos_low = scipy.signal.butter(
        uppe_orde, uppe_stop / half_rate, "lowpass", output="sos"
    )
    sos_high = scipy.signal.butter(
        lowe_orde, lowe_stop / half_rate, "highpass", output="sos"
    )

    x = scipy.signal.sosfiltfilt(sos_low, x, axis=0)
    x = scipy.signal.sosfiltfilt(sos_high, x, axis=0)
    return x


def lowpass_filter(x, sample_rate):
    """

    :param x: csi data with shape:(Time,*)
    :param sample_rate: csi data sample rate
    :return: csi data with shape:(Time,*)
    """
    sample_rate -= sample_rate % 2
    half_rate = sample_rate / 2
    uppe_orde = 6
    uppe_stop = 60

    sos_low = scipy.signal.butter(
        uppe_orde, uppe_stop / half_rate, "lowpass", output="sos"
    )

    x = scipy.signal.sosfiltfilt(sos_low, x, axis=0)
    return x


def median_filter(x, window_size):
    """

    :param x: csi data with shape:(Time,)
    :param window_size: filter window size
    :return: csi data with shape:(Time,)
    """
    x = scipy.ndimage.median_filter(x, window_size)
    return x


if __name__ == "__main__":

    N_subcarrier = 30
    N_antenna = 3
    x = np.random.randn(1234, N_antenna, N_subcarrier)
    x2 = median_filter(x, (10, 1, 1))
