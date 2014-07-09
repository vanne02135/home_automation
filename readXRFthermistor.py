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

# TODO parse concatenated messages like this
# 2014-07-09 22:08:51.731778 invalid literal for float(): 28.09aTAAWAKE----aTABATT2.93-aTASLEEPING-

# just copy paste from here to screen /dev/ttyACM0 9600 
# or ttyAMA0 on raspberry

COMMANDS = """
aTAINTVL005M
aTACYCLE----
"""

def parseLLAP(msg):
	if not msg[0] == 'a':
		raise Exception("Not a LLAP message: %s" % msg)

	temperature = None
	battery = None

	deviceName = msg[1:3]
	if msg[3:7] == 'TMPA':
		temperature = float(msg[7:12])
	elif msg[3:7] == 'BATT':
		battery = float(msg[7:-1])
	else:
		raise Exception("Unable to parse %s" % msg)	

	return (deviceName, temperature, battery)

if __name__ == "__main__":

	api_key = open("api_key.txt").read().strip()

	while True:
		if ser.inWaiting() >= 12:
			# TODO split concatenated messages here. Temp & Battery value
			# should be posted in one call to thingspeak (15s min update interval)
			now = datetime.datetime.now()
			msg = ser.readline()
			print "%s inbound message: %s" % (now, msg)
			deviceName = None
			temperature = None
			try:
				[deviceName, temperature, battery] = parseLLAP(msg)
				logline = "%s %s %.3f %s" % (now, deviceName, temperature, battery)
				# battery value not yet xferd to thingspeak
				fields = [0]
				if deviceName == "TA":
					fields[0] = temperature
				thingspeak.thingspeak_write(api_key, fields)
			except Exception as e:
				logline = "%s %s" % (now, e)
			open(outfile, "a").write(logline + "\n")
			print logline	

		time.sleep(1)


