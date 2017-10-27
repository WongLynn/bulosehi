print "importing..."
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import re

data=[]
with open("sampledata.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for out in readCSV:
    	data.append(out)

x = []
ysell = []
ybuy = []
ylast = []
timelist = []
for i in data:
	timelist.append( re.search('[0-9]{2}[:]{1}[0-9]{2}[:]{1}[0-9]{2}' ,i[1] ).group(0) )
	ysell.append(i[2])
	ybuy.append(i[4])
	ylast.append(i[8])
for timestamp in timelist:
	x.append( int(timestamp[0:2])+float(int(timestamp[3:5])/60.)+ float(int(timestamp[6:8])/3600.))
ticks= [0]
print timelist[0]
print timelist[0][0:2]
print timelist[0][3:5]
print timelist[0][6:8]
labels1 =   [
			'0:00','1:00','2:00','3:00','4:00','5:00',
			'6:00','7:00','8:00','9:00','10:00','11:00',
			'12:00','13:00','14:00','15:00','16:00','17:00',
			'18:00','19:00','20:00','21:00','22:00','23:00'
			]
labels = []
for i in range(len(x)):
	if ticks[-1]!= int(x[i]):
		ticks.append( int(x[i]) )
if ticks[-1]!=23:
	ticks.append( ticks[-1]+1 )
if len(ticks)>1:
	if ticks[1]!=1:
		ticks=ticks[1:]
for i in range(len(labels1)):
	for item in ticks:
		if int(item) == i:
			labels.append( labels1[i] )
plt.xticks(ticks,labels)
if ticks[-1]==23 and x[-1]>ticks[-1]:
	plt.xlim(ticks[0],x[-1])
else:
	plt.xlim(ticks[0],ticks[-1])
print ticks
print labels
plt.plot(x,ybuy,color="r",label='buy')
plt.plot(x,ysell,color="b",label='sell')
plt.plot(x,ylast,color="y",ls='--',label='last')
plt.legend()
plt.show()


