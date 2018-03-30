import json
import urllib2

def query(symbol):
  url = "https://www.bitstamp.net/api/v2/ticker/" + symbol
  response = urllib2.urlopen(url, timeout = 5)
  return json.load(response)


def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}

  symbols=[
      "btcusd","xrpusd","xrpbtc","ltcusd","ltcbtc","ethusd","ethbtc","bchusd","bchbtc"
  ]
  for symbol in symbols:
    info = query(symbol)
    prices['bid'][symbol[0:3] + "_" + symbol[3:]] = float(info['bid'])
    prices['ask'][symbol[0:3] + "_" + symbol[3:]] = float(info['ask'])

  return prices
