"""Final script to unblind individual TDEs. Draws the background TS values
generated by compare_cluster_search_to_time_integration.py, in order to
quantify the significance of the result. Produces relevant post-unblinding
plots.
"""
import numpy as np
from flarestack.core.unblinding import Unblinder
from flarestack.data.icecube.gfu.gfu_v002_p01 import txs_sample_v1
from flarestack.data.icecube.gfu.gfu_v002_p04 import gfu_v002_p04
from flarestack.analyses.tde.shared_TDE import individual_tde_cat, \
    individual_tdes
from flarestack.utils.custom_seasons import custom_dataset

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
    "Flare Search?": True
}

name_root = "analyses/tde/unblind_individual_tdes/"
#bkg_ts_root = "analyses/tde/compare_cluster_search_to_time_integration/"
bkg_ts_root = "analyses/tde/compare_spectral_indices_individual/AT2018cow/flare_winter/"
cat_res = dict()

for j, cat in enumerate(["AT2018cow"]):
# for j, cat in enumerate(individual_tdes):

    name = name_root + cat.replace(" ", "") + "/"

    bkg_ts = bkg_ts_root #+ cat.replace(" ", "") + "/flare/"

    cat_path = individual_tde_cat(cat)
    catalogue = np.load(cat_path)

    if cat != "AT2018cow":
        dataset = custom_dataset(txs_sample_v1, catalogue,
                                 unblind_llh["LLH Time PDF"])
    else:
        dataset = gfu_v002_p04

    unblind_dict = {
        "name": name,
        "datasets": dataset,
        "catalogue": cat_path,
        "llh kwargs": unblind_llh,
        "background TS": bkg_ts
    }

    ub = Unblinder(unblind_dict, mock_unblind=False, full_plots=True)
