import numpy as np
import os
import cPickle as Pickle
from core.minimisation import MinimisationHandler
from core.results import ResultsHandler
from data.icecube_pointsource_7year import ps_7year
from shared import plot_output_dir, flux_to_k, analysis_dir
from utils.prepare_catalogue import ps_catalogue_name
from utils.skylab_reference import skylab_7year_sensitivity
from scipy.interpolate import interp1d
from cluster import run_desy_cluster as rd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialise Injectors/LLHs

injection_energy = {
    "Name": "Power Law",
    "Gamma": 2.0,
}

injection_time = {
    "Name": "Steady",
}

llh_time = {
    "Name": "Steady",
}

inj_kwargs = {
    "Injection Energy PDF": injection_energy,
    "Injection Time PDF": injection_time,
    "Poisson Smear?": True,
}

llh_energy = injection_energy

llh_kwargs = {
    "LLH Energy PDF": llh_energy,
    "LLH Time PDF": llh_time,
    "Fit Gamma?": True,
}

name = "tests/ps_sens"

# sindecs = np.linspace(0.90, -0.90, 13)
sindecs = np.linspace(0.75, -0.75, 7)

sens = []

analyses=[]

for sindec in sindecs:
    cat_path = ps_catalogue_name(sindec)

    subname = name + "/sindec=" + '{0:.2f}'.format(sindec) + "/"

    scale = flux_to_k(skylab_7year_sensitivity(sindec)) * 2

    mh_dict = {
        "name": subname,
        "datasets": ps_7year,
        "catalogue": cat_path,
        "inj kwargs": inj_kwargs,
        "llh kwargs": llh_kwargs,
        "scale": scale,
        "n_steps": 10
    }

    analysis_path = analysis_dir + subname

    try:
        os.makedirs(analysis_path)
    except OSError:
        pass

    pkl_file = analysis_path + "dict.pkl"

    with open(pkl_file, "wb") as f:
        Pickle.dump(mh_dict, f)

    rd.submit_to_cluster(pkl_file, n_jobs=10)

    # mh = MinimisationHandler(mh_dict)
    # mh.iterate_run(mh_dict["scale"], mh_dict["n_steps"])

    analyses.append(mh_dict)

rd.wait_for_cluster()

for rh_dict in analyses:
    rh = ResultsHandler(rh_dict["name"], rh_dict["llh kwargs"],
                        rh_dict["catalogue"])
    sens.append(rh.sensitivity)

plot_range = np.linspace(-0.99, 0.99, 1000)

plt.figure()
ax1 = plt.subplot2grid((4, 1), (0, 0), colspan=3, rowspan=3)
ax1.plot(plot_range, skylab_7year_sensitivity(plot_range),
         label=r"7-year Point Source analysis")

ax1.scatter(
    sindecs, sens, color='black',
    label='FlareStack')

ax1.set_xlim(xmin=-1., xmax=1.)
# ax1.set_ylim(ymin=1.e-13, ymax=1.e-10)
ax1.grid(True, which='both')
ax1.semilogy(nonposy='clip')
ax1.set_ylabel(r"Flux Strength [ GeV$^{-1}$ cm$^{-2}$ s$^{"
               r"-1}$ ]",
               fontsize=12)

plt.title('7-year Point Source Sensitivity')

ax2 = plt.subplot2grid((4, 1), (3, 0), colspan=3, rowspan=1, sharex=ax1)

ratios = sens / skylab_7year_sensitivity(sindecs)

ax2.scatter(sindecs, ratios, color="black")
ax2.plot(sindecs, ratios, linestyle="--", color="red")
ax2.set_ylabel(r"ratio", fontsize=12)
ax2.set_xlabel(r"sin($\delta$)", fontsize=12)
#
ax1.set_xlim(xmin=-1.0, xmax=1.0)
# ax2.set_ylim(ymin=0.5, ymax=1.5)
ax2.grid(True)
xticklabels = ax1.get_xticklabels()
plt.setp(xticklabels, visible=False)
plt.subplots_adjust(hspace=0.001)

ratio_interp = interp1d(sindecs, ratios)

interp_range = np.linspace(np.min(sens),
                           np.max(sens), 1000)

ax1.plot(
    interp_range,
    skylab_7year_sensitivity(interp_range)*ratio_interp(interp_range),
    color='red', linestyle="--", label="Ratio Interpolation")

ax1.legend(loc='upper right', fancybox=True, framealpha=1.)

plt.savefig(plot_output_dir(name) + "/7yearPS.pdf")
plt.close()