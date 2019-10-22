"""Script to unblind the TDE catalogues. Draws the background TS values
generated by compare_spectral_indices.py, in order to
quantify the significance of the result. Produces relevant post-unblinding
plots.
"""
import numpy as np
from flarestack.core.unblinding import Unblinder
from flarestack.data.icecube.gfu.gfu_v002_p01 import txs_sample_v1
from flarestack.utils.custom_seasons import custom_dataset
from flarestack.analyses.tde.shared_TDE import tde_catalogue_name, \
    tde_catalogues, tde_weighted_catalogue_name

analyses = dict()

# Initialise Injectors/LLHs

# Shared

llh_energy = {
    "Name": "Power Law",
    "Gamma": 2.0,
}

llh_time = {
    "Name": "FixedEndBox"
}

unblind_llh = {
    "LLH Energy PDF": llh_energy,
    "LLH Time PDF": llh_time,
    "Fit Gamma?": True,
    "Fit Negative n_s?": False,
    "Fit Weights?": True
}

name_root = "analyses/tde/unblind_stacked_TDEs_weighted/"

bkg_ts_root = "analyses/tde/compare_mass_weighting/"

cat_res = dict()

res = []

for j, cat in enumerate(["jetted"]):

    name = name_root + cat.replace(" ", "") + "/"

    bkg_ts = bkg_ts_root + cat.replace(" ", "") + "/" #+ "/fit_weights/"

    cat_path = tde_weighted_catalogue_name(cat)
    catalogue = np.load(cat_path)

    unblind_dict = {
        "name": name,
        "datasets": custom_dataset(txs_sample_v1, catalogue,
                                   unblind_llh["LLH Time PDF"]),
        "catalogue": cat_path,
        "llh kwargs": unblind_llh,
        "background TS": bkg_ts
    }

    ub = Unblinder(unblind_dict, mock_unblind=False, full_plots=True)

    res.append((cat, ub.ts))

for x in res:
    print x
