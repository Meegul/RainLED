import requests
import json
import math
import time
import sys

#Debugging function that prints each rainstation's lats and lons
def printCoords(array):
    for i in array:
        lat = i['station']['coord']['lat']
	lon = i['station']['coord']['lon']
	print "(" + str(lat) + "," + str(lon) + ")"

#Takes rain data and determines if an LED should turn on
def shouldTurnOn(rain):
    return 1 if rain > .5 else 0

#-----CONFIGURATION-VARIABLES-----#
#Configure these to suit your needs
APIKey = ''
latitude = ''
longitude = ''
#---------------------------------#

payload = {'lat': latitude,'lon': longitude, 'cnt': 50, 'APPID': APIKey}
url = 'http://api.openweathermap.org/data/2.5/station/find'

#Determines if too many arguments were passed
if (len(sys.argv) > 3):
    print "Usage: python main.py [dimension 3-9 (3 for 3x3)(defaults to 5x5)] [log (optional)]"
    quit()

#Determines what the inputted dimension is
#If none was given, default to 5
if (len(sys.argv) > 1):
    try:
        dimension = int(float(sys.argv[1]))
    except ValueError:
        dimension = 5
else: dimension = 5

#ensures dimension is at least 3
if (dimension < 3):
    dimension = 5

#Ensures dimension is odd
#This ensures there's a center
if (dimension % 2 == 0):
    dimension += 1

#Determines whether the user specified whether the program
#should log the output to logs.txt
if ('log' in sys.argv):
	toLog = 1
else: toLog = 0

#Primary loop that continues until a keyboard interrupt occurs
while (1):
	if(toLog):
		log = open('logs.txt' , 'a')
		log.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) + "\n")
                print "Logging..."
	print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

        r = []
	temp = requests.get(url, params=payload)

        #requests data from spots:
        #X-X-X
        #-----
        #X-X-X
        #-----
        #X-X-X
        for y in range(3):
            for x in range(3):
                payload = {'lat': str(float(latitude) + x - 1),'lon': str(float(longitude) - y + 1), 'cnt': 50, 'APPID': APIKey}
                temp = requests.get(url, params=payload)
                for n in temp.json():
                    if (n not in r):
                        r.append(n)
        counter = 0
	rainStations = []

        #finds stations that contain rain data
	for i in range(len(r)):
            try:
		x = r[i]['last']['rain']['1h']
		#ensures no duplicates
		if not(r[i] in rainStations):
		    rainStations.append(r[i])
		    counter += 1
	    except KeyError: pass

        #5x5 Array index example:
	#0  1  2  3  4
	#5  6  7  8  9
        #10 11 12 13 14
	#15 16 17 18 19
        #20 21 22 23 24
	array = []
        smallestDistances = []
        for i in range(pow(dimension, 2)):
            array.append(-1)
            smallestDistances.append(100)

        #Chooses a station closest to each location shown here in a 5x5 example:
	#(-100km, +100km) (-50km, +100km) (+0km, +100km) (+50km, +100km) (+100km, +100km)
        #(-100km, +50km)  (-50km, +50km)  (+0km, +50km)  (+50km, +50km)  (+100km, +50km)
	#(-100km, +0km)   (-50km, +0km)   (+0km, +0km)   (+50km, +0km)   (+100km, +0km)
        #(-100km, -50km)  (-50km, -50km)  (+0km, -50km)  (+50km, -50km)  (+100km, -50km)
	#(-100km, -100km) (-50km, -100km) (+0km, -100km) (+50km, -100km) (+100km, -100km)
	for q in rainStations:
		lat = q['station']['coord']['lat']
		lon = q['station']['coord']['lon']
                dif = 1/float(dimension/2) #determines the distance that should be incremented in a single loop. ex: .3 for 7x7
		for i in range(dimension):
			for n in range(dimension):
                                index = i*dimension + n
				x = lon - float(longitude) - n*dif + 1
				y = lat - float(latitude) + i*dif - 1
                                distance = math.sqrt(pow(x, 2) + pow(y, 2))
				if (distance < smallestDistances[index]):
					array[index] = q;
					smallestDistances[index] = distance

        #Outputs final results
	for i in range(pow(dimension, 2)):
	    if (toLog):
                log.write(str(shouldTurnOn(float(array[i]['last']['rain']['1h']))))
            print (str(shouldTurnOn(float(array[i]['last']['rain']['1h'])))),
	    if (i % dimension == dimension-1):
	        if (toLog):
                    log.write('\n')
		print
	print
	if (toLog):
		log.close()

        #waits 15 minutes
        time.sleep(900)
