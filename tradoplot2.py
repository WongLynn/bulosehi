print "importing..."
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import re
from itertools import combinations

def calculateSlope(x,y):
	slope = []
	for i in range(len(x)-1):
		if x[i+1]-x[i] == 0:
			slope.append(0)
			continue
		else:
			slope.append((y[i+1]-y[i])/(x[i+1]-x[i]))
	slope.append(0)
	return slope

def calculatePrecSlope(x,y):
	slope = []
	for i in range(len(x)-4):
		if x[i+2]-x[i+1] == 0:
			slope.append(0)
			continue
		else:
			slope.append((-y[i+3]+8*y[i+2]-8*y[i+1]+y[i])/(12*(x[i+2]-x[i+1])))
	slope.append(0)
	slope.append(0)
	slope.append(0)
	slope.append(0)
	return slope

def oppurtunity(fees,x,y,tRange):
	oppourtinity=[]
	maxSlope=0
	maxSlopeA=0
	maxSlopeB=0
	maxSlopeC=0
	isPrice=0
	inRow=0
	for i in range(len(x)-tRange):
		if x[i+tRange]-x[i] == 0:
			continue
		slope=(y[i+tRange]-y[i])/(x[i+tRange]-x[i])
		if slope>maxSlope:
			maxSlope=slope
			isPrice=y[i]
			row=i
		#if slope > y[i]*fees:
			#print y[i]*fees, y[i]
	#print maxSlope, isPrice, maxSlope/fees, row


def getDiff(x,y):
	return [x_i-y_i for x_i,y_i in zip(x,y)]

def getPrecSlope(x,y):
	return ((-y[3]+8*y[2]-8*y[1]+y[0])/(12*(x[2]-x[1])))

def getPrecDiff(x):
	if type(x) == 'collections.deque':
		x = [x.get() for _ in range(4)]
	return -x[3]+8*x[2]-8*x[1]+x[0]

def getNewDiff(marketQueues,queueLength=1000):
	data = combinations(marketQueues,2)
	totalDiff=[]
	for j in data:
		differences=[]
		for i in range(queueLength):
			differences.append(j[0][i]-j[1][i])
		totalDiff.append(differences)
	return totalDiff

def getMovingAverage(listPrice):
	nom = 0
	denom = 0
	for i in range(len(listPrice)):
		nom+=i*float(listPrice[i])
		denom+=i
	average = nom/denom
	return average


data=[]
with open("trado2.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for out in readCSV:
    	data.append(out)

bitfinexFees=0.001
bitfinex=[]
bitfinexTime=[]
bitfinexQueue=[]
bitstampFees=0.0025
bitstamp=[]
bitstampTime=[]
bitstampQueue=[]
krakenFees=0.0026
kraken=[]
krakenTime=[]
krakenQueue=[]

for i in data:
	if i[1] == "Kraken":
		kraken.append(float(i[2]))
		krakenTime.append(float(i[0]))
	elif i[1] == "Bitstamp":
		bitstamp.append(float(i[2]))
		bitstampTime.append(float(i[0]))
	else:
		bitfinex.append(float(i[2]))
		bitfinexTime.append(float(i[0]))

markets = [bitfinex,bitstamp,kraken]
time = [bitfinexTime,bitstampTime,krakenTime]
queues = [bitfinexQueue,bitstampQueue,krakenQueue]
diffs = [] #contains differences in the markets in the following order: finexstamp, finexkrak, stampkrak
movAvg = [[],[],[]]
diffLists = [[],[],[]]
diffsTime = []
position=0
for position in range(len(bitfinexTime)):
	for i in range(len(markets)):
		if len(queues[i]) < 1000:
			queues[i].append(markets[i][position])
			continue
		else:
			del queues[i][0]
			queues[i].append(markets[i][position-1])
	if not len(queues[0])<1000:
		diffs = getNewDiff(queues)
		movAvg[0].append(getMovingAverage(diffs[0]))
		movAvg[1].append(getMovingAverage(diffs[1]))
		movAvg[2].append(getMovingAverage(diffs[2]))
		diffLists[0].append(diffs[0][999])
		diffLists[1].append(diffs[1][999])
		diffLists[2].append(diffs[2][999])
	else:
		movAvg[0].append(0)
		movAvg[1].append(0)
		movAvg[2].append(0)
		diffLists[0].append(0)
		diffLists[1].append(0)
		diffLists[2].append(0)

print len(movAvg[0])
print len(bitfinex)

for i in range(15):
	tRange=i+1
	oppurtunity(bitfinexFees,bitfinexTime,bitfinex,tRange)
	oppurtunity(bitstampFees,bitstampTime,bitstamp,tRange)
	oppurtunity(krakenFees,krakenTime,kraken,tRange)

bitfinexSlope = calculateSlope(bitfinex,bitfinexTime)
bitstampSlope = calculateSlope(bitstamp,bitstampTime)
krakenSlope = calculateSlope(kraken,krakenTime)
bitfinexPrecSlope = calculatePrecSlope(bitfinex,bitfinexTime)
bitstampPrecSlope=calculatePrecSlope(bitstamp,bitstampTime)
krakenPrecSlope=calculatePrecSlope(kraken,krakenTime)

#finstampDiff = getDiff(bitfinex,bitstamp)
#finkrakDiff = getDiff(bitfinex,kraken)
#stampkrakDiff = getDiff(bitstamp,kraken)

finstampDiff = diffLists[0]
finkrakDiff = diffLists[1]
stampkrakDiff = diffLists[2]

finstampMovAvg = movAvg[0]
finkrakMovAvg = movAvg[1]
stampkrakMovAvg = movAvg[2]

fig = plt.figure()
ax01 = fig.add_subplot(311)
ax02 = fig.add_subplot(312)
ax03 = fig.add_subplot(313)

ax01.plot(bitfinexTime,finstampMovAvg,label='$FinStamp')
ax01.plot(krakenTime,finkrakMovAvg,label='$FinKrak')
print len(bitstampTime), len(stampkrakMovAvg)
ax01.plot(bitstampTime,stampkrakMovAvg[:-1],label='$StampKrak')
#ax02.plot(krakenTime,krakenPrecSlope,label='Kraken')
#ax02.plot(bitstampTime,bitstampPrecSlope,label='Bitstamp')
#ax02.plot(bitfinexTime,bitfinexPrecSlope,label='Bitfinex')
print len(bitfinexTime), len(finstampDiff)
ax02.plot(bitfinexTime,finstampDiff,label='finstamp')
ax02.plot(krakenTime,finkrakDiff,label='finkrak')
print len(bitstampTime),len(stampkrakDiff)
ax02.plot(bitstampTime,stampkrakDiff[:-1],label='stampkrak')
ax03.plot(krakenTime,kraken,label='Kraken')
ax03.plot(bitstampTime,bitstamp,label='Bitstamp')
ax03.plot(bitfinexTime,bitfinex,label='Bitfinex')


#ax01.xlabel("Unix Time")
#ax01.ylabel("$/BTC")
ax01.legend()
ax02.legend()
ax03.legend()
fig.show()
plt.savefig('slopeplot.png')


