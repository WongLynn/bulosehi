from exchanges import Kraken,Bitstamp,Bitfinex
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

k = Kraken()
B = Bitstamp()
Bf = Bitfinex()


#read all data:
data=[]
with open("ticker.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for out in readCSV:
    	data.append(out)

data = data[-250:-1]
bitst = []
krak = []
bitfi = []
x = []
for row in data:
	krak.append(float(row[1]))
	bitst.append(float(row[2]))
	bitfi.append(float(row[3]))
	x.append(float(row[0]))

if len(data) <10:
	print 'too little data, need at least 100 entries... exiting...'
	#exit()


def get_local_extrema(x,data):
	m = [ [],[] ]
	delta = 50
	for i in range(delta,len(data)-delta):
		if data[i] == max(data[i-delta:i+delta])  and data[i] not in m[1]:
			m[0].append(x[i])
			m[1].append(data[i])
		if data[i] == min(data[i-delta:i+delta]) and data[i] not in m[1]:
			m[0].append(x[i])
			m[1].append(data[i])
	return m

def norm(a,b):
	return np.sqrt(float(a)**2+float(b)**2)

def slope(a,b):
	return b/float(a)

def SLOPEcon(pair_slope,pair2_slope):
	if pair_slope < 0 and pair2_slope <0:
		slope_condition = bool(pair_slope > pair2_slope*1.4 and pair_slope < pair2_slope*0.6)
	elif pair_slope >= 0 and pair2_slope >=0:
		slope_condition = bool(pair_slope < pair2_slope*1.4 and pair_slope > pair2_slope*0.6)
	else:
		return False
	return slope_condition

def NORMcon(pair_norm,pair2_norm):
	return bool(pair_norm < pair2_norm*1.2 and pair_norm>pair2_norm*0.8)

def find_match2(xbifi,ybifi,xbits,ybits):
	poss=[[],[]]
	for i in range(len(xbifi)):
		for j in range(i,len(xbifi)):
			for k in range(j,len(xbifi)):
				if i!=j and i!=k and k!=j:
					tripplet = [[xbifi[i],xbifi[j],xbifi[k]],[ybifi[i],ybifi[j],ybifi[k]]]
					tr_norm1 = norm(tripplet[0][0]-tripplet[0][1],tripplet[1][0]-tripplet[1][1])
					tr_norm2 = norm(tripplet[0][1]-tripplet[0][2],tripplet[1][1]-tripplet[1][2])
					tr_norm3 = norm(tripplet[0][2]-tripplet[0][0],tripplet[1][2]-tripplet[1][0])
					tr_slope1 = slope(tripplet[0][0]-tripplet[0][1],tripplet[1][0]-tripplet[1][1])
					tr_slope2 = slope(tripplet[0][1]-tripplet[0][2],tripplet[1][1]-tripplet[1][2])
					tr_slope3 = slope(tripplet[0][2]-tripplet[0][0],tripplet[1][2]-tripplet[1][0])
					for l in range(len(xbits)):
						for m in range(l,len(xbits)):
							for n in range(m,len(xbits)):
								if m!=n and n!=l and m!=l:
									tripplet2 = [[xbits[l],xbits[m],xbits[n]],[ybits[l],ybits[m],ybits[n]]]
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
									p1 = [i,j,k]
									p2 = [l,m,n]
									if not ((tripplet[0][0]<= tripplet[0][1] and  tripplet2[0][0]<= tripplet2[0][1]) or (tripplet[0][0]>= tripplet[0][1] and  tripplet2[0][0]>= tripplet2[0][1])):
										break
									if not ((tripplet[0][1]<= tripplet[0][2] and  tripplet2[0][1]<= tripplet2[0][2]) or (tripplet[0][1]>= tripplet[0][2] and  tripplet2[0][1]>= tripplet2[0][2])):
										break
									if not ((tripplet[0][2]<= tripplet[0][0] and  tripplet2[0][2]<= tripplet2[0][0]) or (tripplet[0][2]>= tripplet[0][0] and  tripplet2[0][2]>= tripplet2[0][0])):
										break
									if c1 and c2 and c3 and c4 and c5 and c6:
										
										if p1 in poss[0] or p2 in poss[1]:
											pass
										else:
											poss[0].append(p1)
											poss[1].append(p2)
	return poss




EXCHANGES = [bitst,bitfi]



ybifi = []
xbifi = []
ybits = []
xbits = []
for i in range(len(bitst)):
	if not i % 30:
		ybifi.append(bitfi[i])
		xbifi.append(x[i])
		ybits.append(bitst[i])
		xbits.append(x[i])

sum = 0

poss = find_match2(xbifi,ybifi,xbits,ybits)	
print poss
for i,j in zip(poss[0],poss[1]):
	plt.plot([xbifi[i[0]],xbifi[i[1]],xbifi[i[2]],xbifi[i[0]]],[ybifi[i[0]],ybifi[i[1]],ybifi[i[2]],ybifi[i[0]]],color='red')
	plt.plot([xbits[j[0]],xbits[j[1]],xbits[j[2]],xbits[j[0]]],[ybits[j[0]],ybits[j[1]],ybits[j[2]],ybits[j[0]]],color='green')
	print 'difference',xbifi[i[0]]-xbits[j[0]]+xbifi[i[1]]-xbits[j[1]]+xbifi[i[2]]-xbits[j[2]]
	sum += xbifi[i[0]]-xbits[j[0]]+xbifi[i[1]]-xbits[j[1]]+xbifi[i[2]]-xbits[j[2]]
	print sum
if poss != [[],[],]:
	print len(poss[0])
	sum = sum/float(len(poss[0])*3)
else:
	print 'no pattern found'
	sum = 0
index = None
for i in range(len(x)):
	if int(x[i])==int(x[-1]-sum):
		index=i
		break
if sum < 0:
	print 'bitfinex is leading by {:.2f} seconds'.format(sum)
	if index!= None:
		for i in range(index-10,index+10):
			if int(bitst[i])<=int(bitfi[-1]) +10 and int(bitst[i])>=int(bitfi[-1])-10:
				print 'confirmed'
				break
	else:
		print 'no index found'
elif sum >0:
	print 'bitstamp is leading by {:.2f} seconds'.format(sum)
	if index:
		for i in range(index-10,index+10):
			if int(bitst[i])<=int(bitfi[-1]) +10 and int(bitst[i])>=int(bitfi[-1])-10:
				print 'confirmed'
				break
	else:
		print 'no index found'
else:
	print 'inconclusive'

#x = [i  for i in range(len(bitst))]
plt.plot(x,bitst,color='blue',label='bistampt')
#plt.plot(x,krak,color='red',label='kraken')
plt.plot(x,bitfi,color='black',label='bitfinex')


plt.legend()
plt.show()