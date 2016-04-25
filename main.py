import requests
import json
import time

#for debugging purposes
def printStuff(kek):
	for i in range(9):
		print kek[i]['station']['coord']['lat'],
		if (i % 3 == 2):
			print
	for i in range(9):
		print kek[i]['station']['coord']['lon'],
		if (i % 3 == 2):
			print
	print 'kek'
	return

url = 'http://api.openweathermap.org/data/2.5/station/find'
APIKey = ''
payload = {'lat': '40.42','lon': '-86.91', 'cnt': 9, 'APPID': APIKey}
stations = []
log = open('logs.txt' , 'a')
while (1):
	r = requests.get(url, params=payload)

	#add stations json data to an array if it doesn't have 9 already
	if (len(stations) < 9):
		for i in range(9):
			stations.append(r.json()[i])
	#else, replace first 9 with the new data
	else: 
		for i in range(9):
			stations[i] = r.json()[i]

	#printStuff(stations)

	#sort stations by longitute
	for i in range(8):
		for n in range(8):
			if (stations[n]['station']['coord']['lon'] < stations[n+1]['station']['coord']['lon']):
				temp = stations[n+1]
				stations[n+1] = stations[n]
				stations[n] = temp

	#printStuff(stations)

	#sort stations by latitude, but only 3 at a time, so as to not change which row they're in
	# 12 51 31 21 56 78 90 13 78 becomes
	# 51 31 12 78 56 21 90 78 13
	for i in range(3):
		for n in range(2):
			if (stations[i*3 + n]['station']['coord']['lat'] < stations[i*3 + n + 1]['station']['coord']['lat']):
				temp = stations[i*3 + n +1]
				stations[i*3 + n +1] = stations[i*3 + n]
				stations[i*3 + n] = temp

	#printStuff(stations)

	#flips [0] and [2] spots in a row
	# 51 31 12 78 56 21 90 78 13 becomes
	# 12 31 51 21 56 78 13 78 90
	# I'm aware that I should've just fixed the previous sort
	# But you do it. I was having problems. This just works
	for i in range(3):
		temp = stations[i*3]
		stations[i*3] = stations[i*3 + 2]
		stations[i*3 + 2] = temp

	#printStuff(stations)

	log.write(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) + "\n")
	for i in range(9):
		try: 
			print stations[i]['last']['clouds'][0]['condition'],;# "cloud",
			log.write("" + stations[i]['last']['clouds'][0]['condition']+ " ")
	    	except KeyError: pass
		try: 
			print stations[i]['last']['rain']['1h'],# "rain",
			log.write("" + str(stations[i]['last']['rain']['1h']) + " ")
	    	except KeyError: pass
	    	
	    	if (i % 3 == 2):
	    		log.write('\n')
	    		print
	time.sleep(900)
