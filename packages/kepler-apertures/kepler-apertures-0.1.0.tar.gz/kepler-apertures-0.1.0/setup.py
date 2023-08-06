# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kepler_apertures']

package_data = \
{'': ['*'], 'kepler_apertures': ['data/*']}

install_requires = \
['astropy>=4.2,<5.0',
 'lightkurve>=2.0.4,<3.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.2.0,<1.3.0',
 'patsy>=0.5.1,<0.6.0',
 'photutils>=1.0.2,<2.0.0',
 'pyia>=1.2,<2.0',
 'scipy>=1.6.1,<2.0.0',
 'tqdm>=4.59.0,<5.0.0',
 'wget>=3.0,<4.0']

setup_kwargs = {
    'name': 'kepler-apertures',
    'version': '0.1.0',
    'description': "Tools to compute PRF models from Kepler's FFI and use them to do aperture photometry and compile light curves of the EXBA masks. ",
    'long_description': "# Kepler Apertures\n\nTake me to the [documentation](https://jorgemarpa.github.io/kepler-apertures/).\nPaper coming soon!\n\nTools to create aperture mask for Kepler sources using PRF models build from Kepler's\nFull Frame Images.\n\n# PRF models\n\nFirst we create PRF models using Kepler's FFI which contains ~10k Gaia EDR3 sources per Kepler's channel.\n\nThe following figure shows the PRF models in the focal plane. Channels at the border shows PRFs with very distorted shapes, while in the center these are round and smooth.\n\n![PRF Models](https://github.com/jorgemarpa/kepler-apertures/blob/main/docs/focal_plane_prf_model.png)\n\nLater this PRF models are used to compute apertures photometry.\n\n# Kepler's EXBA masks\n\nThe EXBA masks are custom apertures observed by Kepler's first mission, they cover relatively dark regions of the Kepler field and were observed continuously between quarters 4 and 17. The scientific motivation to collect these data was to obtain an unbiased characterization of the eclipsing binary occurrence fraction in the Kepler field.\n\nHere an example of the full EXBA mask observed in quarter 5 with channel 48\n\n![exba_ch48](https://github.com/jorgemarpa/kepler-apertures/blob/main/docs/EXBA_img_q5_ch48.png)\n\n# Dependencies\n* numpy\n* scipy\n* astropy\n* matplotlib\n* photutils\n* pandas\n* tqdm\n* patsy\n* pyia\n* lightkurve\n",
    'author': 'Jorge Martinez-Palomera',
    'author_email': 'jorgemarpa@ug.uchile.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorgemarpa/kepler-apertures',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
