#!/usr/bin/env python
#
# This program is used to detect dog barking from a USB microphone
#
# Copyright 2016, Andrew DeJong, andrew.dejong5@gmail.com
# This software is is distributed under the terms of the full GNU General Public License
#
# Based on the alarmBeepDetector freely distributed by
# Benjamin Chodroff benjamin.chodroff@gmail.com

import sqlite3
from time import perf_counter,time

print("Opening SQLite database...")
sqconn=sqlite3.connect('/var/www/databases/barkActivity.db')
sqcurs=sqconn.cursor()
print("Last entry: ")
for row in sqcurs.execute("SELECT * FROM sessions ORDER BY datetime DESC LIMIT 1"):
    print(row)
sqconn.close()


print("Bark detector working. Press CTRL-C to quit.")

rows= [(int(time()),0,1)]
for row in rows: 
    print(row)
    sqconn=sqlite3.connect('/var/www/databases/barkActivity.db', isolation_level=None)
    sqcurs=sqconn.cursor()
    sqcurs.execute('INSERT INTO sessions VALUES (?,?,?)',row)
    sqconn.close
