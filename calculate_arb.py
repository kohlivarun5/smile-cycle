"""
Each function returns the results in  a dict containing:
    { 
        "from" : "From Exchange",
        "to"   : "To Exchange",
        "gain_perc" : "Gain in %",
        "coin"  : "Base coin"
    }
"""
import json
import coindelta
import coinbase
import forex

def coinbase_coindelta():
    prices = {}
    prices['coinbase'] = coinbase.get_prices()
    prices['coindelta'] = coindelta.get_prices()
    prices['forex'] = forex.get_prices()
    result = []

    for i in prices.keys():
      for j in prices.keys():
        if (i == j):
          continue
        for cur in prices[i]['bid'].keys():
          if (cur.split('_')[1] != 'usd'):
            continue
          if (cur.split('_')[0] + "_inr" not in prices[j]['bid'].keys()):
            continue
          buy_amt = 1000
          buy = buy_amt/prices[i]['ask'][cur]
          sell = (buy - 0.001) * prices[j]['bid'][cur.split('_')[0] + "_inr"]
          buy_flow = buy_amt * prices['forex']['bid']['usd_inr']
          profit = sell - buy_flow
          if (profit > 0):
            result.append({'from' : i, 'to' : j, 'coin' : cur.split('_')[0], 'gain_perc' : profit*100/buy_flow})

    return result

if __name__ == "__main__":
    print(coinbase_coindelta())
