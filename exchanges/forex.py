import json
import urllib2

def query():
  url = "https://api.fixer.io/latest"
  response = urllib2.urlopen(url, timeout = 5)
  return json.load(response)

def get_prices():
  exch_rates=query()
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  prices['bid']['usd_inr'] = float(exch_rates['rates']['INR'])/float(exch_rates['rates']['USD'])
  prices['ask']['usd_inr'] = float(exch_rates['rates']['INR'])/float(exch_rates['rates']['USD'])
  return prices
