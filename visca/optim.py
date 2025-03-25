import re
import binascii
import serial
from scipy.interpolate import interp1d

from visca.camera import Camera


class Optim(Camera):
    """ DSPL Optim camera interface class based on python-visca
    
        This class follows the FCB-ER8550_8530_Tech_Manual provided by DSPL and
        define tables to map from human readable camera settings to the hex values 
        used by VISCA.
        
        The interface requires a working serial connection between the host and the
        camera, typically /dev/ttyUSB0.
        
        Currently only a small subset of function and presents are defined.
    """

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
    
    """ Mapping from camera sensor gain in dB to hex setting """
    gain_table = {}
    gain_table['48'] = '11'
    gain_table['45'] = '10'
    gain_table['42'] = '0F'
    gain_table['39'] = '0E'
    gain_table['36'] = '0D'
    gain_table['33'] = '0C'
    gain_table['30'] = '0B'
    gain_table['27'] = '0A'
    gain_table['24'] = '09'
    gain_table['21'] = '08'
    gain_table['18'] = '07'
    gain_table['15'] = '06'
    gain_table['12'] = '05'
    gain_table['9'] = '04'
    gain_table['6'] = '03'
    gain_table['3'] = '02'
    gain_table['0'] = '01'
    
    """ Mapping from camera iris in f/# to hex setting """
    iris_table = {}
    iris_table['F2.0'] = '19'
    iris_table['F2.2'] = '18'
    iris_table['F2.4'] = '17'
    iris_table['F2.6'] = '16'
    iris_table['F2.8'] = '15'
    iris_table['F3.1'] = '14'
    iris_table['F3.4'] = '13'
    iris_table['F3.7'] = '12'
    iris_table['F4.0'] = '11'
    iris_table['F4.4'] = '10'
    iris_table['F4.8'] = '0F'
    iris_table['F5.2'] = '0E'
    iris_table['F5.6'] = '0D'
    iris_table['F6.2'] = '0C'
    iris_table['F6.8'] = '0B'
    iris_table['F7.3'] = '0A'
    iris_table['F7.8'] = '09'
    iris_table['F8.0'] = '08'
    iris_table['F9.6'] = '07'
    iris_table['F10'] = '06'
    iris_table['F11'] = '05'
    iris_table['CLOSE'] = '00'
    
    """ Mapping from camera zoom in x (times) to hex value """
    zoom_table = {}
    zoom_table['1x'] = '0000'
    zoom_table['2x'] = '0DC1'
    zoom_table['3x'] = '186C'
    zoom_table['4x'] = '2015'
    zoom_table['5x'] = '2594'
    zoom_table['6x'] = '29B7'
    zoom_table['7x'] = '2CFB'
    zoom_table['8x'] = '2FB0'
    zoom_table['9x'] = '2CFB'
    zoom_table['10x'] = '342D'
    zoom_table['11x'] = '3608'
    zoom_table['12x'] = '37AA'
    zoom_table['13x'] = '391C'
    zoom_table['14x'] = '3A66'
    zoom_table['15x'] = '3B90'
    zoom_table['16x'] = '3C9C'
    zoom_table['17x'] = '3D91'
    zoom_table['18x'] = '3E72'
    zoom_table['19x'] = '3F40'
    zoom_table['20x'] = '4000'
    
    """ Mapping from camera focus position to hex value """
    focus_table = {}
    focus_table['100m'] = '1000'
    focus_table['10m'] = '2000'
    focus_table['5m'] = '3000'
    focus_table['3.3m'] = '4000'
    focus_table['2.5m'] = '5000'
    focus_table['2.0m'] = '6000'
    focus_table['1.7m'] = '7000'
    focus_table['2.5m'] = '5000'
    focus_table['1.5m'] = '8000'
    focus_table['1.0m'] = '9000'
    focus_table['0.5m'] = 'A000'
    focus_table['0.3m'] = 'B000'
    focus_table['15cm'] = 'C000'
    focus_table['6cm'] = 'D000'
    focus_table['1cm'] = 'E000'

    def __init__(self, output='/dev/ttyUSB0'):
        """Sony VISCA control class.

        :param output: Serial port string. (default: 'COM1')
        :type output: str
        """
        super(self.__class__, self).__init__(output=output)

    def init(self):
        """Initializes camera object by connecting to serial port.

        :return: Camera object.
        :rtype: Camera
        """
        super(self.__class__, self).init()
        return self
    
    def command(self, com):
        """Sends hexadecimal string to serial port.

        :param com: Command string. Hexadecimal format.
        :type com: str
        :return: Success.
        :rtype: bool
        """
        try:
            self._output.write(binascii.unhexlify(com))
            return self.read()
        except Exception as e:
            print (com, e)
            return False

    def comm(self, com):
        """Sends hexadecimal string to serial port.

        :param com: Command string. Hexadecimal format.
        :type com: str
        :return: Success.
        :rtype: bool
        """
        super(self.__class__, self).command(com)

    def set_manual_AE(self):
        """Set the camera to manual control of iris, gain, and exposure
        """
        return self.command('8101043903FF')
    
    def set_auto_AE(self):
        """Set the camera to auto control of iris, gain, and exposure
        """
        return self.command('8101043900FF')
    
    def set_shutter_AE(self):
        """Set the camera to auto exposure with shutter priority
        """
        return self.command('810104390AFF')
    
    def set_gain_AE(self):
        """Set the camera to auto exposure with gain priority
        """
        return self.command('810104390EFF')
    
    def set_iris_AE(self):
        """Set the camera to auto exposure with iris priority
        """
        return self.command('810104390BFF')
        
    def turn_off_noise_reduction(self):
        """Set the NR to zero
        """
        return self.command('8101045300FF')
    
    def set_direct_value(self, base_hex, direct_value):
        """ Set a direct value for camera parameter like gain, shutter speed or iris
        
        Args:
            base_hex (str): The address of the parameter
            direct_vale (str): the two char value to set from table
        """
        cmd = base_hex + '0' + direct_value[0] + '0' + direct_value[1] + 'FF'
        # print(cmd)
        return self.command(cmd)

    def set_direct_focus(self, base_hex, direct_value):
        """ Set a direct value for camera parameter like gain, shutter speed or iris
        
        Args:
            base_hex (str): The address of the parameter
            direct_vale (str): the two char value to set from table
        """
        cmd = base_hex + '0' + direct_value[0] + '0' + direct_value[1]  + '0' + direct_value[2] + '0' + direct_value[3] + 'FF'
        # print(cmd)
        return self.command(cmd)

    def set_direct_zoom(self, base_hex, direct_value):
        """ Set a direct value for camera parameter like gain, shutter speed or iris

        Args:
            base_hex (str): The address of the parameter
            direct_vale (str): the two char value to set from table
        """
        cmd = base_hex + '0' + direct_value[0] + '0' + direct_value[1]  + '0' + direct_value[2] + '0' + direct_value[3] + 'FF'
        # print(cmd)
        return self.command(cmd)

    
    def set_focus(self, focus):
        """ Set the camera sensor iris when in manual mode
        
        Args:
            focus (str): lens focus distance value (see table)
        """
        if focus in self.focus_table:
            return self.set_direct_focus('81010448', self.focus_table[focus])
   
    def set_zoom(self, zoom):
        """ Set the camera sensor iris when in manual mode
        
        Args:
            focus (str): lens focus distance value (see table)
        """
        if zoom in self.zoom_table:
            return self.set_direct_focus('81010447', self.zoom_table[zoom])

    
    def set_shutter_speed(self, speed):
        """set the shutter speed on the camera when in manual mode

        Args:
            speed (str): shutter speed in 1/s
        """
        if speed in self.speed_table:
            return self.set_direct_value('8101044A0000', self.speed_table[speed])
        
    def set_gain(self, gain):
        """ Set the camera sensor gain when in manual mode
        
        Args:
            gain (str): sensor gain in dB
        """
        if gain in self.gain_table:
            return self.set_direct_value('8101044C0000', self.gain_table[gain])
        
    def set_iris(self, iris):
        """ Set the camera sensor iris when in manual mode
        
        Args:
            iris (str): sensor iris in F/#
        """
        if iris in self.iris_table:
            return self.set_direct_value('8101044B0000', self.iris_table[iris])

    def set_auto_focus(self):
        """set the camera to auto focus mode
        """
        return self.command('8101043802FF') # manual focus
    
    def set_manual_focus(self):
        """set the camera to manual focus mode
        """
        return self.command('8101043803FF') # manual focus

    def set_far_focus(self):
        """set the camera to far focus
        """
        return self.command('8101040827FF') # fastest focus speed

    def set_near_focus(self):
        """set the camera to near focus
        """
        return self.command('8101040837FF') # fastest focus speed
    
    def set_wide_zoom(self):
        """Set full wide zoom on the camera
        """
        return self.command('8101040737FF') # fastest zoom speed
    
    def set_tele_zoom(self):
        """Set full tele zoom on the camera
        """
        return self.command('8101040727FF') # fastest zoom speed
    
    def set_ICR_On(self):
        """Set the ICR mode
        """
        return self.command('8101040102FF')
    
    def set_ICR_Off(self):
        """Set the ICR mode
        """
        return self.command('8101040103FF')
    
