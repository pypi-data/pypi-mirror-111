# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stimpy', 'stimpy.animate']

package_data = \
{'': ['*']}

install_requires = \
['PsychoPy>=2021.2.0,<2022.0.0', 'numpy>=1.21.0,<2.0.0']

extras_require = \
{'dev': ['black',
         'isort',
         'flake8',
         'mypy',
         'pydata-sphinx-theme',
         'sphinx',
         'sphinx-autodoc-typehints']}

setup_kwargs = {
    'name': 'stimpy',
    'version': '0.1.1',
    'description': 'A PsychoPy wrapper to create moving visual stimuli without loops.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/stimpy.svg)](https://pypi.python.org/pypi/stimpy)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/stimpy.svg)](https://pypi.python.org/pypi/stimpy)\n[![Documentation Status](https://readthedocs.org/projects/stimpy/badge/?version=latest)](https://stimpy.readthedocs.io/en/latest/?badge=latest)\n# StimPy\n\n[StimPy](https://github.com/kclamar/stimpy) is a thin [PsychoPy](https://www.psychopy.org/) wrapper to simplify the creation of visual stimuli.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install StimPy.\n\n```bash\npip install stimpy\n```\n\n## Usage\n\n```python\nimport stimpy as sp\n\ncircle = sp.visual.Circle(size=(2, 2), fillColor=(1, 1, 1),\n                          pos=sp.Animate([(-45, 0), (45, 0)], [2, 2]))\n\nstimuli = sp.Stimuli()\nstimuli.append(circle, begin=0, dur=10)\n\nwin = sp.Window(distance=13, width=26, units="degFlat")\ntrial = sp.Trial(stimuli, win=win)\ntrial.run()\n```\n',
    'author': 'Ka Chung Lam',
    'author_email': 'kclamar@connect.ust.hk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kclamar/stimpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
