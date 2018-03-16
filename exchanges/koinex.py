import urllib2
import json

def query():
  url = "https://koinex.in/api/ticker"
  response = urllib2.urlopen(url, timeout = 5)
  return json.load(response)


def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  koinex = query()
  for prod in koinex['stats'].keys():
    market = koinex['stats'][prod]
    highest_bid = market.get('highest_bid')
    lowest_ask = market.get('lowest_ask')
    if highest_bid and lowest_ask:
        prices['bid'][prod.lower() + "_inr"] = float(highest_bid)
        prices['ask'][prod.lower() + "_inr"] = float(lowest_ask)
  return prices


ADDRESSES = {
    "ETH" : "0xbfad5b9dc635de580ec87f2340c8a29b2055eb60",
    "LTC" : "LXR9gNKxAVtgapKjmKxtcCi9WYdTzXsXSr",
    "BCH" : "1JgUgB8fZaiPyqztipK4qE42gTaEf6xQ2g"
}

CONFIRMATIONS = {
    "ETH" : 32,
    "LTC" : 6,
    "BCH" : 8
}
