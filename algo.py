import csv
import numpy as np
import matplotlib.pyplot as plt
import time
import websocket
import json



live = False

'''
this code will first run through all the data in sampledata.csv, 
if live == False, then it will plot the analyzed results and terminate, 
if live == True it will not plot anything but switch to live ticker mode and
append all new fetched data to the sampledata.csv
'''

ws = websocket.WebSocket()

def get_price(pair):
	'''
		returns in the form of:
		[BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW]
	'''
	ws = websocket.create_connection("wss://api.bitfinex.com/ws/2")
	ws.recv()
	request = {
		'event' : 'subscribe',
		'channel' : 'ticker',
		'symbol' : pair
		}
	ws.send(json.dumps(request))
	ID = json.loads(ws.recv())['chanId']
	while True:
		ans = json.loads(ws.recv())
		if len(ans[1]):
			return ws,ans[1]
		if str(ans[1]) == 'hb':
			return ws,'no info received...'
def maketrade(w,a,c):
	global tradecounter
	print ''
	print "making trade #{}".format(tradecounter)
	tradecounter += 1
	w[1][1] = w[1][1] - a
	w[0][1] = w[0][1] + a/c - 0.75 #0.75 XRP transaction fee
	print 'sending {} BTC as {} XRP'.format(a,a/c-0.75)
	return w
	
def makebacktrade(w,a,c):
	print "making a backtrade"
	w[1][1] = w[1][1] + (a-0.75)*c #0.75 XRP transaction fee
	w[0][1] = w[0][1] - a
	print 'receiving {} XRP as {} BTC'.format(a,(a-0.75)*c)
	return w
	
def algo(p):
	global ysell
	global ybuy
	global threshhold
	ysell.append(p[2])
	ybuy.append(p[4])
	if len(ysell)> 150: #leave a buffer at the first entries
		''' check if the price has fallen and is climbing now'''
		c1 = bool(float(ybuy[-3])>float(ybuy[-2])) 
		#c1: if the price has been falling
		c2 = bool(float(ybuy[-1])>float(ybuy[-2]))
		#c2: if the price is now climbing again
		c3 = bool(float(ybuy[-100])>1.005*float(ybuy[-3]))
		#c3: if the price has fallen for the last 100 entries by 0.5 percent	
		condition = bool( c1  and c2 and c3 )
		if condition and threshhold==0:
			'''threshhold must be =0 otherwise a trade is already ongoing
			and we do not want to invest more in a falling price'''
			threshhold = float(p[4])*(1.005)
			'''ca 1.5 XRP transaction fee per trade,
			thus we set the threshhold at 0.5 percent, for our 0.02BTC
			investement in this example'''
			return 1
		if float(p[2])>=threshhold and threshhold != 0:
			''' if the threshhold is reached, we sell'''
			threshhold =0
			return -1
		else:
			'''do nothing'''
			return 0
		
	else:
		''' do nothing'''
		return 0


tradecounter = 0
threshhold = 0
ysell = []
ybuy = []
data=[]
buys = []
sells = []
threshholds = []

''' set wallet'''
wallet = [ ['XRP', 0], ['BTC', 2] ]
walletbegin = [ ['XRP', 0], ['BTC', 2] ]



print "sample data__"
with open("sampledata.csv") as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for out in readCSV:
		data.append(out)
''' using the sample data file '''
i=0
for currentprice in data:
	''' feeding sample data one by one to the algo function, as the live ticker would do'''
	res = algo(currentprice)
	if res == 1:
		'''buy with 0.02 BTC (BTC->XRP)'''
		amount = 0.02
		buys.append(i)
		''' save the buy in the buys list to visualize it later'''
		wallet = maketrade(wallet,amount,float(currentprice[4]))
	elif res ==-1:
		''' sell whole (previously bought) wallet content (XRP->BTC)'''
		amount = wallet[0][1]
		sells.append(i)
		''' save the sell in the sells list to visualize it later'''
		wallet = makebacktrade(wallet,amount,float(currentprice[2]))
	elif res ==0:
		''' do nothing'''
		pass
	i+=1
	if threshhold == 0:
		''' for visualizing purposes'''
		threshholds.append(np.nan)
	else:
		threshholds.append(threshhold)
if not live:
	print "\nbegin wallet:"
	print walletbegin
	print " current wallet:"
	''' final back trade to put all in the XRP wallet'''
	#wallet = makebacktrade(wallet,wallet[0][1],float(currentprice[2]))
	print wallet
	print "netto: "
	print wallet[1][1]-walletbegin[1][1], 'BTC'
	print (wallet[1][1]-walletbegin[1][1])/float(currentprice[2]), 'XRP'
	print "I made {} trades".format(tradecounter)	
	''' now plot everything to see when the bot made the trades
	only for debugging useful, thus only in not-live clause'''
	plt.plot(np.arange(len(ybuy)),ybuy,color='red',label='buy')
	plt.plot(np.arange(len(ybuy)),ysell,color='blue',label='sell')
	plt.plot(np.arange(len(ybuy)),threshholds,color='orange',ls='--',label='threshhold')
	plt.ylabel('BTC')
	plt.xlabel('measurement')
	minimum = min(min(ybuy),min(ysell))
	maximum = max(max(ybuy),max(ysell))
	print minimum,maximum
	ybuys = [float(minimum)*0.995 for i in buys]
	ysells = [float(minimum)*0.995 for i in sells]
	if buys:
		plt.bar(buys,ybuys,50,color='black',label='buy order')
	if sells:
		plt.bar(sells,ysells,50,color='orange',label='sell order')
	plt.ylim(float(minimum)*0.99,float(maximum)*1.01)
	plt.legend()
	plt.show()
	exit()
''' switching to live ticker '''
print "live data__"
try:
	i=0
	''' initialize live ticker'''
	ts,price = get_price('tXRPBTC')
	out = price
	while True:
		''' get live data:'''
		ans = json.loads(ts.recv())
		if str(ans[1]) == 'hb':
			pass
		else:
			'''append new tickerdata to csv'''
			out = ['XRP',time.ctime(),float(ans[1][0]),float(ans[1][1]),float(ans[1][2]),float(ans[1][3]),float(ans[1][4]),float(ans[1][5]),float(ans[1][6]),float(ans[1][6]),float(ans[1][8]),float(ans[1][9])]
			with open("sampledata.csv", 'a') as fp:
				a = csv.writer(fp, delimiter=',')
				a.writerow(out)
		currentprice = out
		res = algo(currentprice)
		if res == 1:
			amount = 100
			buys.append(i)
			wallet = maketrade(wallet,amount,float(currentprice[4]))
		elif res ==-1:
			amount = 100
			sells.append(i)
			wallet = makebacktrade(wallet,amount,float(currentprice[2]))
		elif res ==0:
			pass
		i+=1
		if threshhold == 0:
			threshholds.append(np.nan)
		else:
			threshholds.append(threshhold)
except Exception as e:
	print "ERROR: ",e
	print "\nbegin wallet:"
	print walletbegin
	print " current wallet:"
	''' final back trade to put all in the XRP wallet'''
	wallet = makebacktrade(wallet,wallet[1][1]/float(currentprice[2]),float(currentprice[2]))
	print wallet
	print "netto: "
	print wallet[0][1]-walletbegin[0][1]
	print "I made {} trades".format(tradecounter)
