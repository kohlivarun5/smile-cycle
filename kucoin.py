import commands
import json

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  if (download > 0):
    commands.getoutput("wget --no-check-certificate -O kucoin https://api.kucoin.com/v1/open/tick")
  file="kucoin"
  with open(file, 'r') as conf:
    kucoin = json.load(conf)

  for market in kucoin['data']:
    tmp = market['symbol']
    cur = tmp.split('-')[0].lower()
    cur1 = tmp.split('-')[1].lower()
    if 'buy' in market.keys():
      prices['bid'][cur + "_" + cur1] = float(market['buy'])
      prices['ask'][cur + "_" + cur1] = float(market['sell'])
