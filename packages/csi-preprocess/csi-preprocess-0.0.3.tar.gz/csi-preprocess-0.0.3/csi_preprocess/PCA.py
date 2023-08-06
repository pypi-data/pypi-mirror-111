import scipy.linalg
import numpy as np


def pca(X, k):
    """

    :param X: csi data with shape:(Time,Subcarrier)
    :param k: number of components for dimensionality reduction
    :return: processed data with shape:(Time,k)
    """

    def complex_sign(complex):
        return complex / abs(complex)

    center = X - X.mean(axis=0)
    U, S, V = scipy.linalg.svd(center, full_matrices=False)
    V = V.conj().T
    max_abs_idx = np.argmax(abs(V), axis=0)
    colsign = complex_sign(V[max_abs_idx, range(V.shape[0])])
    U *= colsign
    V *= colsign[None, :]
    score = U * S
    return score[:, :k]


if __name__ == "__main__":
    N_subcarrier = 30
    x = np.random.randn(1000, N_subcarrier)
    pcax = pca(x, k=3)
