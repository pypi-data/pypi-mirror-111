# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peakfit']

package_data = \
{'': ['*']}

install_requires = \
['lmfit>=1.0.2,<2.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'nmrglue>=0.8,<0.9',
 'numpy>=1.20.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0']

entry_points = \
{'console_scripts': ['peakfit = peakfit.peakfit:main',
                     'plot_cest = peakfit.plot_cest:main',
                     'plot_cpmg = peakfit.plot_cpmg:main']}

setup_kwargs = {
    'name': 'peakfit',
    'version': '0.2.0.dev2',
    'description': 'PeakFit allow for lineshape fitting in pseudo-3D NMR spectra.',
    'long_description': '## Synopsis\n\nPeakFit allow for lineshape fitting in pseudo-3D NMR spectra.',
    'author': 'Guillaume Bouvignies',
    'author_email': 'gbouvignies@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gbouvignies/PeakFit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
