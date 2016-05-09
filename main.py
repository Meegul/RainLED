import requests
import json
import math
import time
import sys

url = 'http://api.openweathermap.org/data/2.5/station/find'
APIKey = ''
latitude = ''
longitude = ''
payload = {'lat': latitude,'lon': longitude, 'cnt': 50, 'APPID': APIKey}

def shouldTurnOn(rain):
    return 1 if rain != 0 else 0

if (len(sys.argv) == 2 and sys.argv[1] == 'log'):
	toLog = 1
else: toLog = 0

while (1):
	if(toLog):
		log = open('logs.txt' , 'a')
		log.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) + "\n")
	print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

        r = []
	temp = requests.get(url, params=payload)

        #requests data from spots:
        #(0, 2, 4, 10, 12, 14, 02, 22, 24)
        for y in range(3):
            for x in range(3):
                payload = {'lat': str(float(latitude) + x - 1),'lon': str(float(longitude) - y + 1), 'cnt': 50, 'APPID': APIKey}
                temp = requests.get(url, params=payload)
                for n in temp.json():
                    if (n not in r):
                        r.append(n)
        counter = 0
	rainStations = []

        #finds stations with rain data
	for i in range(len(r)):
            try:
		x = r[i]['last']['rain']['1h']
		#ensures no duplicates
		if not(r[i] in rainStations):
		    rainStations.append(r[i])
		    counter += 1
	    except KeyError: pass

        #Array:
	#0  1  2  3  4
	#5  6  7  8  9
        #10 11 12 13 14
	#15 16 17 18 19
        #20 21 22 23 24
	array = []
        smallestDistances = []
        for i in range(25):
            array.append(-1)
            smallestDistances.append(100)

	#Chooses stations with distances closest to:
	#(-100km, +100km) (-50km, +100km) (+0km, +100km) (+50km, +100km) (+100km, +100km)
        #(-100km, +50km)  (-50km, +50km)  (+0km, +50km)  (+50km, +50km)  (+100km, +50km)
	#(-100km, +0km)   (-50km, +0km)   (+0km, +0km)   (+50km, +0km)   (+100km, +0km)
        #(-100km, -50km)  (-50km, -50km)  (+0km, -50km)  (+50km, -50km)  (+100km, -50km)
	#(-100km, -100km) (-50km, -100km) (+0km, -100km) (+50km, -100km) (+100km, -100km)
	for q in rainStations:
		lat = q['station']['coord']['lat']
		lon = q['station']['coord']['lon']
		for i in range(5):
			for n in range(5):
                                index = n + i*5
				x = lon - float(longitude) - n*.5 + 1
				y = lat - float(latitude) + i*.5 - 1
                                distance = math.sqrt(pow(x, 2) + pow(y, 2))
                                #print "Index: " + str(index),
                                #print "x: " + str(x),
                                #print "y: " + str(y),
                                #print "distance: " + str(distance)
				if (distance < smallestDistances[index]):
					array[index] = q;
					smallestDistances[index] = distance

        #prints selected stations' locations
        #for i in array:
        #       lat = i['station']['coord']['lat']
	#	lon = i['station']['coord']['lon']
	#	print "(" + str(lat) + "," + str(lon) + ")"


        #outputs final results
	for i in range(25):
	    if (toLog):
                log.write(str(shouldTurnOn(float(array[i]['last']['rain']['1h']))))
            print (str(shouldTurnOn(float(array[i]['last']['rain']['1h'])))),
	    if (i % 5 == 4):
	        if (toLog):
                    log.write('\n')
		print
	print
	if (toLog):
		log.close()
	#waits 15 minutes
        time.sleep(900)
