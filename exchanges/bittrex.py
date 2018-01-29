import commands
import json

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  if (download > 0):
    commands.getoutput("wget --no-check-certificate -O bittrex https://bittrex.com/api/v1.1/public/getmarketsummaries")
  file="bittrex"
  with open(file, 'r') as conf:
    bittrex = json.load(conf)
  for market in bittrex['result']:
    tmp = market['MarketName']
    cur1 = tmp.split('-')[1].lower()
    cur2 = tmp.split('-')[0].lower()
    prices['bid'][cur1 + "_" + cur2] = float(market['Bid'])
    prices['ask'][cur1 + "_" + cur2] = float(market['Ask'])
  return prices
