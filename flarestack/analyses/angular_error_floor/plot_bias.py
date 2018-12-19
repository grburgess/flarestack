import os
import numpy as np
import matplotlib.pyplot as plt
from flarestack.data.icecube.gfu.gfu_v002_p01 import txs_sample_v1
from flarestack.data.icecube.ps_tracks.ps_v003_p01 import IC86_234567_dict
from flarestack.shared import plot_output_dir
from flarestack.utils.dataset_loader import data_loader
from flarestack.core.astro import angular_distance

basedir = plot_output_dir("analyses/angular_error_floor/plots/")

energy_bins = np.linspace(1., 10., 20 + 1)

data_samples = txs_sample_v1 + [IC86_234567_dict]


def get_data(season):
    mc = data_loader(season["mc_path"], floor=False)
    x = np.degrees(angular_distance(
        mc["ra"], mc["dec"], mc["trueRa"], mc["trueDec"]))
    y = np.degrees(mc["sigma"]) * 1.177
    return mc, x, y


try:
    os.makedirs(basedir)
except OSError:
    pass

plt.figure()

for season in data_samples:

    mc, x, y = get_data(season)

    mask = x > y
    gammas = np.linspace(1.0, 4.0, 16 + 1)
    underestimates = []

    for gamma in gammas:

        weights = mc["ow"] * mc["trueE"] ** -gamma
        frac = np.sum(weights[mask]) / np.sum(weights)
        underestimates.append(frac)

    plt.plot(gammas, underestimates, label=season["Name"])

plt.xlabel(r"Assumed Spectral Index $\gamma$ for MC weighting")
plt.ylabel("Fraction of events outside '50% contour'")
plt.plot([1, 4], [0.5, 0.5], linestyle=":")
plt.legend()
plt.title("Fraction of MC events with underestimated angular errors")
plt.savefig(basedir + "underfluctuations_index.pdf")
plt.close()


plt.figure()
ax = plt.subplot(111)
log_e_bins = np.linspace(2.0, 7.0, 10 + 1)
centers = 0.5 * (log_e_bins[:-1] + log_e_bins[1:])

for season in data_samples[3:]:

    gamma = 2.0

    mc, x, y = get_data(season)
    weights = mc["ow"] * mc["trueE"] ** -gamma

    underestimates = []
    log_es = []

    for i, lower in enumerate(log_e_bins[:-1]):
        upper = log_e_bins[i + 1]
        mask = np.logical_and(
            np.log10(mc["trueE"]) > lower,
            np.log10(mc["trueE"]) < upper
        )
        cut_mc = mc[mask]

        over_mask = x[mask] > y[mask]
        frac = np.sum(weights[mask][over_mask]) / np.sum(weights[mask])
        underestimates += [frac for _ in range(2)]
        log_es += [lower, upper]

    plt.plot(log_es, underestimates, label=season["Name"])

plt.xlabel(r"Log(True Energy/GeV)")
plt.ylabel("Fraction of events outside '50% contour'")
plt.plot([min(log_e_bins), max(log_e_bins)], [0.5, 0.5], linestyle=":")
plt.legend()
plt.title("Fraction of MC events with underestimated angular errors")
ax.set_ylim(bottom=0.4)
plt.savefig(basedir + "underfluctuations_loge_true.pdf")
plt.close()

for gamma in [2.0, 3.0, 3.5]:

    plt.figure()
    ax = plt.subplot(111)

    for season in data_samples[3:]:

        sin_dec_bins = season["sinDec bins"]

        mc, x, y = get_data(season)

        underestimates = []
        log_es = []

        for i, lower in enumerate(sin_dec_bins[:-1]):
            upper = sin_dec_bins[i + 1]
            mask = np.logical_and(
                mc["sinDec"] > lower,
                mc["sinDec"] < upper
            )
            cut_mc = mc[mask]

            over_mask = x[mask] > y[mask]

            weights = cut_mc["ow"] * cut_mc["trueE"] ** -gamma
            frac = np.sum(weights[over_mask]) / np.sum(weights)
            underestimates += [frac for _ in range(2)]
            log_es += [lower, upper]

        plt.plot(log_es, underestimates, label=season["Name"])

    plt.xlabel(r"$\sin(\delta)$")
    plt.ylabel("Fraction of events outside '50% contour'")
    plt.plot([-1., 1.], [0.5, 0.5], linestyle=":")
    plt.legend()
    plt.title(r"MC events weighted with $E^{-" + str(gamma) + "}$")
    plt.savefig(basedir + "underfluctuations_sindec_" + str(gamma) + ".pdf")
    plt.close()

    plt.figure()
    ax = plt.subplot(111)
    log_e_bins = np.linspace(2.5, 5.0, 5 + 1)
    centers = 0.5 * (log_e_bins[:-1] + log_e_bins[1:])

    for season in data_samples[3:]:

        mc, x, y = get_data(season)
        weights = mc["ow"] * mc["trueE"] ** -gamma

        underestimates = []
        log_es = []

        for i, lower in enumerate(log_e_bins[:-1]):
            upper = log_e_bins[i + 1]
            mask = np.logical_and(
                mc["logE"] > lower,
                mc["logE"] < upper
            )
            cut_mc = mc[mask]

            over_mask = x[mask] > y[mask]

            frac = np.sum(weights[mask][over_mask]) / np.sum(weights[mask])
            underestimates += [frac for _ in range(2)]
            log_es += [lower, upper]

        plt.plot(log_es, underestimates, label=season["Name"])

    plt.xlabel(r"Log(Energy Proxy/GeV)")
    plt.ylabel("Fraction of events outside '50% contour'")
    plt.plot([min(log_e_bins), max(log_e_bins)], [0.5, 0.5], linestyle=":")
    plt.legend()
    plt.title(r"MC events weighted with $E^{-" + str(gamma) + "}$")
    ax.set_ylim(bottom=0.4)
    plt.savefig(basedir + "underfluctuations_loge_" + str(gamma) + ".pdf")
    plt.close()

raw_input("prompt")

    # print


for season in data_samples:

    mc, x, y = get_data(season)

    title = season["Data Sample"] + "/" + season["Name"]

    savedir = basedir + title + "/"

    try:
        os.makedirs(savedir)
    except OSError:
        pass


    # mc = mc[mc["logE"] < 4.0]

    plt.figure()
    ax = plt.subplot(111)


    weights = mc["ow"] * mc["trueE"] ** -3.0

    print "True", max(x), min(x), "Reco", max(y), min(y)

    print "frac over",

    mask = x > y
    print np.sum(weights[mask])/np.sum(weights)

    max_err = 1.0
    bins = np.linspace(0.0, max_err, 11)

    hist_2d, bin_edges = np.histogramdd((x, y),
                                        bins=(bins, bins),
                                        weights=weights)

    meds = []
    centers = 0.5*(bin_edges[0][:-1] + bin_edges[0][1:])

    for i, row in enumerate(hist_2d.T):
        mask = np.logical_and(
            y > bin_edges[0][i],
            y < bin_edges[0][i + 1]
        )
        row /= np.sum(weights[mask])
        mc_cut = x[mask]
        # meds.append(np.median(mc_cut))

    X, Y = np.meshgrid(bin_edges[0], bin_edges[1])
    cbar = ax.pcolormesh(X, Y, hist_2d)
    range = [0.0, max_err]
    plt.plot(range, range, color="white", linestyle="--")
    # plt.plot(centers, meds, color="white", linestyle=":")
    plt.colorbar(cbar, label="Log(N)")

    # plt.scatter()
    plt.ylabel(r"True $\sigma$ (degrees)")
    plt.xlabel(r"Fit $\sigma$ (degrees)")
    ax.set_xlim(left=0.0)
    ax.set_ylim(bottom=0.0)
    plt.title(title)
    plt.savefig(savedir + "scatter.pdf")
    plt.close()

    # raw_input("prompt")