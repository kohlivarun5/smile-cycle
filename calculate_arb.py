"""
Each function returns the results in  a dict containing:
    { 
        "from" : "From Exchange",
        "to"   : "To Exchange",
        "gain_perc" : "Gain in %",
        "coin"  : "Base coin"
    }
"""

from exchanges import coindelta
from exchanges import koinex
from exchanges import coinbase_api
from exchanges import forex
def coinbase_coindelta():
    prices = {}
    prices['coinbase'] = coinbase_api.get_prices()
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
            result.append({'from' : i, 'to' : j, 'coin' : cur.split('_')[0].upper(), 'gain_perc' : profit*100/buy_flow})

    return result

def coinbase_koinex():
    prices = {}
    prices['coinbase'] = coinbase_api.get_prices()
    prices['koinex'] = koinex.get_prices()
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
            result.append({'from' : i, 'to' : j, 'coin' : cur.split('_')[0].upper(), 'gain_perc' : profit*100/buy_flow})

    return result

from exchanges import binance
from exchanges import kucoin
def binance_kucoin():
    result = []
    fees = {}
    fees['binance'] = binance.get_fees()
    prices = {}
    prices['binance'] = binance.get_prices()
    prices['kucoin'] = kucoin.get_prices()
    buy_amts = {}
    buy_amts['btc'] = 0.1
    buy_amts['inr'] = 50000
    buy_amts['usd'] = 1000
    for c in prices['binance']['bid'].keys():
        cur1 = c.split('_')[0]
        cur2 = c.split('_')[1]
        if (cur2 == 'btc'):
            buy_amts[cur1] = 0.1/prices['binance']['bid'][c]
    for i in prices.keys():
        for j in prices.keys():
            if (i == j):
                continue
            set1 = set(prices[i]['bid'].keys())
            set2 = set(prices[j]['bid'].keys())
            curs = set1.intersection(set2)
            for cur in curs:
                cur1 = cur.split('_')[0]
                cur2 = cur.split('_')[1]
                buy_amt = buy_amts.get(cur2, 1) # assuming buy amt as 1 in cur2 terms if not found
                buy = buy_amt/prices[i]['ask'][cur]
                fee = fees['binance'].get(cur1, 1) # assuming withdrawal fee as 1 if not found
                sell = (buy - fee) * prices[j]['bid'][cur]
                gain = (sell - buy_amt)*100
                if (gain > 2*buy_amt and gain < 60*buy_amt) :
                    # appending only if > 2% profit and < 60% (to prevent false positives)
                    coin = "Buy %s using %s" % (cur1.upper(),cur2.upper())
                    result.append({'from' : i, 'to' : j, 'coin' : coin, 'gain_perc' : (sell - buy_amt)*100/buy_amt})
    return result


import unittest
class TestCalcs(unittest.TestCase):
    def test_coinbase_coindelta(self):
        arbs = coinbase_coindelta()
        #import formatting
        #print(formatting.text_of_arbs(arbs))
        if len(arbs) != 0:
            for arb in arbs:
                self.assertEqual("coinbase",arb["from"])
                self.assertEqual("coindelta",arb["to"])
                self.assertEqual(3,len(arb["coin"]))
                self.assertEqual("float",type(arb["gain_perc"]).__name__)

    def test_binance_kucoin(self):
        arbs = binance_kucoin()
        if len(arbs) != 0:
            for arb in arbs:
                self.assertLessEqual(3,len(arb["coin"]))
                self.assertEqual("float",type(arb["gain_perc"]).__name__)

    def test_coinbase_koinex(self):
        arbs = coinbase_koinex()
        #import formatting
        #print(formatting.text_of_arbs(arbs))
        if len(arbs) != 0:
            for arb in arbs:
                self.assertEqual("coinbase",arb["from"])
                self.assertEqual("koinex",arb["to"])
                self.assertEqual(3,len(arb["coin"]))
                self.assertEqual("float",type(arb["gain_perc"]).__name__)

