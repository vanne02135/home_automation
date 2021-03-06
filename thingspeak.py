# interface for thingspeak
#!/usr/bin/python

import urllib
import httplib


def thingspeak_write(api_key, fields):
	# write to thingspeak channel and return entry id on succesful update,
	# raise exception on failed update
	

	fieldDict = fields

	fieldDict["key"] = api_key

	
	params = urllib.urlencode(fieldDict)


	# Other code to send information to ThingSpeak
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain", "X-THINGSPEAKKEY": api_key}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	conn.request("POST", "/update", params, headers)
	response = conn.getresponse()
	data = int(response.read())

	conn.close()

	if data == 0:
		raise Exception("Error writing to ThingSpeak")	

	return data


if __name__ == "__main__":
	import datetime
	try:
		api_key = open("api_key.txt").read().strip()
	except:
		raise Exception("API key for testing should be in api_key.txt")

	now = datetime.datetime.now()

	entry_id = thingspeak_write(api_key, [now.minute, now.second])
	print "Succesfully written entry id %d" % entry_id




