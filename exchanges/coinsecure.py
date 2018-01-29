import commands
import json

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  if (download > 0):
    commands.getoutput("wget -O coinsecure https://api.coinsecure.in/v1/exchange/ticker")
  file="coinsecure"
  with open(file, 'r') as conf:
    coinsecure = json.load(conf)
  prices['bid']['btc_inr'] = float(coinsecure['message']['bid'])/100
  prices['ask']['btc_inr'] = float(coinsecure['message']['ask'])/100
  return prices
