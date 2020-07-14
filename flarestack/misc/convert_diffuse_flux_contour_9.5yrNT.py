"""Script to convert the Diffuse Flux contour to a format where it can be
plotted as a 'butterfly contour'.

The values are taken from https://arxiv.org/pdf/1908.09551.pdf
for the 9.5years Northern Track sample, tracing the 68% and 95% contours in Figure 5.


"""
import numpy as np
import matplotlib.pyplot as plt
from flarestack.shared import illustration_dir

contour_68 = [
    (2.1474761536053775, 1.1819099315348742),
    (2.15745389846805, 1.3039308554297238),
    (2.16382267178465, 1.0801421376692102),
    (2.168493105550156, 1.3560868497858762),
    (2.180947595591506, 1.058583433968721),
    (2.1832828124742596, 1.4456793322604407),
    (2.1957373025156097, 1.4867502250347786),
    (2.198072519398363, 1.0562400966099719),
    (2.210527009439713, 1.5595889612692213),
    (2.223759905108648, 1.6005973650473257),
    (2.2276519332465696, 1.078736135253961),
    (2.243220045798257, 1.6692571496586668),
    (2.243220045798257, 1.093941791004064),
    (2.258593556943049, 1.7046708354927582),
    (2.2712426483912953, 1.128414887259436),
    (2.2868107609429833, 1.1489321076893706),
    (2.2909317319125475, 1.7968859358478402),
    (2.3092547898716664, 1.1924021780638827),
    (2.322617419811865, 1.8351654346580837),
    (2.3257310423222024, 1.226366388855137),
    (2.337407126735968, 1.845153910149751),
    (2.3490832111497344, 1.2896364975413555),
    (2.3638729180738376, 1.328008646790868),
    (2.3662081349565907, 1.8352240180920525),
    (2.3833330587634474, 1.8214152252101306),
    (2.390338709411707, 1.4436816371621073),
    (2.398901171315135, 1.7323163579825978),
    (2.4018201924185765, 1.535833378794905),
    (2.404350010708226, 1.6800755571315573),
    (2.4059068219633946, 1.5907162925179348),
]

contour_95 = [

    (2.0552051480586435, 0.9918704219323407),
    (2.0610731289435105, 0.8727567814199388),
    (2.061851534571095, 1.0399539019666677),
    (2.0680787795917697, 1.1217949592209706),
    (2.0774196471227824, 1.1718447396415814),
    (2.0781980527503667, 0.8289363728113357),
    (2.090652542791717, 0.8138921469681679),
    (2.0907940710876414, 1.259173111877621),
    (2.1015502215778987, 1.3077739286980719),
    (2.114783117246833, 1.391032705054418),
    (2.1171183341295863, 0.8071433353749717),
    (2.1272376072881833, 1.4347671912932003),
    (2.1326864466812743, 0.8129756416900795),
    (2.142027314212287, 1.5167058876041177),
    (2.154481804253637, 1.557808024876572),
    (2.162265860529481, 0.8235466968862131),
    (2.1700499168053247, 1.6329354205980597),
    (2.178612378708753, 0.8352868170535448),
    (2.1832828124742596, 1.6766386623387253),
    (2.2011861419087, 1.7538516283094996),
    (2.2074133869293755, 0.8615087620979445),
    (2.2151974432052195, 1.792449742232891),
    (2.223759905108648, 0.8770450887864492),
    (2.2323223670120758, 1.8602391443966964),
    (2.2471120739361794, 1.895418496494913),
    (2.25256091332927, 0.9121248490469194),
    (2.266572214625789, 1.9619399857663957),
    (2.268129025880958, 0.9315485120427702),
    (2.2821403271774767, 1.994408226725949),
    (2.294594817218827, 0.9728172866385139),
    (2.3054924960050087, 2.0479404668324777),
    (2.310162929770515, 0.9934126183137395),
    (2.3367584553796483, 1.0478710346144409),
    (2.342855966129059, 2.0926619444492665),
    (2.359980889935916, 2.1138551991092838),
    (2.388003492528954, 1.1480989210729264),
    (2.3950690205331813, 2.119689336603769),
    (2.410577255728901, 2.107109735140886),
    (2.4135112461713346, 1.219330067793694),
    (2.4262565690845292, 1.2659092768882467),
    (2.4362646414391858, 2.0589541524185972),
    (2.445494308166258, 1.3109776056299611),
    (2.450275942735705, 2.024071902021222),
    (2.4572815933839642, 1.3733326968713349),
    (2.4687846987693782, 1.9302528572597586),
    (2.4703729607569747, 1.455779116276648),
    (2.4782985453287427, 1.892617371445009),
    (2.4789212698308103, 1.5090593546275337),
    (2.4829689790942493, 1.8005509942445652),
    (2.4860826016045867, 1.747892856168681),
    (2.4860826016045867, 1.6484683996617662),
]


units = 10 ** -18  #/ u.GeV /u.cm**2 / u.s / u.sr


def f(energy, norm, index):
    return norm * units * energy ** -index * (10**5) ** index

# Fit is valid from 40 TeV to 3.5 PeV.
global_fit_e_range = np.logspace(np.log10(40) + 3, np.log10(3.5) + 6, 100)



def upper_contour(energy_range, contour):
    """Trace upper contour"""
    return [max([f(energy, norm, index) for (index, norm) in contour])
            for energy in energy_range]


def lower_contour(energy_range, contour):
    """Trace lower contour"""
    return [min([f(energy, norm, index) for (index, norm) in contour])
            for energy in energy_range]


plt.figure()

# Plot 68% contour

for (index, norm) in contour_68:
    plt.plot(global_fit_e_range,
             global_fit_e_range ** 2 * f(global_fit_e_range, norm, index),
             alpha=0.6)
plt.plot(
    global_fit_e_range,
    global_fit_e_range ** 2 * upper_contour(global_fit_e_range, contour_68),
    color="k", label="68% contour", linestyle="-"
)
plt.plot(
    global_fit_e_range,
    global_fit_e_range ** 2 * lower_contour(global_fit_e_range, contour_68),
    color="k", linestyle="-",
)

# Plot 95% contour

for (index, norm) in contour_95:
    plt.plot(global_fit_e_range,
             global_fit_e_range ** 2 * f(global_fit_e_range, norm, index),
             alpha=0.3)
plt.plot(
    global_fit_e_range,
    global_fit_e_range ** 2 * upper_contour(global_fit_e_range, contour_95),
    color="k", linestyle="--", label="95% contour"
)
plt.plot(
    global_fit_e_range,
    global_fit_e_range ** 2 * lower_contour(global_fit_e_range, contour_95),
    color="k", linestyle="--"
)

plt.yscale("log")
plt.xscale("log")
plt.legend()
plt.title(r"Diffuse Flux 9.5yr NT Best Fit ($\nu_{\mu} + \bar{\nu}_{\mu})$")
plt.ylabel(r"$E^{2}\frac{dN}{dE}$[GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]")
plt.xlabel(r"$E_{\nu}$ [GeV]")
plt.savefig(illustration_dir + "diffuse_flux_9.5yearsNTsample.pdf")
plt.close()

