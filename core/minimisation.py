import numpy as np
import resource
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm
import scipy.optimize
from core.injector import Injector
from core.llh import LLH
from core.ts_distributions import plot_background_ts_distribution


class MinimisationHandler:
    """Generic Class to handle both dataset creation and llh minimisation from
    experimental data and Monte Carlo simulation. Initilialised with a set of
    IceCube datasets, a list of sources, and independent sets of arguments for
    the injector and the likelihood.
    """
    n_trials = 1000

    def __init__(self, datasets, sources, inj_kwargs, llh_kwargs, scale=1.):

        self.injectors = dict()
        self.llhs = dict()
        self.seasons = datasets
        self.sources = sources

        self.inj_kwargs = inj_kwargs
        self.llh_kwargs = llh_kwargs

        # For each season, we create an independent injector and a
        # likelihood, using the source list along with the sets of energy/time
        # PDFs provided in inj_kwargs and llh_kwargs.

        for season in self.seasons:
            self.injectors[season["Name"]] = Injector(season, sources,
                                                      **inj_kwargs)
            self.llhs[season["Name"]] = LLH(season, sources, **llh_kwargs)

        # The default value for n_s is 1. It can be between 0 and 1000.
        p0 = [1.]
        bounds = [(0, 1000.)]

        # If weights are to be fitted, then each source has an independent
        # n_s in the same 0-1000 range.
        if "Fit Weights?" in llh_kwargs.keys():
            if llh_kwargs["Fit Weights?"]:
                p0 = [1. for x in sources]
                bounds = [(0, 1000.) for x in sources]

        # If gamma is to be included as a fit parameter, then its default
        # value if 2, and it can range between 1 and 4.
        if "Fit Gamma?" in llh_kwargs.keys():
            if llh_kwargs["Fit Gamma?"]:
                p0.append(2.)
                bounds.append((1., 4.))

        self.p0 = p0
        self.bounds = bounds

        # Sets the default flux scale for finding sensitivity
        # Default value is 1 (Gev)^-1 (cm)^-2 (s)^-1
        self.scale = scale
        self.bkg_ts = None

    def run_trials(self, n=n_trials, scale=1):

        param_vals = [[] for x in self.p0]
        ts_vals = []
        flags = []

        print "Generating", n, "trials!"

        for i in tqdm(range(int(n))):

            f = self.run(scale)

            res = scipy.optimize.fmin_l_bfgs_b(
                f, self.p0, bounds=self.bounds, approx_grad=True)

            flag = res[2]["warnflag"]

            if flag > 0:
                res = scipy.optimize.brute(f, ranges=self.bounds,
                                           full_output=True)

            vals = res[0]
            ts = -res[1]

            for j, val in enumerate(vals):
                param_vals[j].append(val)
            ts_vals.append(float(ts))

            flags.append(flag)

        mem_use = str(
            float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1.e6)
        print 'Memory usage max: %s (Gb)' % mem_use

        for i, param in enumerate(param_vals):
            print "Parameter", i, ":", np.mean(param), np.median(param), np.std(
                param)

        print "Test Statistic:", np.mean(ts_vals), np.std(ts_vals)

        # print "FLAG STATISTICS:"
        # for i in sorted(np.unique(flags)):
        #     print "Flag", i, ":", flags.count(i)

        return ts_vals, param_vals, flags

    def run(self, scale=1):

        llh_functions = dict()

        for season in self.seasons:
            dataset = self.injectors[season["Name"]].create_dataset(scale)
            llh_f = self.llhs[season["Name"]].create_llh_function(dataset)
            llh_functions[season["Name"]] = llh_f

        def f_final(params):

            weights_matrix = np.ones([len(self.seasons), len(self.sources)])

            for i, season in enumerate(self.seasons):
                llh = self.llhs[season["Name"]]
                acc = llh.acceptance(self.sources, params)

                time_weights = []

                for source in self.sources:

                    time_weights.append(llh.time_PDF.effective_injection_time(
                        source))

                w = acc * self.sources["weight_distance"] * np.array(
                    time_weights)

                w = w[:, np.newaxis]

                for j, ind_w in enumerate(w):
                    weights_matrix[i][j] = ind_w

            weights_matrix /= np.sum(weights_matrix)

            ts_val = 0
            for i, (name, f) in enumerate(llh_functions.iteritems()):
                w = weights_matrix[i][:, np.newaxis]

                ts_val += f(params, w)

            return -ts_val

        return f_final

    def scan_likelihood(self, scale=1):

        f = self.run(scale)

        n_range = np.linspace(1, 200, 1e4)
        y = []

        for n in tqdm(n_range):
            new = f([n])
            try:
                y.append(new[0][0])
            except IndexError:
                y.append(new)

        plt.figure()
        plt.plot(n_range, y)
        plt.savefig("llh_scan.pdf")
        plt.close()

        min_y = np.min(y)
        print "Minimum value of", min_y,

        min_index = y.index(min_y)
        min_n = n_range[min_index]
        print "at", min_n

        l_y = np.array(y[:min_index])
        try:
            l_y = min(l_y[l_y > (min_y + 0.5)])
            l_lim = n_range[y.index(l_y)]
        except ValueError:
            l_lim = 0

        u_y = np.array(y[min_index:])
        try:
            u_y = min(u_y[u_y > (min_y + 0.5)])
            u_lim = n_range[y.index(u_y)]
        except ValueError:
            u_lim = ">" + str(max(n_range))

        print "One Sigma interval between", l_lim, "and", u_lim

    def bkg_trials(self):
        """Generate 1000 Background Trials, and plots the distribution. Also
        fits a Chi-squared distribution to the data, accounting for the fact
        that the Test Statistic distribution is truncated at 0.

        :return: Array of Test Statistic values
        """
        print "Generating background trials"

        bkg_ts, params, flags = self.run_trials(100, 0.0)

        ts_array = np.array(bkg_ts)

        frac = float(len(ts_array[ts_array <= 0])) / (float(len(ts_array)))

        print "Fraction of underfluctuations is", frac

        plot_background_ts_distribution(ts_array)

        self.bkg_ts = ts_array

        return ts_array

    def find_sensitivity(self):

        if self.bkg_ts is None:
            self.bkg_trials()

        bkg_median = np.median(self.bkg_ts)

        ts = self.run_trials(100, scale=self.scale)[0]
        frac_over = np.sum(ts > bkg_median) / float(len(ts))

        if frac_over < 0.95:
            rescale = 10
        else:
            rescale = 0.1

        converge = False

        # while not conver
