from gpiozero import MCP3008
from time import sleep

adc = MCP3008(channel=0)

for voltage in adc.values:
    print('Reading: ', adc.values)
    sleep(0.5)
