"""
Each function returns the results in  a dict containing:
    { 
        "from" : "From Exchange",
        "to"   : "To Exchange",
        "gain_perc" : "Gain in %",
        "coin"  : "Base coin"
    }
"""
import json
import commands

def get_coindelta_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  if (download > 0):
    commands.getoutput("wget -O coindelta https://coindelta.com/api/v1/public/getticker")
  file="coindelta"
  with open(file, 'r') as conf:
    coindelta = json.load(conf)
  for market in coindelta:
    cur = market['MarketName'].split('-')
    prices['bid'][cur[0] + "_" + cur[1]] = float(market['Bid'])
    prices['ask'][cur[0] + "_" + cur[1]] = float(market['Ask'])
  return prices

def get_coinbase_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  curs = ['btc', 'eth', 'ltc', 'bch']
  for c in curs:
    if (download > 0):
      commands.getoutput("wget -O " + c + ".coinbase.sell https://api.coinbase.com/v2/prices/" + c.upper() + "-USD/sell")
    file = "" + c + ".coinbase.sell"
    with open(file, 'r') as conf:
      tmp = json.load(conf)
    prices['bid'][c + "_usd"] = float(tmp['data']['amount'])
  for c in curs:
    if (download > 0):
      commands.getoutput("wget -O " + c + ".coinbase.buy https://api.coinbase.com/v2/prices/" + c.upper() + "-USD/buy")
    file = "" + c + ".coinbase.buy"
    with open(file, 'r') as conf:
      tmp = json.load(conf)
    prices['ask'][c + "_usd"] = float(tmp['data']['amount'])
  return prices

def get_forex_prices(download=1):
  if (download > 0):
    commands.getoutput("wget -O forex https://api.fixer.io/latest")
  file="forex"
  with open(file, 'r') as conf:
    exch_rates = json.load(conf)
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  prices['bid']['usd_inr'] = float(exch_rates['rates']['INR'])/float(exch_rates['rates']['USD'])
  prices['ask']['usd_inr'] = float(exch_rates['rates']['INR'])/float(exch_rates['rates']['USD'])
  return prices

prices = {}
prices['coinbase'] = get_coinbase_prices()
prices['coindelta'] = get_coindelta_prices()
prices['forex'] = get_forex_prices()
result = []
for i in prices.keys():
  for j in prices.keys():
    if (i == j):
      continue
    for cur in prices[i]['bid'].keys():
      if (cur.split('_')[1] != 'usd'):
        continue
      if (cur.split('_')[0] + "_inr" not in prices[j]['bid'].keys()):
        continue
      buy_amt = 1000
      buy = buy_amt/prices[i]['ask'][cur]
      sell = (buy - 0.001) * prices[j]['bid'][cur.split('_')[0] + "_inr"]
      buy_flow = buy_amt * prices['forex']['bid']['usd_inr']
      profit = sell - buy_flow
      if (profit > 0):
        result.append({'from' : i, 'to' : j, 'coin' : cur.split('_')[0], 'gain_perc' : profit*100/buy_flow})

def coinbase_coindelta():
    return result
