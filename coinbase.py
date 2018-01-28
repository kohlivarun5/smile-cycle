import commands
import json

def get_prices(download=1):
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
