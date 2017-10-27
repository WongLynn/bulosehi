import json as json
import requests as req

class CrossPairings:
  def __init__(self):
    #A dictionary of the form {'BTC':[Bitfinex,Bitstamp,Poloniex,...],...}
    self.exchangesByTicker={}

  def addExchanges(self, exchangesDict):
    """
    Expects Dictionary of form {"Kraken":kraken,...}, where kraken is a full Exchange Object
    Populates the exchangesByTicker dict
    """
    for exchName in exchangesDict.keys():
      for ticker in exchangesDict[exchName].pairsByTicker:
        if not ticker in self.exchangesByTicker:
          self.exchangesByTicker[ticker] = [exchName]
        else:
          self.exchangesByTicker[ticker].append(exchName)

  def getExchanges(self, primary, secondary):
    """
    Return exchanges that have the matching ticker
    """
    exchs = []
    for tikA in self.exchangesByTicker[primary]:
      for tikB in self.exchangesByTicker[secondary]:
        if tikA == tikB and not tikB in exchs and not tikB in exchs:
          exchs.append(tikA)
    return exchs



class Exchange:
  def __init__(self):
    #Holds all trading pairs in the exchange
    self.allPairs = self.getPairs
    #Holds all available single Tickers e.g. BTC, USD etc.
    self.availableTickers = []
    #A dictionary of the form: {'BTC':[btcusd,btceur,...],...}
    self.pairsByTicker = {}

  def getJson(self,url):
    """
    Gets the json at the url location and returns a json object
    """
    r = req.get(str(url),"GET")
    jsonResponse = json.loads(r.text)
    return jsonResponse

  def getTradedPair(self,primary,secondary):
    for i in self.pairsByTicker[primary]:
      for j in self.pairsByTicker[secondary]:
        if i == j:
          return i

class Kraken(Exchange):
  def __init__(self):
    self.allPairs = self.getPairs()
    self.availableTickers = self.getTradedTickers()
    self.pairsByTicker = self.orderPairs()

  def getPairs(self):
    """
    Returns traded Currency Pairs on Kraken
    """
    jsonResponse = self.getJson("https://api.kraken.com/0/public/AssetPairs")
    allPairs = []
    for i in jsonResponse["result"]:
      allPairs.append(i.split(".d",1)[0])
    return allPairs

  def getTradedTickers(self):
    """
    Returns traded Tickers on Kraken
    """
    jsonResponse = self.getJson("https://api.kraken.com/0/public/Assets")
    availableTickers = []
    for i in jsonResponse["result"]:
      availableTickers.append(i)
    return availableTickers

  def orderPairs(self):
    """
    Order Pairs by Common Ticker into a dict
    """
    pairsByTickers = {}
    for asset in self.availableTickers:
      if asset[0]=="X" or asset[0]=="Z":
        asset = asset[1:]
      holder = []
      for pair in self.allPairs:
        if asset in pair:
          holder.append(pair)
      if asset == "XBT":
        asset = "BTC"
      pairsByTickers[asset] = holder
    return pairsByTickers

  def getCurrentPrice(self,primary,secondary):
    """
    Gets the current price of a traded currency pair on Kraken
    """
    pair = self.getTradedPair(primary,secondary)
    uri = "https://api.kraken.com/0/public/Ticker"
    requestUrl = uri + "?pair=" + pair
    jsonResponse = self.getJson(requestUrl)
    currentPrice = jsonResponse["result"][pair]["c"]
    return currentPrice


class Bitstamp(Exchange):
  def __init__(self):
    self.allPairs = ["btcusd", "btceur", "eurusd", "xrpusd", "xrpeur", "xrpbtc", "ltcusd", "ltceur", "ltcbtc", "ethusd", "etheur", "ethbtc"]
    self.availableTickers = self.formatTickers()
    self.pairsByTicker = self.orderPairs()

  def formatTickers(self):
    """
    Format ticker to uppercase and unique symbols for every traded asset
    """
    availableTickers = []
    for pair in self.allPairs:
      if not pair.upper()[0:3] in availableTickers:
        availableTickers.append(pair.upper()[0:3])
      if not pair.upper()[3:] in availableTickers:
        availableTickers.append(pair.upper()[3:])
    return availableTickers

  def orderPairs(self):
    """
    Order Pairs by Common Ticker into a dict
    """
    pairsByTickers = {}
    for asset in self.availableTickers:
      holder = []
      for pair in self.allPairs:
        if asset.lower() in pair:
          holder.append(pair)
        pairsByTickers[asset] = holder
    return pairsByTickers

  def getTicker(self,primary,secondary):
    """
    Returns the complete Json response for calling the ticker of a specific pair
    """
    pair = self.getTradedPair(primary,secondary)
    uri = "https://www.bitstamp.net/api/v2/ticker/"
    requestUrl = uri + pair
    return self.getJson(requestUrl)


  def getCurrentPrice(self,primary,secondary):
    """
    Gets the current price of a traded currency pair on Kraken
    """
    currentPrice = self.getTicker(primary,secondary)
    return currentPrice["last"]


class Bitfinex(Exchange):
  def __init__(self):
    self.allPairs = self.getJson("https://api.bitfinex.com/v1/symbols")
    self.availableTickers = self.formatTickers()
    self.pairsByTicker = self.orderPairs()

  def formatTickers(self):
    """
    Format ticker to uppercase and unique symbols for every traded asset
    """
    availableTickers = []
    for pair in self.allPairs:
      if not pair.upper()[0:3] in availableTickers:
        availableTickers.append(pair.upper()[0:3])
      if not pair.upper()[3:] in availableTickers:
        availableTickers.append(pair.upper()[3:])
    return availableTickers

  def orderPairs(self):
    """
    Order Pairs by Common Ticker into a dict
    """
    pairsByTickers = {}
    for asset in self.availableTickers:
      holder = []
      for pair in self.allPairs:
        if asset.lower() in pair:
          holder.append(pair.upper())
        pairsByTickers[asset] = holder
    return pairsByTickers

  def getCurrentPrice(self,primary,secondary):
    """
    Gets the current price of a traded currency pair on Kraken
    """
    pair = self.getTradedPair(primary,secondary)
    uri = "https://www.bitfinex.com/v2/ticker/t"
    requestUrl = uri + pair
    jsonResponse = self.getJson(requestUrl)
    currentPrice = jsonResponse[0]
    return currentPrice

class Poloniex(Exchange):
  def __init__(self):
    self.allPairs = self.getPairs()
    self.availableTickers = self.getTradedTickers()
    self.pairsByTicker = self.orderPairs()

  def getPairs(self):
    """
    Returns traded Currency Pairs on Kraken
    """
    jsonResponse = self.getJson("https://poloniex.com/public?command=returnTicker")
    allPairs = []
    for i in jsonResponse:
      allPairs.append(i)
    return allPairs

  def getTradedTickers(self):
    """
    Returns traded Tickers on Kraken
    """
    availableTickers = []
    for i in self.allPairs:
      i,j = i.split("_")
      if not i in availableTickers:
        availableTickers.append(i)
      if not j in availableTickers:
        availableTickers.append(j)
    return availableTickers

  def orderPairs(self):
    """
    Order Pairs by Common Ticker into a dict
    """
    pairsByTickers = {}
    for asset in self.availableTickers:
      if asset[0]=="X" or asset[0]=="Z":
        asset = asset[1:]
      holder = []
      for pair in self.allPairs:
        if asset in pair:
          holder.append(pair)
      if asset == "XBT":
        asset = "BTC"
      pairsByTickers[asset] = holder
    return pairsByTickers

  def getCurrentPrice(self,primary,secondary):
    """
    Gets the current price of a traded currency pair on Kraken
    """
    pair = self.getTradedPair(primary,secondary)
    jsonResponse = self.getJson("https://poloniex.com/public?command=returnTicker")
    currentPrice = jsonResponse[pair]["last"]
    return currentPrice

class Bittrex(Exchange):
  def __init__(self):
    self.allPairs = self.getPairs()
    self.availableTickers = self.getTradedTickers()
    self.pairsByTicker = self.orderPairs()

  def getPairs(self):
    """
    Returns traded Currency Pairs on Kraken
    """
    jsonResponse = self.getJson("https://poloniex.com/public?command=returnTicker")
    allPairs = []
    for i in jsonResponse:
      allPairs.append(i)
    return allPairs

  def getTradedTickers(self):
    """
    Returns traded Tickers on Kraken
    """
    availableTickers = []
    for i in self.allPairs:
      i,j = i.split("_")
      if not i in availableTickers:
        availableTickers.append(i)
      if not j in availableTickers:
        availableTickers.append(j)
    return availableTickers

  def orderPairs(self):
    """
    Order Pairs by Common Ticker into a dict
    """
    pairsByTickers = {}
    for asset in self.availableTickers:
      if asset[0]=="X" or asset[0]=="Z":
        asset = asset[1:]
      holder = []
      for pair in self.allPairs:
        if asset in pair:
          holder.append(pair)
      if asset == "XBT":
        asset = "BTC"
      pairsByTickers[asset] = holder
    return pairsByTickers

  def getCurrentPrice(self,primary,secondary):
    """
    Gets the current price of a traded currency pair on Kraken
    """
    pair = self.getTradedPair(primary,secondary)
    jsonResponse = self.getJson("https://poloniex.com/public?command=returnTicker")
    currentPrice = jsonResponse[pair]["last"]
    return currentPrice

