import numpy as np
import os
from shared import plots_dir
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.optimize, scipy.stats


class Chi2_LeftTruncated(object):
    """ A class similar to the ones from scipy.stats
       allowing to fit left-truncated chi^2 distributions.
    """

    def __init__(self, data, cut=0., **kwargs):
        """ Fit the given ensemble of measurements with a chi^2 function.

        `data` is a list of test statistics values.
        `cut` defines where the distribution is truncated.
        """

        data_left = data[data <= cut]
        data_right = data[data > cut]
        N_all = len(data)
        N_left = len(data_left)

        # three parameters will be fitted: dof, location, scale
        p_start = [2., -1., 1.]
        p_bounds = [(0., None),  # dof > 0
                    (None, -0),  # location < 0 for 'truncated' effect
                    (1e-5, 1e5)]  # shape ~ free

        # define the fit function: likelihood for chi^2 distribution,
        # plus knowledge about the amount of truncated data
        def func(p):
            dist = scipy.stats.chi2(*p)
            loglh = dist.logpdf(data_right).sum()
            # print loglh,
            loglh += N_left * dist.logcdf(cut)

            # print loglh, p, N_all, N_left

            return -loglh

        res = scipy.optimize.minimize(func, x0=p_start, bounds=p_bounds)

        if not res.success:
            print 'Chi2 fit did not converge! Result is likely garbage.'

        self._q_left = N_left / float(N_all)
        self._cut = cut
        self._f = scipy.stats.chi2(*res.x)
        self._ks = scipy.stats.kstest(data_right, self._f.cdf)[0]

    def pdf(self, x):
        """ Probability density function.
        """
        m_flat = (0. <= x) & (x <= self._cut)
        m_chi2 = (x > self._cut)

        x = np.asarray(x)
        r = np.zeros_like(x)
        if self._cut == 0.:
            r[m_flat] = self._f.cdf(self._cut)
        else:
            r[m_flat] = self._f.cdf(self._cut) / self._cut
        r[m_chi2] = self._f.pdf(x[m_chi2])
        return r

    def cdf(self, x):
        """ Cumulative distribution function.
        """
        return self._f.cdf(x)

    def sf(self, x):
        """ Survival function.
        """
        return self._f.sf(x)

    def isf(self, x):
        """ Inverse survival function.
        """
        return self._f.isf(x)

    def ppf(self, x):
        """ Percent point function.
        """
        return self._f.ppf(x)

    def __str__(self):
        return 'Left-truncated Chi^2 Distribution:\n' + \
               '\t DoF      = {0:7.2f}\n'.format(self._f.args[0]) + \
               '\t Location = {0:7.2f}\n'.format(self._f.args[1]) + \
               '\t Scale    = {0:7.2f}\n'.format(self._f.args[2]) + \
               '\t KS       = {0:7.2%}'.format(self._ks)


def plot_background_ts_distribution(ts_array, path):
    ts_array = np.array(ts_array)

    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

    plt.figure()
    plt.hist(ts_array, bins=20, lw=2, histtype='step', color='black',
             label='Test Stat', density=True)

    yrange = 0.1/float(len(ts_array))

    try:
        chi2 = Chi2_LeftTruncated(ts_array)
        df = chi2._f.args[0]
        loc = chi2._f.args[1]
        scale = chi2._f.args[2]
        xrange = np.linspace(
            min([np.min(ts_array), loc]), np.max(ts_array), 100
        )
        plt.plot(xrange, scipy.stats.chi2.pdf(xrange, df, loc, scale))
    except ValueError:
        pass

    plt.ylim((yrange, 1.))
    plt.yscale("log")
    plt.grid()
    plt.xlabel(r"$\lambda$")
    plt.savefig(path)
    plt.close()


def plot_fit_results(results, name, labels):
    results = np.array(results)

    dir = plots_dir + name + "/"
    try:
        os.makedirs(dir)
    except OSError:
        pass
    path = dir + "params.pdf"

    n_dim = len(results)
    print n_dim
    plt.figure()

    for i, row in enumerate(results):
        plt.subplot(n_dim, 1, i+1)
        plt.hist(row, density=True)
        plt.title(labels[i])

    plt.savefig(path)
    plt.close()