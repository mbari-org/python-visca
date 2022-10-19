import sys
from visca import camera

cam = camera.D100(output="/dev/ttyUSB0")
cam.init()
cam.comm(sys.argv[1])
print(cam.read(amount=3))