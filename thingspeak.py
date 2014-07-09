# interface for thingspeak
#!/usr/bin/python

import urllib
import httplib


def thingspeak_write(api_key, fields):
	# write to thingspeak channel and return entry id (?)
	

	fieldDict = {}
	for i, f in enumerate(fields):
		fieldDict["field" + str(i+1)] = str(f)
	
	fieldDict["key"] = api_key

	#params = urllib.urlencode({'field1': str(field1), 'field2': str(field2), "key":api_key})
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
	api_key = open("api_key.txt").read().strip()

	now = datetime.datetime.now()

	entry_id = thingspeak_write(api_key, [now.minute, now.second])
	print "Succesfully written entry id %d" % entry_id




