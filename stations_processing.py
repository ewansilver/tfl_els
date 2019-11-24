import xml.etree.ElementTree as ET
import csv
import urllib.request
import shutil

# Download the stations xml from :http://tfl.gov.uk/tfl/syndication/feeds/stations.kml and save it as stations.kml.
# Run the file: python3 ./stations_processing.py
# and you will get a CSV called stations.csv in your directory.
# CSV format is :STATION NAME, LAT, LONG

def get_station_locations(file):
	tree = ET.parse(file)
	stations = []
	root = tree.getroot()

	for member in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
		location = []
		nameElement = member.find('.//{http://www.opengis.net/kml/2.2}name')
		coordinatesElement = member.find('.//{http://www.opengis.net/kml/2.2}coordinates')

		name = nameElement.text.strip()
		coords = []
		for c in coordinatesElement.text.strip().split(','):
			coords.append(float(c))

		location.append(name)
		location.append(coords[0])
		location.append(coords[1])
		location.append(coords[2])
		stations.append(location)
	return stations

def save_station_locations(locations, file):
# open a file for writing
	location_data = open(file, 'w')
# create the csv writer object
	csvwriter = csv.writer(location_data)
	for location in locations:
		print(location)
		csvwriter.writerow(location)
	location_data.close()


locations = get_station_locations("./stations.kml")
save_station_locations(locations, './stations.csv')