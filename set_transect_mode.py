from visca.optim import Optim
cam = Optim(output="/dev/ttyUSB0")
cam.init()
cam.set_wide_zoom()
cam.set_manual_AE()
cam.set_gain('6')
#cam.set_iris('F2.0')
cam.set_shutter_AE()
cam.set_shutter_speed('1/500')
