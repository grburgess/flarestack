"""Script to convert the Diffuse Flux contour to a format where it can be
plotted as a 'butterfly contour'.

The values are taken from https://arxiv.org/abs/1607.08006
for the 6years Northern Track sample, tracing the 68% and 95% contours in Figure 6.


"""
import numpy as np
from astropy import units as u

contour_68 = np.array([
    (1.9321029740384577, 0.5435661287274187),
    (1.9397702849315752, 0.6304832917736136),
    (1.9538255805117974, 0.4926978308209975),
    (1.9522723425949229, 0.6831862993153308),
    (1.9815112815112812, 0.49160595289627507),
    (2.0091781379171407, 0.5026876824530779),
    (2.036839119243811, 0.5175647131658856),
    (2.0612014837821286, 1.037541737541737),
    (2.0644911216758723, 0.5382421097963612),
    (2.08250810508875, 1.0928192121740503),
    (2.0921354754199326, 0.5638605588752212),
    (2.103819197367584, 1.1452084387568249),
    (2.119774175785906, 0.5931310901985385),
    (2.126389478002381, 1.1970652131942447),
    (2.1474085529804, 0.625194390297029),
    (2.1514783201000207, 1.2477377342479978),
    (2.175033618728633, 0.6632728846805089),
    (2.1790914139887745, 1.2935500498550347),
    (2.2026500381339087, 0.7069369166143353),
    (2.206720802908486, 1.3288357754633406),
    (2.229001663840373, 0.7547544521738065),
    (2.2343721402372427, 1.3499428288284587),
    (2.252830604443507, 0.8064201128717254),
    (2.2620500816981752, 1.3538636128078938),
    (2.272884947078495, 0.8577663835728346),
    (2.2897709223222416, 1.330071537402915),
    (2.2891645698097305, 0.9088720346784855),
    (2.3029213448568284, 0.9639308381243858),
    (2.30997848997849, 1.2824344443699276),
    (2.314417189901061, 1.016324616969778),
    (2.3213909310683505, 1.226126532578145),
    (2.3213704458865747, 1.0767793148438303),
    (2.323989988506117, 1.172941879393492),
    (2.325327012423786, 1.1221276543857184),
])

contour_95 = np.array([
    (1.8106484596220667, 0.31415018365164915),
    (1.8244061024706184, 0.4847774196161283),
    (1.8383586585932625, 0.29723261600094375),
    (1.8555254974609812, 0.5880998687450294),
    (1.8660409232256738, 0.2983606312052056),
    (1.8730523472458953, 0.6464000689807139),
    (1.893716204273389, 0.30400004212320875),
    (1.8889133824617694, 0.6969455130745446),
    (1.9097826613955644, 0.7637784186171275),
    (1.9213854993913644, 0.3135063636529902),
    (1.9275221581673192, 0.8201925363215681),
    (1.9490531317510786, 0.32408682701937774),
    (1.976715110732706, 0.3383193726302225),
    (2.004374096749463, 0.354485373546956),
    (2.018311621537428, 1.1056830701991989),
    (2.032030422353003, 0.37237000140225884),
    (2.035351216641539, 1.153588503911084),
    (2.0596847526466293, 0.39154359946148753),
    (2.0873350923204295, 0.4132951379285683),
    (2.114983104132664, 0.4365504749668965),
    (2.142628122980029, 0.4617392673111138),
    (2.1611731984166003, 1.4880721481894499),
    (2.1702699271614225, 0.48900473387276877),
    (2.1887749855491787, 1.541188628285402),
    (2.1979078515735404, 0.5187765313865014),
    (2.216385751576367, 1.5885047424636864),
    (2.225540233458122, 0.5521288016889181),
    (2.2440131451861656, 1.6250794382759188),
    (2.2531686247228766, 0.5880590123991878),
    (2.271657498930226, 1.6506978873547782),
    (2.2807900324029355, 0.6285006188231987),
    (2.2993221383250706, 1.6632118060270547),
    (2.308401130981776, 0.6756019046341621),
    (2.3270087261289607, 1.6615470524561429),
    (2.3347501960405186, 0.7250736186220053),
    (2.354722915719983, 1.642051544397585),
    (2.358579258579258, 0.7766605089185727),
    (2.3812087592732754, 1.603164350906286),
    (2.3786313366958525, 0.8294696585019157),
    (2.3949132239454816, 0.8791124307253337),
    (2.4026826123600316, 1.5504100955713853),
    (2.408678290613774, 0.9288148468793622),
    (2.417870284321897, 1.494012717883685),
    (2.419923436052468, 0.9805799257412153),
    (2.4292819937981225, 1.4381774285000086),
    (2.4311640698737467, 1.0352595094530574),
    (2.435658006625748, 1.3837892708860444),
    (2.4373718115653595, 1.0895745057035375),
    (2.442040421072679, 1.3252656672011505),
    (2.4423202632880052, 1.144487596100499),
    (2.4450872870227705, 1.2537644569902628),
    (2.444757451209064, 1.1958706507093595),
    (1.9467397384064054, 0.87421395754729),
    (1.9699116365783031, 0.9514640347973669),
    (1.99666166332833, 1.0320578653911978),
    (1.7988125071458405, 0.3703905370572027),
    (1.8130521047187713, 0.4308697642030963),
    (1.839755256421923, 0.5417448750782072),
])


units = 10 ** -18  #/ u.GeV /u.cm**2 / u.s / u.sr

for contour in [contour_68, contour_95]:
    contour.T[1] *= units

best_fit_flux = 0.90 * units * (
        u.GeV ** -1 * u.cm ** -2 * u.s ** -1 * u.sr ** -1
)
best_fit_gamma = 2.13

# Fit is valid from 194 TeV and 7.8 PeV
e_range = np.logspace(np.log10(194) + 3, np.log10(7.8) + 6, 100)

nt_16 = {
    "northern_tracks_16": (
        best_fit_flux,
        best_fit_gamma,
        contour_68,
        contour_95,
        e_range,
        "https://arxiv.org/abs/1607.08006"
    )
}

