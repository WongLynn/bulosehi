import hmac
import hashlib
import time
import websocket
import json
import csv
import ssl
from exchanges import Kraken,Bitstamp,Bitfinex,Poloniex,Bittrex


kraken = Kraken()
bitstamp = Bitstamp()
bitfinex = Bitfinex()
poloniex = Poloniex()
bittrex = Bittrex()

class BitfinexWS:

	ssl_defaults = ssl.get_default_verify_paths()
	sslopt_ca_certs = {'ca_certs': ssl_defaults.cafile}

	def begin(self):
		'''
			returns wallet in the form of:
			[
				['coin', amount],
				...
			]
		'''
		file = open('key.txt','r')
		data = file.readlines()
		API_KEY = data[0].replace('\n','')
		API_SECRET = data[1].replace('\n','')
		file.close()
		ws = websocket.create_connection("wss://api.bitfinex.com/ws/2",sslopt=self.sslopt_ca_certs)
		nonce = int(time.time() * 1000000)
		auth_payload = 'AUTH{}'.format(nonce)
		signature = hmac.new(
		  API_SECRET.encode(),
		  msg = auth_payload.encode(),
		  digestmod = hashlib.sha384
		).hexdigest()

		print(ws.recv())
		auth = {
		  'apiKey': API_KEY,
		  'event': 'auth',
		  'authPayload': auth_payload,
		  'authNonce': nonce,
		  'authSig': signature
		}
		ws.send(json.dumps(auth))
		ws.recv()
		while True:
			ans = json.loads(ws.recv())
			if str(ans[1]) == 'ws':
				break
		ans = ans[2]
		wallet = [ [str(w[1]),w[2]] for w in ans]
		return ws,wallet


	def get_price(self,pair):
		'''
			returns in the form of:
			[BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW]
		'''
		ws = websocket.create_connection("wss://api.bitfinex.com/ws/2",sslopt=self.sslopt_ca_certs)
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

	def get_wallet(ws,self):
		return



	def new_order(self,ws,amount='None',pair='None'):
		payload = [
			  0,
			  "on",None,
				{
				"type": "EXCHANGE MARKET",
				"symbol": pair,
				"amount": amount,
				"hidden": 0
				}
			]
		print 'waiting for heartbeat\n'
		while True:
			ans = json.loads(ws.recv())
			if str(ans[1]) == 'ats':
				break
			if str(ans[1]) == 'hb':
				break
		print 'received heartbeat \n'
		print 'sending order:'
		print payload
		ws.send(json.dumps(payload))
		print 'response:'
		print(ws.recv())


#ws,wallet = begin()
tradoInst = BitfinexWS()
ts,price = tradoInst.get_price(bitfinex.getTradedPair("XRP","BTC"))
#print(bitstamp.getTicker("XRP","BTC"))
#print(bitstamp.getCurrentPrice("XRP","BTC"))
#new_order(ws,'1000','tXRPBTC')
print ''
print price
while True:
	ans = json.loads(ts.recv())
	if str(ans[1]) == 'hb':
		print 'nothing new on the ticker'
	else:
		print ans
		out = ['XRP',time.ctime(),float(ans[1][0]),float(ans[1][1]),float(ans[1][2]),float(ans[1][3]),float(ans[1][4]),float(ans[1][5]),float(ans[1][6]),float(ans[1][6]),float(ans[1][8]),float(ans[1][9])]
		print out
		with open("trado.csv", 'a') as fp:
			a = csv.writer(fp, delimiter=',')
			a.writerow(out)

#ws.close()
ts.close()
