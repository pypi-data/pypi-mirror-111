from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def lda(x, y, n_dim):
    """
    :param x: data with shape: (n_samples, n_features)
    :param y: data label with shape: (n_samples,)
    :param n_dim: number of components (<= min(n_classes - 1, n_features)) for dimensionality reduction
    :return: processed data with shape: (n_samples, n_dim)
    """
    clf = LinearDiscriminantAnalysis(n_components=n_dim)
    return clf.fit_transform(x, y)
