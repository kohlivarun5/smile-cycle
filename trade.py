import logging
from exchanges import coinbase_api,coindelta

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

from datastore.CoinbaseCoindeltaTransaction import CoinbaseCoindeltaTransaction
def save_tx(tx,chat_id,buyer_id):
    try:
        forex = forex.get_prices()['bid']['usd_inr']
    except:
        forex = 0.
    key = CoinbaseCoindeltaTransaction(chat_id=chat_id,
                                       tx_id=tx.id,
                                       buyer_id=buyer_id,
                                       cost_in_usd=float(tx.native_amount.amount),
                                       forex_rate_inr_in_usd=float(forex),
                                       id=tx.id)
    return key.put()

def update_tx(tx_id,inr_settlement=None,fees_to_buy_in_usd=None):
    db_tx = CoinbaseCoindeltaTransaction.get_by_id(tx_id)
    if inr_settlement:
        db_tx.inr_settlement = inr_settlement
    if fees_to_buy_in_usd:
        db_tx.fees_to_buy_in_usd=fees_to_buy_in_usd
    return db_tx.put()

def tx_list_summary(chat_id):
    query = CoinbaseCoindeltaTransaction.query(
                CoinbaseCoindeltaTransaction.chat_id == chat_id)
    
    text = "`Cost($)` | `Made(Rs)` | `%(pp)`|"
    for tx in query:
        if tx.inr_settlement:
            inr_settlement = "%.4g" % tx.inr_settlement
            inr_settlement = inr_settlement.ljust(8)
        else:
            inr_settlement = " - "
            inr_settlement = inr_settlement.center(8)

        usd_cost = "%.4g" % (tx.cost_in_usd * -1)
        usd_cost = usd_cost.ljust(7)

        if tx.inr_settlement:
            usd_made = tx.inr_settlement / tx.forex_rate_inr_in_usd
            profit_per_person = "%.4g%%" % ( (usd_made-tx.cost_in_usd) / tx.cost_in_usd * 100 / 2)
            profit_per_person = profit_per_person.ljust(5)
        else:
            profit_per_person = " - "
            profit_per_person = profit_per_person.center(5)

        text+="\n`%s` | `%s` | `%s`|" %(usd_cost,inr_settlement,profit_per_person)
    return text

def send_coinbase_coindelta(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    client = coinbase_api.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    to = coindelta.ADDRESSES.get(currency)
    if to == None:
        raise UserWarning("No coindelta address for currency:%s" % currency)
    tx = coinbase_api.send(client,to,amount,currency)
    print(tx)
    logging.info(tx)
    return tx

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
