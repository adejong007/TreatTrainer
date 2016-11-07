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
from time import time,sleep,perf_counter
from subprocess import call
from os import environ

#-------------------------------------------------------------------------------------
#
#    Calibration Variables
#
#-------------------------------------------------------------------------------------

# Noise Detection Variables
#Volume Sensitivity, 0.05: Extremely Sensitive, may give false alarms
#             0.1: Probably Ideal volume
#             1: Poorly sensitive, will only go off for relatively loud
SENSITIVITY= 0.2
# Alarm frequency (Hz) to detect (Set frequencyoutput to True if you need to detect what frequency to use)
TONE = 1500
#Bandwidth for detection (i.e., detect frequencies +- within this margin of error of the TONE)
BANDWIDTH = 500

# Bark Trainer Logic Variables
#How many 46ms blips before we declare a bark?
barklength=3
# How many clear blips in between barks clears the session test
maxBarkGap=7
# How long of consistent barking defines a session
minSessionTime=30
# How long of silense until session is over
resetlength=100
# How long after a reward until another reward is possible
rewardCooldown=300

# Servo control variables
servoPin = 18
servoRest = 60
servoDump = 110

# LED control variables
redPin = 16
greenPin = 21
bluePin = 20
ledON = 1
ledOFF = 0

# Debugging variables
# Enable blip, beep, and reset debug output (useful for understanding when blips, beeps, and resets are being found)
debug=True
# Show the most intense frequency detected (useful for configuration of the frequency and beep lengths)
frequencyoutput=True


#-------------------------------------------------------------------------------------
#
#    Setup
#
#-------------------------------------------------------------------------------------

# Functions
def led(color):
    wiringpi.digitalWrite(redPin,ledOFF)
    wiringpi.digitalWrite(greenPin,ledOFF)
    wiringpi.digitalWrite(bluePin,ledOFF)
    if(color=='red'): wiringpi.digitalWrite(redPin,ledON)
    if(color=='green'): wiringpi.digitalWrite(greenPin,ledON)
    if(color=='blue'): wiringpi.digitalWrite(bluePin,ledON)



print("------------------------------------------------------------")
print("                        BarkDetector                        ")
print("                   a TreatTrainer product                   ")
print("------------------------------------------------------------")
print("(C) Andrew DeJong, distributed under the LGPL               ")
print("")
print("")
print("Initializing...")
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(redPin,1)
wiringpi.pinMode(greenPin,1)
wiringpi.pinMode(bluePin,1)
led('red')

print("Configuring PWM servo pin...")
wiringpi.pinMode(servoPin, 2)
wiringpi.pwmSetMode(0)
wiringpi.pwmSetClock(384)
wiringpi.pwmSetRange(1000)

print("Opening SQLite database...")
sqconn=sqlite3.connect('/var/www/databases/barkActivity.db')
sqcurs=sqconn.cursor()
print("Last entry: ")
for row in sqcurs.execute("SELECT * FROM sessions ORDER BY datetime DESC LIMIT 1"):
    print(row)
sqconn.close()

print("Writing parameter files...")
f = open('messages.sh','w')
f.write('barkstop=False')
f.close()
f = open('status','w')
f.write('0')
f.close()


print("Opening audio stream...")
# Audio Sampler
NUM_SAMPLES = 1024
SAMPLING_RATE = 24000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  input_device_index=2,
                  frames_per_buffer=NUM_SAMPLES)

print("Bark detector working. Press CTRL-C to quit.")
now=perf_counter()
barkcount=0
resetcount=0
isQuiet=True
inSession=False
sessionStart=now
sessionEnd=0
sessionTime=0
lastBark=now
barkStart=now
thisBark=now
lastReward=0
wasRewarded=0


#-------------------------------------------------------------------------------------
#
#    Loop
#
#-------------------------------------------------------------------------------------
led('green')

barkstop = False
while not barkstop:

    now = perf_counter()

    # Read in variables from messages.sh
    # Quit if barkstop is set
    with open('./messages.sh') as messageFile:
        exec(messageFile.read())
 
    # Get audio samples
    nAvailable = _stream.get_read_available()
    if(nAvailable < NUM_SAMPLES):
        sleep(0.01)
        continue
    try:
        audio_string = _stream.read(nAvailable)
    except IOError:
        print('Stream overload. Emptied.')
        continue


    audio_data  = fromstring( audio_string, dtype=short)[-NUM_SAMPLES:]
    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0
    intensity = abs(fft(normalized_data))[:NUM_SAMPLES/2]
    frequencies = linspace(0.0, float(SAMPLING_RATE)/2, num=NUM_SAMPLES/2)
    if frequencyoutput:
        which = intensity[1:].argmax()+1
        # use quadratic interpolation around the max
        if which != len(intensity)-1:
            y0,y1,y2 = log(intensity[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*SAMPLING_RATE/NUM_SAMPLES
        else:
            thefreq = which*SAMPLING_RATE/NUM_SAMPLES

    # If sound is detected
    if max(intensity[(frequencies < TONE+BANDWIDTH) & (frequencies > TONE-BANDWIDTH )]) > max(intensity[(frequencies < TONE-1000) & (frequencies > TONE-2000)]) + SENSITIVITY:
        if frequencyoutput:
            print("\t\t\t\tfreq=",thefreq)
        resetcount=0
        barkcount+=1
        #if not currently in a session, determine if this is a real bark
        if not inSession:
            led('blue')
            #if this is the first blip, record the start of this bark
            if (barkcount == 1):
                lastBark = thisBark
                barkStart = now
            #if multiple blips, then this is a bark, not a false positive,
            elif (barkcount>=barklength):
                thisBark = barkStart
                if debug: print("\tBark",barkcount)
                #if gap is big, then this is the potential beginning of a new session
                if (thisBark-lastBark > maxBarkGap):
                    sessionStart = thisBark
                #if gap is small, and this has been going on for awhile, then this is a session
                elif (thisBark - sessionStart > minSessionTime):
                    led('red')
                    inSession=True
                    if debug: print("Barking Session!")

    # If no sound detected
    else:
        if frequencyoutput:
            print("\t\t\t\tfreq=")
        barkcount=0
        #if currently in a barking session
        if inSession:
            resetcount+=1
            if debug: print("\t\t\treset",resetcount)
            #if long quiet, end session
            if (resetcount >= resetlength):
                led('green')
                if debug: print("Cleared")
                inSession = False
                sessionEnd = now
                sessionTime = sessionEnd-sessionStart
                #if no recent treat, give treat
                if (sessionEnd-lastReward) > rewardCooldown:
                    if debug: print("\tReward")
                    wasRewarded = 1
                    lastReward = sessionEnd
                    wiringpi.pwmWrite(servoPin, servoDump) # Dump position
                    sleep(0.5)
                    wiringpi.pwmWrite(servoPin, servoRest) # Rest position
                else:
                    wasRewarded=0
                rows= [(int(time()),int(sessionTime),int(wasRewarded))]
                for row in rows: 
                    print(row)
                    sqconn=sqlite3.connect('/var/www/databases/barkActivity.db', isolation_level=None)
                    sqcurs=sqconn.cursor()
                    sqcurs.execute('INSERT INTO sessions VALUES (?,?,?)',row)
                    sqconn.close
        else:
            resetcount = 0
            led('green')            
    sleep(0.01)


#-------------------------------------------------------------------------------------
#
#    Exit
#
#-------------------------------------------------------------------------------------

# Stop PWM
wiringpi.digitalWrite(servoPin,0)
wiringpi.pinMode(servoPin,0)

for letter in "goodbye":
    led('red')
    print(letter)
    sleep(0.5)
    led('off')
    sleep(0.5)




