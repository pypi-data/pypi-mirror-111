[![PyPI version](https://badge.fury.io/py/stimpy.svg)](https://pypi.python.org/pypi/stimpy)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/stimpy.svg)](https://pypi.python.org/pypi/stimpy)
[![Documentation Status](https://readthedocs.org/projects/stimpy/badge/?version=latest)](https://stimpy.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
# StimPy

[StimPy](https://github.com/kclamar/stimpy) is a thin [PsychoPy](https://www.psychopy.org/) wrapper to simplify the creation of visual stimuli.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install StimPy.

```bash
pip install stimpy
```

## Usage

```python
import stimpy as sp

circle = sp.visual.Circle(
    size=(2, 2), fillColor=(1, 1, 1),
    pos=sp.Animate([(-40, -20), (-40, 20), (40, 20), (40, -20)], [1, 1, 1, 1])
)

scene = sp.Scene(color=(-1, -1, -1), units="deg")
scene.add(circle, begin=0, dur=4)

win = sp.Window(distance=13, width=26)
trial = sp.Trial(scene, win=win)
trial.start()

trial.save_movie("example.mp4", fps=60)

```
