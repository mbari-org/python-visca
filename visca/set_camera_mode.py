import sys
from visca import camera

cam = camera.D100(output="/dev/ttyUSB0")
cam.init()
cam.comm(sys.argv[1])
print(cam.read(amount=3))



tethysadmin@ikshana:~/software/optim-interface/python-visca$ workon optim-interface
(optim-interface) tethysadmin@ikshana:~/software/optim-interface/python-visca$ python test.py 8101043903FF
9041ff
(optim-interface) tethysadmin@ikshana:~/software/optim-interface/python-visca$ python test.py 8101044A00000104FF
9041ff
(optim-interface) tethysadmin@ikshana:~/software/optim-interface/python-visca$ python test.py 8101044C00000005FF
9041ff
(optim-interface) tethysadmin@ikshana:~/software/optim-interface/python-visca$ python test.py 8101044B00000109FF