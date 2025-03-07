import re
import binascii
import serial
from scipy.interpolate import interp1d


class Camera(object):
    _input = None
    _output = None
    _output_string = None
    _input_string = None

    def __init__(self, output='COM1'):
        """Sony VISCA control class.

        :param output: Outbound serial port string. (default: 'COM1')
        :type output: str
        """
        self._output_string = output
        # self._input_string = input

    def init(self):
        """Initializes camera object by connecting to serial port.

        :return: Camera object.
        :rtype: Camera
        """
        # self._input = serial.Serial(self._input_string)
        self._output = serial.Serial(self._output_string, 9600, timeout=1)

    def command(self, com):
        """Sends hexadecimal string to serial port.

        :param com: Command string. Hexadecimal format.
        :type com: str
        :return: Success.
        :rtype: bool
        """
        try:
            self._output.write(binascii.unhexlify(com))
            return True
        except Exception as e:
            print (com, e)
            return False

    @staticmethod
    def close(serial_port):
        """Closes current serial port.

        :param serial_port: Serial port to modify.
        :return: True if successful, False if not.
        :rtype: bool
        """
        if serial_port.isOpen():
            serial_port.close()
            return True
        else:
            print ("Error closing serial port: Already closed.")
            return False

    @staticmethod
    def open(serial_port):
        """Opens serial port.

        :param serial_port: Serial port to modify.
        :return: True if successful, False if not.
        :rtype: bool
        """
        if not serial_port.isOpen():
            serial_port.open()
            return True
        else:
            print ("Error opening serial port: Already open.")
            return False

    def read(self, amount=3):
        total = ""
        while True:
            msg = binascii.hexlify(self._output.read()).decode("utf-8")
            total = total + msg
            #print(msg)
            if len(msg) == 0:
                break
        return total
