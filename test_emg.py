"""
Test program to test the EMG class
"""

from emg import EMG
from time import sleep

emg = EMG(0)

while 1:
    print(emg.read())
    sleep(0.5)
