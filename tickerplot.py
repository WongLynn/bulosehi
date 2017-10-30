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

area = 5000 #how much recorded data we want to analyse (more than 2000 recommended)


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

def SLOPEcon(pair_slope,pair2_slope):
	if pair_slope < 0 and pair2_slope <0:
		slope_condition = bool(pair_slope > pair2_slope*1.7 and pair_slope < pair2_slope*0.3)
	else:
		slope_condition = bool(pair_slope < pair2_slope*1.7 and pair_slope > pair2_slope*0.3)
	return slope_condition

def NORMcon(pair_norm,pair2_norm):
	return bool(pair_norm < pair2_norm*1.7 and pair_norm>pair2_norm*0.3)


def find_match(xbifi,ybifi,xbits,ybits):
	poss=[[],[]]
	for i in range(2,len(xbifi)):
		print 'searching'
		if ybifi[i-1]!=ybifi[i]:
			''' here we are spawning the first tripplet, 
			we connect all three dots'''
			tripplet = [[xbifi[i-2],xbifi[i-1],xbifi[i]],[ybifi[i-2],ybifi[i-1],ybifi[i]]]
			tr_norm1 = norm(tripplet[0][0]-tripplet[0][1],tripplet[1][0]-tripplet[1][1])
			tr_norm2 = norm(tripplet[0][1]-tripplet[0][2],tripplet[1][1]-tripplet[1][2])
			tr_norm3 = norm(tripplet[0][2]-tripplet[0][0],tripplet[1][2]-tripplet[1][0])
			tr_slope1 = slope(tripplet[0][0]-tripplet[0][1],tripplet[1][0]-tripplet[1][1])
			tr_slope2 = slope(tripplet[0][1]-tripplet[0][2],tripplet[1][1]-tripplet[1][2])
			tr_slope3 = slope(tripplet[0][2]-tripplet[0][0],tripplet[1][2]-tripplet[1][0])
			for j in range(2,len(xbits)):
				if ybits[j-1]!=ybits[j]:
					''' other tripplet'''
					tripplet2=[[xbits[j-2],xbits[j-1],xbits[j]],[ybits[j-2],ybits[j-1],ybits[j]]]
					tr2_norm1 = norm(tripplet2[0][0]-tripplet2[0][1],tripplet2[1][0]-tripplet2[1][1])
					tr2_norm2 = norm(tripplet2[0][1]-tripplet2[0][2],tripplet2[1][1]-tripplet2[1][2])
					tr2_norm3 = norm(tripplet2[0][2]-tripplet2[0][0],tripplet2[1][2]-tripplet2[1][0])
					tr2_slope1 = slope(tripplet2[0][0]-tripplet2[0][1],tripplet2[1][0]-tripplet2[1][1])
					tr2_slope2 = slope(tripplet2[0][1]-tripplet2[0][2],tripplet2[1][1]-tripplet2[1][2])
					tr2_slope3 = slope(tripplet2[0][2]-tripplet2[0][0],tripplet2[1][2]-tripplet2[1][0])
					''' compare their slope and length'''
					c1 = SLOPEcon(tr2_slope1,tr_slope1)
					c2 = SLOPEcon(tr2_slope2,tr_slope2)
					c3 = SLOPEcon(tr2_slope3,tr_slope3)
					c4 = NORMcon(tr2_norm1,tr_norm1)
					c5 = NORMcon(tr2_norm2,tr_norm2)
					c6 = NORMcon(tr2_norm3,tr_norm3)
					if c1 and c2 and c3 and c4 and c5 and c6:
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
	sum += xbifi[i-1]-xbits[j-1]
if poss != [[],[],]:
	print len(poss[0])
	sum = sum/float(len(poss[0]))
else:
	print 'no pattern found'
	sum = 0
if sum < 0:
	print 'bitfinex is leading by {:.2f} seconds'.format(sum)
elif sum >0:
	print 'bitstamp is leading by {:.2f} seconds'.format(sum)
adjx = [ i + sum for i in x]
plt.plot(x[-area:-100],bitst[-area:-100],color='blue',label='bistampt')
plt.plot(adjx[-area:-100],bitst[-area:-100],color='red',label='bistampt adjusted')
plt.plot(x[-area:-100],bitfi[-area:-100],color='black',label='bitfinex')


plt.legend()
plt.show()
	












