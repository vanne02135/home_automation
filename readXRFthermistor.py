#!/usr/bin/python

import serial
import datetime
import time
import thingspeak

devid = 'TA'
baud = 9600
port = "/dev/ttyACM0"
outfile = "thermistor.log"

ser = serial.Serial(port, baud)
ser.timeout = 0

# just copy paste from here to screen /dev/ttyACM0 9600 
# or ttyAMA0 on raspberry

COMMANDS = """
aTAINTVL005M
aTACYCLE----
"""

def parseLLAPTemp(msg):
	if not msg[0] == 'a':
		raise Exception("Not a LLAP message: %s" % msg)

	deviceName = msg[1:3]
	if msg[3:7] == 'TMPA':
		temperature = float(msg[7:])
	else:
		raise Exception("Unable to parse %s" % msg)	

	return (deviceName, temperature)


api_key = open("api_key.txt").read().strip()

while True:
	if ser.inWaiting() >= 12:
		now = datetime.datetime.now()
		msg = ser.readline()
		deviceName = None
		temperature = None
		try:
			[deviceName, temperature] = parseLLAPTemp(msg)
			logline = "%s %s %.3f" % (now, deviceName, temperature)
			fields = []
			if deviceName == "TA":
				fields[0] = temperature
			thingspeak.thingspeak.write(api_key, fields)
		except Exception as e:
			logline = "%s %s" % (now, e)
		open(outfile, "a").write(logline + "\n")
		print logline	

	time.sleep(1)	
