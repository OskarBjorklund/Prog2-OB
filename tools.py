"""
Tools for SF1918 lab assignments
"""

import numpy as np
from scipy import stats


def regress(X, y, alpha=0.05):
    """
    Multiple linear regression using ordinary least squares

    The model is

        y = X * beta + e

    where
        - y is a vector of observed values with shape (n,),
        - X is a matrix of regressors wit shape (n, p),
        - beta is a vector of parameters with shape (p,), and
        - e is a vector of random errors with shape(n,).

    Given X and y, the function estimates beta using ordinary least squares,
    that is by minimizing the objective

        | y - X * beta |^2

    In addition, a confidence interval with significance level alpha is
    calculated for beta. Any rows containing NaN values are discarded prior to
    processing.

    Arguments
    ---------
    y
        The vector y in the model.
    X
        The matrix X in the model.
    alpha, optional
        The significance level of the confidence interval for beta. Default is
        0.05.

    Returns
    -------
    beta
        The estimate of the vector beta in the model. Its shape is (p,).
    beta_int
        The confidence intervals of beta wit significance level alpha. Its
        shape is (p, 2).
    """

    if y.ndim != 1:
        raise TypeError("y must be a vector")

    if X.ndim != 1 and X.ndim != 2:
        raise TypeError("X must be a vector or a matrix")

    if X.shape[0] != y.shape[0]:
        raise TypeError("X and y must contain the same number of rows")

    if X.ndim == 1:
        X = X[:, np.newaxis]

    notnans = ~np.any(np.isnan(np.concatenate((X, y[:, np.newaxis]), axis=-1)), axis=-1)

    X = X[notnans]
    y = y[notnans]

    n = X.shape[0]
    p = X.shape[1]

    Q, R = np.linalg.qr(X, "reduced")

    beta = np.linalg.solve(R, np.dot(Q.T, y))

    dof = n - p

    r = y - np.dot(X, beta)
    sse = np.sum(r ** 2)
    v = sse / dof

    c = np.diag(np.linalg.inv(R.T @ R))

    t_alpha_2 = stats.t.ppf(1 - alpha / 2, dof)
    dbeta = t_alpha_2 * np.sqrt(v * c)
    beta_int = np.stack((beta - dbeta, beta + dbeta), axis=0).T

    return beta, beta_int
