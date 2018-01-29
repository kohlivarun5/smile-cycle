import json
import urllib2

def query(currency, direction):
  url = "https://api.coinbase.com/v2/prices/" + currency + "-USD/" + direction
  response = urllib2.urlopen(url, timeout = 5)
  return json.load(response)

def get_prices():
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  curs = ['btc', 'eth', 'ltc', 'bch']
  for c in curs:
    tmp = query(c.upper(),"sell")
    prices['bid'][c + "_usd"] = float(tmp['data']['amount'])
  for c in curs:
    tmp = query(c.upper(),"buy")
    prices['ask'][c + "_usd"] = float(tmp['data']['amount'])
  return prices
