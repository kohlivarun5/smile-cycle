import json
import re
import urllib2

def get_fees():
  file="binance_fees"
  fees = {}
  with open(file, 'r') as conf:
    for line in conf:
      x = re.split('\s+', line)
      fees[x[1].lower()] = float(x[0])
  return fees

def query():
  url = "https://api.binance.com/api/v1/ticker/24hr"
  response = urllib2.urlopen(url, timeout=5)
  return json.load(response)

def get_prices():
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  prices['bqty'] = {}
  prices['aqty'] = {}
  binance = query()
  for market in binance:
    cur = market['symbol'][0:3].lower()
    cur1 = market['symbol'][3:].lower()
    prices['bid'][cur + "_" + cur1] = float(market['bidPrice'])
    prices['ask'][cur + "_" + cur1] = float(market['askPrice'])
    prices['bqty'][cur + "_" + cur1] = float(market['bidQty'])
    prices['aqty'][cur + "_" + cur1] = float(market['askQty'])
  return prices
