import json
import urllib2

def query(base,cross):
  url = "https://api.fixer.io/latest?symbols=%s&base=%s" % (cross,base)
  response = urllib2.urlopen(url, timeout = 10)
  return json.load(response)

def get_prices():
  exch_rates=query("USD","INR")
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  usd_inr = float(exch_rates['rates']['INR'])
  prices['bid']['usd_inr'] = usd_inr
  prices['ask']['usd_inr'] = usd_inr
  return prices
