# visca
A Python library for controlling Sony VISCA cameras with specific classes for the DSPL Optim camera

# Installation

Run `pip install git+git://github.com/mbari-org/python-visca.git`.

# Usage

```
from optim import Optim
cam = Optim(output="/dev/ttyUSB0")
cam.init()
cam.set_wide_zoom()
cam.set_iris_AE()
cam.set_iris('F11')

```
