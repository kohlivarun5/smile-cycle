import json
import commands

def get_prices(download=1):
  if (download > 0):
    commands.getoutput("wget -O forex https://api.fixer.io/latest")
  file="forex"
  with open(file, 'r') as conf:
    exch_rates = json.load(conf)
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  prices['bid']['usd_inr'] = float(exch_rates['rates']['INR'])/float(exch_rates['rates']['USD'])
  prices['ask']['usd_inr'] = float(exch_rates['rates']['INR'])/float(exch_rates['rates']['USD'])
  return prices
