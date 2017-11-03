from exchanges import Kraken,Bitstamp,Bitfinex
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

start_time = time.time()



def norm(a,b):
	return np.sqrt(float(a)**2+float(b)**2)

def slope(a,b):
	return b/float(a)

def SLOPEcon(pair_slope,pair2_slope):
	''' returns True/False for slope condition '''
	if pair_slope < 0 and pair2_slope <0:
		slope_condition = bool(pair_slope > pair2_slope*1.3 and pair_slope < pair2_slope*0.7)
	elif pair_slope >= 0 and pair2_slope >=0:
		slope_condition = bool(pair_slope < pair2_slope*1.3 and pair_slope > pair2_slope*0.7)
	else:
		return False
	return slope_condition

def NORMcon(pair_norm,pair2_norm):
	''' returns True/False for norm condition'''
	return bool(pair_norm < pair2_norm*1.1 and pair_norm>pair2_norm*0.9)

def find_match2(xbifi,ybifi,xbits,ybits):
	poss=[[],[]]
	for i in range(len(xbifi)):
		for j in range(i,len(xbifi)):
			for k in range(j,len(xbifi)):
				if i!=j and i!=k and k!=j:
					''' create first triangle'''
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
									'''create 2nd triangle'''
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
									''' check that we don't confuse mirrored triangle pattern, e.g. check that order of x coordinates is the same'''
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
	sum = 0
	for i,j in zip(poss[0],poss[1]):
		''' take the average of all x-axis-differences of all patterns'''
		''' optionally plot each triangle and print each x-axis difference for debugging purposes'''
		plt.plot([xbifi[i[0]],xbifi[i[1]],xbifi[i[2]],xbifi[i[0]]],[ybifi[i[0]],ybifi[i[1]],ybifi[i[2]],ybifi[i[0]]],color='red')
		plt.plot([xbits[j[0]],xbits[j[1]],xbits[j[2]],xbits[j[0]]],[ybits[j[0]],ybits[j[1]],ybits[j[2]],ybits[j[0]]],color='green')
		print 'difference',xbifi[i[0]]-xbits[j[0]]+xbifi[i[1]]-xbits[j[1]]+xbifi[i[2]]-xbits[j[2]]
		sum += xbifi[i[0]]-xbits[j[0]]+xbifi[i[1]]-xbits[j[1]]+xbifi[i[2]]-xbits[j[2]]
	if poss != [[],[]]:
		sum = sum/float(len(poss[0])*3)
	else:
		print 'no pattern found'
		sum = 0
	''' returns difference in seconds, positive if xbits is leading,negative if xbifi is leading'''
	return sum


#read all data:
data=[]
with open("ticker.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for out in readCSV:
    	data.append(out)

data = data[-300:-1]
#300 entries are approx 15 min of data
bitst = []
krak = []
bitfi = []
x = []
for row in data:
	krak.append(float(row[1]))
	bitst.append(float(row[2]))
	bitfi.append(float(row[3]))
	x.append(float(row[0]))

if len(data) <100:
	print 'too little data, need at least 100 entries... exiting...'
	exit()
	

ybifi = []
xbifi = []
ybits = []
xbits = []
for i in range(len(bitst)):
	'''only use every 20th measurement to save time, would take decades otherwise..'''
	if not i % 20:
		ybifi.append(bitfi[i])
		xbifi.append(x[i])
		ybits.append(bitst[i])
		xbits.append(x[i])


'''compare the two graphs'''
sum = find_match2(xbifi,ybifi,xbits,ybits)	

if sum < 0:
	print 'bitfinex is leading by {:.2f} seconds'.format(sum)
elif sum >0:
	print 'bitstamp is leading by {:.2f} seconds'.format(sum)
else:
	print 'inconclusive'
print 'that took {:.1f} seconds to calculate.'.format(time.time()-start_time)

plt.plot(x,bitst,color='blue',label='bistampt')
plt.plot(x,bitfi,color='black',label='bitfinex')


plt.legend()
plt.show()