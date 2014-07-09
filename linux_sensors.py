#!/usr/bin/python
# Read Linux system parameters and upload to thingspeak

import subprocess
import time
from thingspeak import thingspeak_write

def parseSensors(sensors_stdout):
	sensors = {}
	for line in sensors_stdout.split("\n"):
		if line.startswith("Core 0"):
			sensors["core0"] = float(line[7:20])
		if line.startswith("Core 1"):
			sensors["core1"] = float(line[7:20])

		if line.startswith("fan2:"):
			sensors["fan2"] = int(line[7:18])
		if line.startswith("CPUTIN:"):
			sensors["CPUTIN"] = float(line[7:20])

	return sensors


def getSensors():
	sensors = subprocess.Popen(["sensors"], stdout = subprocess.PIPE)
	sensors.wait()
	return sensors.stdout.read()

def TempsAndFan():
	mystr = getSensors()
	return parseSensors(mystr)

def uptime():
	uptime = subprocess.Popen(["uptime"], stdout = subprocess.PIPE)
	uptime.wait()
	mystr = uptime.stdout.read()

	avg1 = mystr.split(" ")[-3]
	avg5 = mystr.split(" ")[-2]
	avg15 = mystr.split(" ")[-1]
	return (avg1, avg5, avg15)

if __name__ == "__main__":
	api_key = open("linux_sensors_api_key.txt").read().strip()
	while True:
		temps = TempsAndFan()
		loadavgs =  uptime()
		data = [temps["CPUTIN"], temps["core0"], temps["core1"], temps["fan2"], loadavgs[0], loadavgs[1], loadavgs[2]]
		entry_id = thingspeak_write(api_key, data)
		print "%d linux sensor entries" % entry_id
		time.sleep(20)


			

