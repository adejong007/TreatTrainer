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
from numpy import zeros,linspace,short,fromstring,hstack,transpose,log
from scipy import fft
from time import sleep


# BARK DETECTION VARIABLES
#Volume Sensitivity, 0.05: Extremely Sensitive, may give false alarms
#             0.1: Probably Ideal volume
#             1: Poorly sensitive, will only go off for relatively loud
SENSITIVITY= 1
# Alarm frequency (Hz) to detect (Set frequencyoutput to True if you need to detect what frequency to use)
TONE = 1500
#Bandwidth for detection (i.e., detect frequencies +- within this margin of error of the TONE)
BANDWIDTH = 500
#How many 46ms blips before we declare a bark?
barklength=3
# How many clear blips before we reset session detection
maxBarkGap=30
# How long of consistent barking defines a session
minSessionTime=10
# How long of silense until session is over
minQuiteTime=5
# How long after a reward until another reward is possible
rewardCooldown=300
# How many false 46ms blips before we declare there are no more beeps? (May need to be increased if there are expected long pauses between beeps) 
resetlength=10
# How many reset counts until we clear an active alarm? (Keep the alarm active even if we don't hear this many beeps)
clearlength=30
# Enable blip, beep, and reset debug output (useful for understanding when blips, beeps, and resets are being found)
debug=True
# Show the most intense frequency detected (useful for configuration of the frequency and beep lengths)
frequencyoutput=True

print("Opening audio stream...")
# Audio Sampler
NUM_SAMPLES = 2048
SAMPLING_RATE = 48000
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  input_device_index=2,
                  frames_per_buffer=NUM_SAMPLES)

print("Opening SQLite database...")
sqconn=sqlite3.connect('../web/db/barkActivity.db')
sqcurs=sqconn.cursor()
print("Last entry: ")
for row in sqcurs.execute("SELECT * FROM sessions WHERE bdate = (SELECT MAX(bdate) FROM sessions) ORDER BY btime DESC LIMIT 1"):
    print(row)

sqconn.close()

print("Alarm detector working. Press CTRL-C to quit.")

barkcount=0
resetcount=0
barkGap=0
inSession=False
sessionStart=0
lastReward=0

beepcount=0
clearcount=0
alarm=False

while True:
    while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
    audio_data  = fromstring(_stream.read(
         _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
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
    if max(intensity[(frequencies < TONE+BANDWIDTH) & (frequencies > TONE-BANDWIDTH )]) > max(intensity[(frequencies < TONE-1000) & (frequencies > TONE-2000)]) + SENSITIVITY:
        if frequencyoutput:
            print "\t\t\t\tfreq=",thefreq
        barkcount+=1
	#if this is the first blip, check barkgap
        if resetcount!=0:
            thisBark=time.perf_counter()
	    #if gap is big, then this is the beginning of session
            if (thisBark-lastBark > minBarkGap):
		sessionStart=thisBark
        resetcount=0
        if debug: print "\t\tBlip",blipcount
        if (barkcount>=barklength):
            blipcount=0
            resetcount=0
            lastBark=
            if debug: print "\tBark",beepcount
            if (beepcount>=alarmlength):
                clearcount=0
                alarm=True
                print "Alarm!"
                beepcount=0
    else:
        if frequencyoutput:
            print "\t\t\t\tfreq="
        blipcount=0
        resetcount+=1
        if debug: print "\t\t\treset",resetcount
        if (resetcount>=resetlength):
            resetcount=0
            beepcount=0
            if alarm:
                clearcount+=1
                if debug: print "\t\tclear",clearcount
                if clearcount>=clearlength:
                    clearcount=0
                    print "Cleared alarm!"
                    alarm=False

    sleep(0.01)
