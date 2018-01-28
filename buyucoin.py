import commands
import json

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  if (download > 0):
    commands.getoutput("wget -O buyucoin https://www.buyucoin.com/api/v1/crypto")
  file="buyucoin"
  with open(file, 'r') as conf:
    buyucoin = json.load(conf)

  for data in buyucoin['BuyUcoin_data'][0].keys():
    cur = data.split('_')[0]
    if (data.split('_')[1] == 'buy'):
      side = 'ask'
    else:
      side = 'bid'
    prices[side][cur+"_inr"] = float(buyucoin['BuyUcoin_data'][0][data])
  return prices
