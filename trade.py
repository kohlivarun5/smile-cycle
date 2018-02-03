from exchanges import coinbase_api,coindelta
def send_coinbase_coindelta(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    client = coinbase_api.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    to = coindelta.ADDRESSES.get(currency)
    if to == None:
        raise UserWarning("No coindelta address for currency:%s" % currency)
    tx = coinbase_api.send(client,to,amount,currency)
    return tx

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

    def test_tx_bad(self):
        client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
        self.assertRaises(UserWarning,coinbase_api.tx,client,"")

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

