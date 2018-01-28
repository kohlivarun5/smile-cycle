import commands
import json
import re

def get_fees():
  file="binance.fees"
  fees = {}
  with open(file, 'r') as conf:
    for line in conf:
      x = re.split('\s+', line)
      fees[x[1].lower()] = float(x[0])
  return fees

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  prices['bqty'] = {}
  prices['aqty'] = {}
  if (download > 0):
    commands.getoutput("wget --no-check-certificate -O binance https://api.binance.com/api/v1/ticker/24hr")
  file="binance"
  with open(file, 'r') as conf:
    binance = json.load(conf)

  for market in binance:
    cur = market['symbol'][0:3].lower()
    cur1 = market['symbol'][3:].lower()
    prices['bid'][cur + "_" + cur1] = float(market['bidPrice'])
    prices['ask'][cur + "_" + cur1] = float(market['askPrice'])
    prices['bqty'][cur + "_" + cur1] = float(market['bidQty'])
    prices['aqty'][cur + "_" + cur1] = float(market['askQty'])
  return prices
