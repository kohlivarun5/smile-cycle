import json
import urllib2

def query():
  url = "https://coindelta.com/api/v1/public/getticker"
  response = urllib2.urlopen(url, timeout = 5)
  return json.load(response)


def get_prices():
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  coindelta = query()
  for market in coindelta:
    cur = market['MarketName'].split('-')
    prices['bid'][cur[0] + "_" + cur[1]] = float(market['Bid'])
    prices['ask'][cur[0] + "_" + cur[1]] = float(market['Ask'])
  return prices

ADDRESSES = {
    "ETH" : "0xA0fCE563cA8cAB01ef12fd2d7a1f193E37a982d2",
    "LTC" : "LYzTCSzfCXaVVpvB5qTx7Xqz4qU7VYyVwf"
}

CONFIRMATIONS = {
    "ETH" : 25,
    "LTC" : 6
}
