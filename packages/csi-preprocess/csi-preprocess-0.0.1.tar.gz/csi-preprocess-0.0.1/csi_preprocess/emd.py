from PyEMD import EMD


def emd(x):
    """

    :param x: csi data with shape: (Time,)
    :return: IMFs data with shape: (IMF level,Time)
    """
    emd = EMD()
    IMFs = emd.emd(x)
    return IMFs
