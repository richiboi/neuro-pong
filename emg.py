"""
This class implements the EMG sensor
"""
from gpiozero import MCP3008
from time import sleep


class EMG:

    def __init__(self, selected_channel):
        self.adc = MCP3008(channel=selected_channel)

    # Scale the raw voltage to a number between -1 and 1
    def _scale_raw(self, raw):
        return 2 * raw - 1

    def read(self):
        # Only one thing in adc.values, but because this
        # is a generator, must access this way
        for voltage in adc.values:
            return self._scale_raw(voltage)
