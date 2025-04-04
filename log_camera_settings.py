import time
import datetime
from visca.optim import Optim
cam = Optim(output="/dev/ttyUSB0")
cam.init()


loop_delay = 10.0
loop_counter = 0
log_file = 'logs/' + str(int(time.time())) + '_optim_camera_log.txt'


cam_control_auto = True

try:
    while True:

        # Log the camera settings
        with open(log_file, "a") as log:

            log.write("################\r\n")
            timestamp = str(datetime.datetime.now())
            print(timestamp)
            log.write(timestamp + "\r\n")
            log.write(cam.command('81097E7E00FF') + "\r\n")
            log.write(cam.command('81097E7E01FF') + "\r\n")
            log.write(cam.command('81097E7E02FF') + "\r\n")
            log.write(cam.command('81097E7E03FF') + "\r\n")

        # Periodically reset camera settings in case they don't take
        if loop_counter % 3 == 0:
            with open(log_file, "a") as log:
                log.write('#resetting camera settings...\r\n')
            
            if not cam_control_auto:
                # Set the camera config
                cam.set_wide_zoom()
                cam.set_manual_AE()
                # Let the gain and iris auto
                cam.set_gain('6')
                cam.set_iris('F2.0')
                #cam.set_shutter_AE()
                cam.set_shutter_speed('1/125')
                cam.set_manual_focus()
                cam.set_focus('100m')
                cam.turn_off_noise_reduction()
            else:
                # Set the camera config
                cam.set_wide_zoom()
                cam.set_auto_AE()
                # Let the gain and iris auto
                cam.set_gain_limit('9') # the lowest gain limit setting
                cam.set_iris('F2.0')
                #cam.set_shutter_AE()
                cam.set_min_shutter('1/125')
                cam.set_manual_focus()
                cam.set_focus('100m')
                cam.turn_off_noise_reduction()

        loop_counter += 1
        
        time.sleep(loop_delay)

except Exception as e:
    print(e)


