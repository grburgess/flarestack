import os
import numpy as np
from scipy.interpolate import interp1d
from shared import skylab_ref_dir

root_url = "https://icecube.wisc.edu/~coenders/"


def download_ref():
    print
    print "Downloading .npy files from", root_url
    print

    for file in os.listdir(skylab_ref_dir):
        os.remove(skylab_ref_dir + file)

    for name in ["sens", "disc"]:
        file = name + ".npy "

        cmd = "wget --user=icecube --password=skua -P " + skylab_ref_dir + \
              " " + root_url + file

        print cmd
        os.system(cmd)


def skylab_7year_sensitivity(sindec=0.0):
    """Interpolates between the saved values of the Stefan Coenders 7 year PS
    analysis sensitivity. Then converts given values for sin(declination to
    the equivalent skylab sensitivity. Adds values for Sindec = +/- 1,
    equal to nearest known value.

    :param sindec: Sin(declination)
    :return: 7 year PS sensitivity at sindec
    """
    skylab_sens_path = skylab_ref_dir + "sens.npy"
    data = np.load(skylab_sens_path)
    sindecs = np.sin(np.array([x[0] for x in data]))

    # The sensitivities here are given in units TeV ^ -gamma per cm2 per s
    # The sensitivities used in this code are GeV ^-1 per cm2 per s
    # The conversion is thus (TeV/Gev) ^ (1 - gamma) , i.e 10 ** 3(1-gamma)
    sens = np.array([x[2] for x in data]) * 10 ** 3

    # Extend range of sensitivity to +/- 1 through approximation,
    # by 1d-extrapolation of first/last pair

    sindecs = np.append(-1, sindecs)
    sindecs = np.append(sindecs, 1)

    lower_diff = sens[0] - sens[1]

    upper_diff = sens[-1] - sens[-2]

    sens = np.append(sens[0] + lower_diff, sens)
    sens = np.append(sens, sens[-1] + upper_diff)

    sens_ref = interp1d(sindecs, sens)

    return sens_ref(sindec)