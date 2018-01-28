import commands
import json

def get_prices(download=1):
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
