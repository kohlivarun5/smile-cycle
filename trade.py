from exchanges import coinbase_api,coindelta
def send_coinbase_coindelta(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    cb_client = coinbase_api.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    coinbase_api.send(client,coindelta.ADDRESSES["currency"],amount,currency)


"""
Parse a send command
/send_from coinbase 1 ETH 
"""
def parse_send_message(text):
    tokens = text.split(" ")
    assert tokens[0].startswith("/")
    tokens.pop(0)

    assert (3 == len(tokens))
    exchange = tokens[0].lower()
    amount = float(tokens[1])
    assert (amount > 0)
    currency = tokens[2].upper()
#
    return (exchange,amount,currency) 


import unittest
class TestParse(unittest.TestCase):
    def test_empty(self):
        self.assertRaises(AssertionError,parse_send_message,"")

    def test_bad_start(self):
        self.assertRaises(AssertionError,parse_send_message,"coinbase 1 ETH")

    def test_bad_format_misplaced_amount(self):
        self.assertRaises(ValueError,parse_send_message,"/send_from coinbase ETH 1")
        self.assertRaises(ValueError,parse_send_message,"/send_from 1 ETH coinbase")

    def test_bad_format_bad_amount(self):
        self.assertRaises(AssertionError,parse_send_message,"/send_from coinbase -1 ETH")
        self.assertRaises(AssertionError,parse_send_message,"/send_from coinbase 0 ETH")

    def test_correct_format(self):
        self.assertEqual(("coinbase",1,"ETH"),parse_send_message("/send_from coinbase 1 ETH"))
        self.assertEqual(("coinbase",1,"ETH"),parse_send_message("/send_from Coinbase 1 eth"))
        self.assertEqual(("coinbase",1.2,"ETH"),parse_send_message("/send_from coinbase 1.2 ETH"))

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
            account = coinbase_api.account(client,currency)
            if account is not None:
                self.assertLess(0,account.balance.amount) 

    def test_tx(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        tx_id = "e0f5eff6-54bd-59f0-bd70-42af7d967791"
        transaction = coinbase_api.tx(client,tx_id)
        self.assertEqual("send",transaction.type)
        self.assertEqual("confirmed",transaction.network.status)

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
