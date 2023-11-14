from visca.camera import Camera

class Optim(Camera):

    """ Mapping from shutter speed to hex setting """
    speed_table = {}
    speed_table['1/10000'] = '21'
    speed_table['1/6000'] = '20'
    speed_table['1/4000'] = '1F'
    speed_table['1/3000'] = '1E'
    speed_table['1/2000'] = '1D'
    speed_table['1/1500'] = '1C'
    speed_table['1/1000'] = '1B'
    speed_table['1/725'] = '1A'
    speed_table['1/500'] = '19'
    speed_table['1/350'] = '18'
    speed_table['1/250'] = '17'
    speed_table['1/180'] = '16'
    speed_table['1/125'] = '15'
    speed_table['1/100'] = '14'
    speed_table['1/90'] = '13'
    speed_table['1/60'] = '12'
    speed_table['1/50'] = '11'
    speed_table['1/30'] = '10'
    speed_table['1/20'] = '0F'
    speed_table['1/15'] = '0E'
    speed_table['1/10'] = '0D'
    speed_table['1/8'] = '0C'
    speed_table['1/6'] = '0B'
    speed_table['1/4'] = '0A'
    speed_table['1/3'] = '09'
    speed_table['1/2'] = '08'
    speed_table['2/3'] = '07'
    speed_table['1/1'] = '06'


    def __init__(self, output):
        """Init the camera object with the specified serial output

        Args:
            output (str): path to the serial output file (eg. COM1 or /dev/ttyUSB0)
        """
        super(output)

    def set_shutter_speed(self, speed):
        """set the shutter speed on the camera when in manual mode

        Args:
            speed (str): shutter speed in 1/s
        """
        if speed in speed_table:
            cmd = '8101044A0000' + '0' + speed_table[speed][0] + '0' + speed_table[speed][1] + 'FF'
            



    