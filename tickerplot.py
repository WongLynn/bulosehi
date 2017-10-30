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
		if data[i] == max(data[i-delta:i+delta])  and data[i] not in m[1]:
			m[0].append(x[i])
			m[1].append(data[i])
		if data[i] == min(data[i-delta:i+delta]) and data[i] not in m[1]:
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
print 'max-minbifi',max(ybifi)-min(ybifi)
print 'max-minbits',max(ybits)-min(ybits)
xbifi = mbifi[0]
xbits = mbits[0]

def norm(a,b):
	return np.sqrt(float(a)**2+float(b)**2)

def slope(a,b):
	return b/float(a)


def find_match(xbifi,ybifi,xbits,ybits):
	poss=[[],[]]
	for i in range(1,len(xbifi)):
		print 'searching'
		if ybifi[i-1]!=ybifi[i]:
			pair = [[xbifi[i-1],xbifi[i]],[ybifi[i-1],ybifi[i]]]
			pair_norm = norm(pair[0][0]-pair[0][1],pair[1][0]-pair[1][1])
			pair_slope = slope(pair[0][0]-pair[0][1],pair[1][0]-pair[1][1])
			for j in range(1,len(xbits)):
				if ybits[j-1]!=ybits[j]:
					pair2=[[xbits[j-1],xbits[j]],[ybits[j-1],ybits[j]]]
					pair2_norm = norm(pair2[0][0]-pair2[0][1],pair2[1][0]-pair2[1][1])
					pair2_slope = slope(pair2[0][0]-pair2[0][1],pair2[1][0]-pair2[1][1])
					print pair_norm,pair2_norm,'__',pair_slope,pair2_slope
					if pair_slope < 0 and pair2_slope <0:
						slope_condition = bool(pair_slope > pair2_slope*1.5 and pair_slope < pair2_slope*0.5)
					else:
						slope_condition = bool(pair_slope < pair2_slope*1.5 and pair_slope > pair2_slope*0.5)
					if pair_norm < pair2_norm*1.5 and pair_norm>pair2_norm*0.5 and slope_condition:
						print 'found match'
						if i in poss[0] or j in poss[1]:
							pass
						else:
							poss[0].append(i)
							poss[1].append(j)
						break
	return poss
poss = find_match(xbifi,ybifi,xbits,ybits)
print 'done'
print poss
sum = 0
for i,j in zip(poss[0],poss[1]):
	plt.plot([xbifi[i-1],xbifi[i]],[ybifi[i-1],ybifi[i]],color='red')
	plt.plot([xbits[j-1],xbits[j]],[ybits[j-1],ybits[j]],color='red')
	print 'difference',xbifi[i]-xbits[j]
	print 'difference',xbifi[i-1]-xbits[j-1]
	sum += xbifi[i]-xbits[j]#+xbifi[i-1]-xbits[j-1]
print 'difference', sum/float(len(poss[0]))
sum = sum/float(len(poss[0]))
#plt.plot(x,krak,color='red',label='kraken')
adjx = [ i + sum for i in x]
plt.plot(x[-area:-100],bitst[-area:-100],color='blue',label='bistampt')
#plt.plot(adjx[-area:-100],bitst[-area:-100],color='red',label='bistampt')
plt.plot(x[-area:-100],bitfi[-area:-100],color='black',label='bitfinex')


plt.legend()
plt.show()
	












