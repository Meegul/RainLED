import requests
import json
import math
import time
import sys

url = 'http://api.openweathermap.org/data/2.5/station/find'
APIKey = ''
latitude = ''
longitude = ''
payload = {'lat': latitude,'lon': longitude, 'cnt': 100, 'APPID': APIKey}

if (len(sys.argv) == 2 and sys.argv[1] == 'log'):
	toLog = 1
else: toLog = 0

while (1):
	if(toLog):
		log = open('logs.txt' , 'a')
		log.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) + "\n")
	print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
	r = requests.get(url, params=payload)

	counter = 0
	rainStations = []

	#finds stations with rain data
	for i in range(50):
		try:
			#print r.json()[i]['last']['rain']['1h'], counter
			x = r.json()[i]['last']['rain']['1h']
			#ensures no duplicates
			if not(r.json()[i] in rainStations):
				rainStations.append(r.json()[i])
				counter += 1
		except KeyError: pass

	#Array: 
	#0 1 2
	#3 4 5
	#6 7 8
	array = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
	smallestDistances = [100,100,100,100,100,100,100,100,100]

	#Chooses stations with distances closest to: 
	#(-100km, +100km) (+0km, +100km) (+100km, +100km)
	# (-100km, +0km)   (+0km, +0km)   (+100km, +0km)
	#(-100km, -100km) (+0km, -100km) (+100km, -100km)
	for q in rainStations:
		lat = q['station']['coord']['lat']
		lon = q['station']['coord']['lon']	
		for i in range(3):
			for n in range(3):
				index = i + n*3
				x = lon - float(longitude) - i*1 + 1
				y = lat - float(latitude) + n*1 - 1
				distance = math.sqrt(pow(x, 2) + pow(y, 2))
				if (distance < smallestDistances[index]):
					array[index] = q;
					smallestDistances[index] = distance

	#prints selected stations' locations
	#for i in array:
	#	lat = i['station']['coord']['lat']
	#	lon = i['station']['coord']['lon']
	#	print "(" + str(lon) + "," + str(lat) + ")"# "Distance:", distance

	for i in range(9):
		if (toLog):
			log.write(str(array[i]['last']['rain']['1h']))
		print array[i]['last']['rain']['1h'],
		if (i % 3 == 2):
			if (toLog):
				log.write('\n')
			print
	print
	if (toLog):
		log.close()
	time.sleep(900)


