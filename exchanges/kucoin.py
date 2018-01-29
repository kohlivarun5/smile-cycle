import json
import urllib2

def query():
  url = "https://api.kucoin.com/v1/open/tick"
  response = urllib2.urlopen(url, timeout=5)
  return json.load(response)

def get_prices():
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  kucoin = query()
  for market in kucoin['data']:
    tmp = market['symbol']
    cur = tmp.split('-')[0].lower()
    cur1 = tmp.split('-')[1].lower()
    if 'buy' in market.keys():
      prices['bid'][cur + "_" + cur1] = float(market['buy'])
      prices['ask'][cur + "_" + cur1] = float(market['sell'])
  return prices
