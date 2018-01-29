import commands
import json

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}

  symbols="btcusd,btceur,eurusd,xrpusd,xrpeur,xrpbtc,ltcusd,ltceur,ltcbtc,ethusd,etheur,ethbtc,bchusd,bcheur,bchbtc"
  for symbol in symbols.split(','):
    if (download > 0):
      commands.getoutput("wget -O " + symbol + ".bitstamp https://www.bitstamp.net/api/v2/ticker/" + symbol)
    file="" + symbol + ".bitstamp"
    with open(file, 'r') as conf:
      info = json.load(conf)
    prices['bid'][symbol[0:3] + "_" + symbol[3:]] = float(info['bid'])
    prices['ask'][symbol[0:3] + "_" + symbol[3:]] = float(info['ask'])
  return prices
