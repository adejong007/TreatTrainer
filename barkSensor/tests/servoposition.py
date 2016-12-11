#!/usr/bin/env python
#
# This program is used to detect dog barking from a USB microphone
#
# Copyright 2016, Andrew DeJong, andrew.dejong5@gmail.com
# This software is is distributed under the terms of the full GNU General Public License
#
# Based on the alarmBeepDetector freely distributed by
# Benjamin Chodroff benjamin.chodroff@gmail.com

import pyaudio
import sqlite3
import wiringpi
from numpy import zeros,linspace,short,fromstring,hstack,transpose,log
from scipy import fft
from time import sleep,perf_counter


# Servo control variables
servoPin = 18
servoRest = 60

# Debugging variables
# Enable blip, beep, and reset debug output (useful for understanding when blips, beeps, and resets are being found)
debug=True
# Show the most intense frequency detected (useful for configuration of the frequency and beep lengths)
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(servoPin, 2)
iter=0
wiringpi.pwmSetMode(0)
wiringpi.pwmSetClock(384)
wiringpi.pwmSetRange(1000)


wiringpi.pwmWrite(servoPin, servoRest) # 50%
sleep(2)

wiringpi.digitalWrite(servoPin,0)
wiringpi.pinMode(servoPin,0)
