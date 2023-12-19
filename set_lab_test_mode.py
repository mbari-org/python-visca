from visca.optim import Optim
cam = Optim(output="/dev/ttyUSB0")
cam.init()
print(cam.set_wide_zoom())
cam.set_iris_AE()
cam.set_iris('F11')
