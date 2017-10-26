from exchanges import Kraken,Bitstamp,Bitfinex,Poloniex,Bittrex
import requests as req
import json as json

kraken = Kraken()
bitstamp = Bitstamp()
bitfinex = Bitfinex()
poloniex = Poloniex()
bittrex = Bittrex()
#print(kraken.pairsByTicker)
#print(bitstamp.pairsByTicker)
#print(poloniex.pairsByTicker)
#print (kraken.getCurrentPrice("BTC","USD"))
#print(kraken.getCurrentPrice("USD","LTC"))
#print(kraken.getCurrentPrice("ETH","USD"))
#print(bitstamp.getCurrentPrice("BTC","USD"))
#print(bitstamp.getCurrentPrice("USD","LTC"))
#print(bitstamp.getCurrentPrice("ETH","USD"))
#print(bitfinex.getCurrentPrice("BTC","USD"))
#print(bitfinex.getCurrentPrice("USD","LTC"))
#print(bitfinex.getCurrentPrice("ETH","USD"))
print bitfinex.getCurrentPrice("BTC","ETH")
print poloniex.getCurrentPrice("BTC","ETH")
