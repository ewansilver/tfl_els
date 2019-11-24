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


# Find the further points North, East, South and  West
def find_furthest_points(locations):
	north = -360
	south = 360
	east = -360
	west = 360
	for location in locations:
		longitude = location[1]
		latitude = location[2]
		if latitude > north:
			north = latitude
		if latitude < south:
			south = latitude
		if longitude > east:
			east = longitude
		if longitude < west:
			west = longitude

	return north, east, south, west

def get_grid_point(latitude, longitude, north, south, east, west, maxX, maxY):
	yLength = north - south
	xLength = east - west

	xPos = ((longitude - west) / xLength) * maxX
	yPos = ((north - latitude)/ yLength) * maxY

	return xPos, yPos


locations = get_station_locations("./stations.kml")
save_station_locations(locations, './stations.csv')
north, east, south, west = find_furthest_points(locations)



print('North:' + str(north))
print('South:' + str(south))
print('East:' + str(east))
print('West:' + str(west))

maxX = 1000
maxY = 1000
for location in locations:
	longitude = location[1]
	latitude = location[2]

	x,y = get_grid_point(latitude, longitude, north, south, east, west, maxX, maxY)

	print(str(x) + " "+ str(y))