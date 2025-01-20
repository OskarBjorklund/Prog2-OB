"""
Plotting tools for SF1918 lab assignments
"""

import numpy as np

from scipy import stats

import matplotlib as mpl
import matplotlib.pyplot as plt

# Not used, but needed to register 3D projection axes.
from mpl_toolkits.mplot3d import Axes3D


def plot_mvn_pdf(mu_x, mu_y, sigma_x, sigma_y, rho):
    """
    Plot the mulivariate normal PDF

    Arguments
    ---------
    mu_x, mu_y
        The x- and y-coordinates of the mean vector.
    sigma_x, sigma_y
        The standard deviation along the x- and y-axis.
    rho
        The correlation between -1 and 1.
    """
    if rho < -1 or rho > 1:
        raise ValueError('rho must be between -1 and 1')

    mu = np.array([mu_x, mu_y])
    sigma = np.array([[sigma_x ** 2, rho * sigma_x * sigma_y],
                      [rho * sigma_x * sigma_y, sigma_y ** 2]])

    rv = stats.multivariate_normal(mu, sigma)

    x, y = np.meshgrid(np.linspace(-10, 10, 100), np.linspace(-10, 10, 100))
    z = rv.pdf(np.dstack((x, y)))


    default_figsize = mpl.rcParams['figure.figsize']
    figsize = [2 * default_figsize[0], default_figsize[1]]
    fig = plt.figure(figsize=figsize)

    ax = fig.add_subplot(1, 2, 1, projection='3d')

    ax.plot_surface(x, y, z, cmap=mpl.cm.coolwarm,
                    linewidth=0, antialiased=False)

    ax = fig.add_subplot(1, 2, 2)
    ax.contour(x, y, z)
