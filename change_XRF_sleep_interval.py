#!/usr/bin/python

import serial
import datetime
import time

baud = 9600
port = "/dev/ttyACM0"

ser = serial.Serial(port, baud)
ser.timeout = 0

def changeInterval(device_id, newinterval_string):
	# When in cyclic sleep mode, XRF wakes up for commands
	# every tenth cycle. It's awake only for 100 ms, so it 
	# needs commands right away. 
	# Every tenth cycle XRF broadcasts battery level as follows:
	# aTAAWAKE----aTABATT2.93-aTASLEEPING-

	# as it is only every tenth time, this function takes
	# on avg 5 times the current interval length to run. 

	# newinterval_string should
	# be something like "030S" for 30 seconds or "010M" for 10 minutes

	commandStr = "a" + device_id + "INTVL" + newinterval_string

	while True:
		if ser.inWaiting() >= 12:
			msgs = ser.readline()
			if msgs[1:3] == device_id and msgs[3:8] == "AWAKE":
				ser.write(commandStr)
				print "Transmitted new interval %s to device %s" % (device_id, newinterval_string)
				reply = ser.readline()
				now = datetime.datetime.now()
				if reply == commandStr:
					print "%s XRF acknowledged" % now
					break
				else:
					print "%s ERROR: no acknowledgement" % now
		time.sleep(0.001)
