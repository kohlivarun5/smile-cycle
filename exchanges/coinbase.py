import json
import urllib2

def query(currency, direction):
  url = "https://api.coinbase.com/v2/prices/" + currency + "-USD/" + direction
  response = urllib2.urlopen(url, timeout = 5)
  return json.load(response)

def get_prices():
  prices = {}
  prices['bid'] = {}
  prices['ask'] = {}
  curs = ['btc', 'eth', 'ltc', 'bch']
  for c in curs:
    tmp = query(c.upper(),"sell")
    prices['bid'][c + "_usd"] = float(tmp['data']['amount'])
  for c in curs:
    tmp = query(c.upper(),"buy")
    prices['ask'][c + "_usd"] = float(tmp['data']['amount'])
  return prices 


def client(COINBASE_API_KEY,COINBASE_API_SECRET):
    from coinbase.wallet.client import Client
    return Client(COINBASE_API_KEY,
                  COINBASE_API_SECRET)

def send(client,to,amount,currency):
    account = client.get_primary_account()
    try:
      tx = account.send_money(to=to, amount=amount,currency=currency)
    except TwoFactorRequiredError:
      # Show 2FA dialog to user and collect 2FA token
      # two_factor_token = ...
      # Re-try call with the `two_factor_token` parameter
      # tx = account.send_money(to=to, amount='1', currency='BTC', two_factor_token="123456")
      print("Doesn't support 2FA right now!")
    print tx
