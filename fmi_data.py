#!/usr/bin/python

# parse data received from finnish meteorologic institute (fmi)


import urllib2
from datetime import datetime

import xml.etree.cElementTree as et
import lxml.etree as et

data_fields = "air temperature, wind speed, gust speed, wind direction, relative humidity, dew point, one hour precipitation amount, precipitation intensity, snow depth, pressure reduced to sea level, visibility"
if __name__ == "__main__":
	fmi_api_key = open("fmi_api_key.txt").read().strip()

	# url for time series from Savilahti, Kuopio
	url = "http://data.fmi.fi/fmi-apikey/%s/wfs?request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&crs=EPSG::3067&fmisid=101586" % fmi_api_key

	xmldata = urllib2.urlopen(url).read()

	ns = {'wfs':'http://www.opengis.net/wfs/2.0', "om": "http://www.opengis.net/om/2.0", "omso": "http://inspire.ec.europa.eu/schemas/omso/2.0rc3", "wml2": "http://www.opengis.net/waterml/2.0"}
	
	tree = et.fromstring(xmldata)

	valueMatrix = []
	for result in tree.xpath("wfs:member/omso:PointTimeSeriesObservation/om:result", namespaces = ns):
		samplingTimes = []
		values = []
		for i in result.xpath("wml2:MeasurementTimeseries/wml2:point/wml2:MeasurementTVP/wml2:time", namespaces = ns):
			samplingTimes.append(datetime.strptime(i.text,'%Y-%m-%dT%H:%M:%SZ'))
	
		for i in result.xpath("wml2:MeasurementTimeseries/wml2:point/wml2:MeasurementTVP/wml2:value", namespaces = ns):
			values.append(float(i.text))

		valueMatrix.append(values)

	fieldnames = data_fields.split(",")

	print "Sampling time (UTC), %s, %s, %s" % (fieldnames[0], fieldnames[1], fieldnames[4])
	for i, st in enumerate(samplingTimes):
		print "%s %.2f %.2f %.2f" % (st, valueMatrix[0][i], valueMatrix[1][i], valueMatrix[4][i])

