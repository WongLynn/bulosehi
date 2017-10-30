from exchanges import Kraken,Bitstamp,Bitfinex
import numpy as np
import matplotlib.pyplot as plt
import time
import csv
import random
import operator

k = Kraken()
B = Bitstamp()
Bf = Bitfinex()

	
print '\nlogging data... '
print 'press ctrl + c to skip to analysing...'
try:
	while True:
		kp = k.getCurrentPrice('BTC','USD')
		Bp = B.getCurrentPrice('BTC','USD')
		Bfp = Bf.getCurrentPrice('BTC','USD')
		out = [time.time(),kp,Bp,Bfp]
		with open("ticker.csv", 'a') as fp:
			a = csv.writer(fp, delimiter=',')
			a.writerow(out)
		time.sleep(1) # reduce CPU usage, ticker rarely updates faster than 1s
except KeyboardInterrupt:
	pass
print 'analysing'

#read all data:
data=[]
with open("ticker.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for out in readCSV:
    	data.append(out)
if len(data) < 1000:
	print '\n too little data, need at least 1000 measurements'
	print 'exiting...'
	exit()
bitst = []
krak = []
bitfi = []
x = []
for row in data:
	krak.append(float(row[1]))
	bitst.append(float(row[2]))
	bitfi.append(float(row[3]))
	x.append(float(row[0]))

def get_local_extrema(x,data):
	m = [ [],[] ]
	delta = 100
	for i in range(delta,len(data)-delta):
		if data[i] == max(data[i-delta:i+delta]):
			m[0].append(x[i])
			m[1].append(data[i])
		if data[i] == min(data[i-delta:i+delta]):
			m[0].append(x[i])
			m[1].append(data[i])
	return m

area = 1000


mbifi = get_local_extrema(x[-area:],bitfi[-area:])
ybifi = [i for i in mbifi[1]]
plt.scatter(mbifi[0],ybifi,color='black')
mbits = get_local_extrema(x[-area:],bitst[-area:])
ybits = [i for i in mbits[1]]
plt.scatter(mbits[0],ybits,color='blue')


#plt.plot(x,krak,color='red',label='kraken')
#plt.plot(x,bitst,color='blue',label='bistampt')
#plt.plot(x,bitfi,color='black',label='bitfinex')


plt.legend()
plt.show()
	












