import time
import datetime
from visca.optim import Optim
cam = Optim(output="/dev/ttyUSB0")
cam.init()


loop_delay = 5.0
log_file = './optim_camera_log.txt'

try:
    while True:
        with open(log_file, "a") as log:

            log.write("################\r\n")
            log.write(str(datetime.datetime.now()) + "\r\n")
            log.write(cam.command('81097E7E00FF') + "\r\n")
            log.write(cam.command('81097E7E01FF') + "\r\n")
            log.write(cam.command('81097E7E02FF') + "\r\n")
            log.write(cam.command('81097E7E03FF') + "\r\n")

        time.sleep(loop_delay)

except KeyboardInterrupt:
    pass


