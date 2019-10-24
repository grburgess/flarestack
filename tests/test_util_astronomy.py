"""A standard time-integrated analysis is performed, using one year of
IceCube data (IC86_1).
"""
import logging
import unittest
from flarestack.analyses.tde.shared_TDE import tde_catalogue_name
from flarestack.utils import load_catalogue, calculate_astronomy
from astropy import units as u

true_res_astro = {
    'Energy Flux (GeV cm^{-2} s^{-1})': 1.151292546497023e-08,
    'Flux from nearest source':   8.61854306789315e-10 / (u.cm**2 * u.GeV * u.s),
    'Mean Luminosity (erg/s)': 9.34797120080954e+45
}

catalogue = tde_catalogue_name("jetted")


class TestUtilAstro(unittest.TestCase):

    def setUp(self):
        pass

    def test_neutrino_astronomy(self):

        logging.info("Testing neutrino_astronomy util function.")

        injection_energy_pdf = {
            "energy_pdf_name": "power_law",
            "gamma": 2.0
        }

        cat = load_catalogue(catalogue)

        res_astro = calculate_astronomy(1.e-9, injection_energy_pdf, cat)

        self.assertEqual(res_astro, true_res_astro)

        logging.info("Calculated values {0}".format(res_astro))
        logging.info("Reference  values {0}".format(true_res_astro))


if __name__ == '__main__':
    unittest.main()