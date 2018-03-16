import logging
from exchanges import coinbase_api

COINBASE_TRANSACTION_ID_BASE="Coinbase Transaction id: "

import re
def parse_coinbase_transaction_id(text):
    ids = re.findall(r''+COINBASE_TRANSACTION_ID_BASE+r'(.*)\n',text)
    if 1 != len(ids):
        raise UserWarning("Could not find transaction id!")
    return ids[0]

def coinbase_transaction_info(tx):
    text = ""
    text +="%s%s" % (COINBASE_TRANSACTION_ID_BASE,tx.id)
    if tx.network.status == "confirmed":
        #text +="\nHash: %s" % tx.network.hash
        text +="\n*Confirmations: %d*" % tx.network.confirmations
    else:
        text +="\nStatus: *%s*" % tx.network.status.title()

    text +="\n\nTotal Cost: *%s%s*" % (tx.native_amount.amount,tx.native_amount.currency)
    text +="\nAmount: %s%s" % (tx.network.transaction_amount.amount,tx.network.transaction_amount.currency)
    #text +="\nFees: %s%s" % (tx.network.transaction_fee.amount,tx.network.transaction_fee.currency)
    return text 

from exchanges import forex
from datastore.CoinbaseCoindeltaTransaction import CoinbaseCoindeltaTransaction
def save_tx(tx,chat_id,buyer_id):
    fx = forex.get_prices()['bid']['usd_inr']
    key = CoinbaseCoindeltaTransaction(chat_id=chat_id,
                                       tx_id=tx.id,
                                       buyer_id=buyer_id,
                                       cost_in_usd=abs(float(tx.native_amount.amount)),
                                       forex_rate_inr_in_usd=float(fx),
                                       id=tx.id)
    key.put()
    return "Done"

def update_tx(tx_id,inr_settlement=None,seller_id=None,fees_to_buy_in_usd=None):
    db_tx = CoinbaseCoindeltaTransaction.get_by_id(tx_id)
    if inr_settlement:
        db_tx.inr_settlement = inr_settlement
    if fees_to_buy_in_usd:
        db_tx.fees_to_buy_in_usd=fees_to_buy_in_usd
    if seller_id:
        db_tx.seller_id=seller_id
    db_tx.put()
    return "Done"

def tx_list_summary(chat_id):
    query = CoinbaseCoindeltaTransaction.query(
                CoinbaseCoindeltaTransaction.chat_id == chat_id
            ).order(-CoinbaseCoindeltaTransaction.date)
    
    text = "Trades:\n"
    text += "`Date  `|`Cost$`|`Made(Rs)`|`%(pp)`|"
    total_cost_usd = 0
    total_profit_per_person_usd = 0 
    for tx in query:
        date = tx.date.strftime('%d%b').ljust(6)

        inr_settlement = "%.0f" % tx.inr_settlement
        inr_settlement = inr_settlement.ljust(8)

        trade_cost = tx.cost_in_usd + tx.fees_to_buy_in_usd
        total_cost_usd += trade_cost
        usd_cost = "%.0f" % trade_cost
        usd_cost = usd_cost.ljust(5)

        usd_made = tx.inr_settlement / tx.forex_rate_inr_in_usd
        profit = (usd_made - trade_cost)/2
        total_profit_per_person_usd += profit
        profit_per_person = "%.2f" % ( (profit) / trade_cost * 100 )
        profit_per_person = profit_per_person.ljust(5)

        text+="\n`%s`|`%s`|`%s`|`%s`|" %(date,usd_cost,inr_settlement,profit_per_person)
    return (total_cost_usd,total_profit_per_person_usd,text)

from datastore.BankSettlement import BankSettlement 
def save_bank_settlement(chat_id,sender_id,amount_usd):
    fx = forex.get_prices()['bid']['usd_inr']
    key = BankSettlement(chat_id=chat_id,
                         sender_id=sender_id,
                         amount_usd=amount_usd,
                         amount_inr=(amount_usd*float(fx)))
    key.put()
    return "Done"

def bank_settlement_summary(chat_id):
    query = BankSettlement.query(
                BankSettlement.chat_id == chat_id
            ).order(-BankSettlement.date)
    
    text = "Settlements:\n"
    text+= "`Date  ` | `Amount($)` |"
    total_amount_usd = 0
    for settlement in query:
        date = settlement.date.strftime('%d%b').ljust(6)
        total_amount_usd+= settlement.amount_usd
        amount_usd = "%.4g" % settlement.amount_usd
        amount_usd = amount_usd.ljust(9)
        text+="\n`%s` | `%s` |" % (date,amount_usd)
    return (total_amount_usd,text)

def summary_of_history(total_cost_usd,total_profit_per_person_usd,total_amount_usd):
    text="Summary:"
    text+="\nTotal Profit: $%.0f_(%.2f%%)_" % (total_profit_per_person_usd,(total_profit_per_person_usd/total_cost_usd*100))
    text+="\nTotal Cost: $%.0f" % total_cost_usd
    text+="\nTotal Settled: $%.0f" % total_amount_usd
    text+="\nPending: *$%.2f*" % (total_cost_usd+total_profit_per_person_usd-total_amount_usd)
    return text 

def send_coinbase_coindelta(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    from exchanges import coindelta
    client = coinbase_api.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    to = coindelta.ADDRESSES.get(currency)
    if to == None:
        raise UserWarning("No coindelta address for currency:%s" % currency)
    tx = coinbase_api.send(client,to,amount,currency)
    print(tx)
    target_confirmations = coindelta.CONFIRMATIONS.get(tx["to"]["currency"])
    logging.info(tx)
    return (tx,target_confirmations)

def send_coinbase_koinex(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    from exchanges import koinex
    client = coinbase_api.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    to = koinex.ADDRESSES.get(currency)
    if to == None:
        raise UserWarning("No koinex address for currency:%s" % currency)
    tx = coinbase_api.send(client,to,amount,currency)
    print(tx)
    target_confirmations = koinex.CONFIRMATIONS.get(tx["to"]["currency"])
    logging.info(tx)
    return (tx,target_confirmations)

def get_coinbase_balance(COINBASE_API_KEY,COINBASE_API_SECRET):
    client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
    accounts = client.get_accounts()["data"]
    text = ""
    for account in accounts:
        text+="\n%s : %s (*%s%s*)" % (account.balance.currency,account.balance.amount,account.native_balance.amount,account.native_balance.currency)
    return text

import unittest
import credentials
class TestCoinbase(unittest.TestCase):
    def test_client(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        user = client.get_current_user()
        self.assertEqual("3a2b719d-f765-52ba-a027-a91d1965972e",user.id)
        self.assertEqual("Varun Kohli",user.name)

    def test_account(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        currencies = ["ETH","LTC","BCH"]
        for currency in currencies:
            try:
                account = coinbase_api.account(client,currency)
                self.assertLess(0,account.balance.amount) 
            except UserWarning as e:
                #print e
                pass

    def test_tx(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        tx_id = "e0f5eff6-54bd-59f0-bd70-42af7d967791"
        transaction = coinbase_api.tx(client,tx_id)
        self.assertEqual("send",transaction.type)
        self.assertEqual("confirmed",transaction.network.status)

    def test_tx2(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        tx_id = "da5769b3-4da4-56f8-8c41-c8cb8085bfb2"
        transaction = coinbase_api.tx(client,tx_id)
        #print transaction
        #print(coinbase_transaction_info(transaction))
        self.assertEqual("send",transaction.type)
        self.assertEqual("confirmed",transaction.network.status)

    def test_tx_bad(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        self.assertRaises(UserWarning,coinbase_api.tx,client,"")

    def test_get_balance(self):
        text = get_coinbase_balance(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        #print text
        self.assertLess(0,len(text))

    def test_all(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        # print(user)
        accounts = client.get_accounts()["data"]
        #print accounts
        #print(client.get_primary_account())
        for account in accounts:
            for tx in account.get_transactions()["data"]:
                transaction = coinbase_api.tx(client,tx.id)

            #print(account.get_addresses())
            #print(client.get_addresses(account.id))
            #client.get_address(account_id, address_id)
        # client.get_transaction(account_id, transaction_id)


class TestSendCoinbaseCoindelta(unittest.TestCase):
    def test_bad_ccy(self):
        self.assertRaises(UserWarning,send_coinbase_coindelta,credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET,1,"")

    def test_zero_amount(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        self.assertRaises(UserWarning,send_coinbase_coindelta,credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET,0,"ETH")
    
    #def test_simple_amount(self):
    #    client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
    #    text = send_coinbase_coindelta(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET,0.001,"ETH")
    #    print(text)
    #    self.assertLess(0,len(text))
