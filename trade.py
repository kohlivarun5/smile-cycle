from exchanges import coinbase,coindelta
def send_coinbase_coindelta(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    cb_client = coinbase.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    coinbase.send(client,coindelta.ADDRESSES["currency"],amount,currency)


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


