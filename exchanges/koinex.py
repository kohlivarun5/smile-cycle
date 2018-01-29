import commands
import json

def get_prices(download=1):
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  if (download > 0):
    commands.getoutput("wget -O koinex https://koinex.in/api/ticker")
  file="koinex"
  with open(file, 'r') as conf:
    koinex = json.load(conf)

  for prod in koinex['stats'].keys():
    market = koinex['stats'][prod]
    prices['bid'][prod.lower() + "_inr"] = float(market['highest_bid'])
    prices['ask'][prod.lower() + "_inr"] = float(market['lowest_ask'])
  return prices
