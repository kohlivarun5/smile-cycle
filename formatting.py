def text_of_arbs(arbs_in, default_msg="No arbitrage found!"):
    arbs = sorted(arbs_in,key = lambda x:x["gain_perc"],reverse=True)
    #print(arbs)
    ## Collect by direction first
    direction_map = {}
    for idx, arb in enumerate(arbs):
        from_,to = arb["from"].title(),arb["to"].title()
        direction = "_%s -> %s_" %(from_,to)
        if direction not in direction_map:
            direction_map[direction] = []
        direction_map[direction].append(arb)

    text = ""
    for direction, arbs in direction_map.iteritems():
        for idx, arb in enumerate(arbs):
            from_,to,coin,gain_perc = arb["from"].title(),arb["to"].title(),arb["coin"],arb["gain_perc"]
            if idx == 0:
                text += "\n_%s -> %s_" %(from_,to)
            text += "\n - %s : *%.4g%%*" % (coin,gain_perc)

    if text == "":
        text = default_msg
    #print(text)
    return text

"""
Parse a send command
/send_from 1 ETH 
"""
def parse_send_message(text):
    tokens = text.split(" ")
    assert tokens[0].startswith("/")
    tokens.pop(0)

    assert (2 == len(tokens))
    amount = float(tokens[0])
    assert (amount >= 0)
    currency = tokens[1].upper()
    return (amount,currency) 


import unittest
class TestFormatting(unittest.TestCase):
    def test_empty(self): 
        self.assertLess(0,len(text_of_arbs([])))

    def test_some(self):
        text = text_of_arbs([{
            "from" : "Coinbase",
            "to"   : "Coindelta",
            "coin" : "ETH",
            "gain_perc" : 100.
        }])
        self.assertLess(0,len(text))

class TestParse(unittest.TestCase):
    def test_empty(self):
        self.assertRaises(AssertionError,parse_send_message,"")

    def test_bad_start(self):
        self.assertRaises(AssertionError,parse_send_message,"1 ETH")

    def test_bad_format_misplaced_amount(self):
        self.assertRaises(ValueError,parse_send_message,"/send_from ETH 1")

    def test_bad_format_bad_amount(self):
        self.assertRaises(AssertionError,parse_send_message,"/send_from -1 ETH")

    def test_correct_format(self):
        self.assertEqual((1,"ETH"),parse_send_message("/send_from 1 ETH"))
        self.assertEqual((1,"ETH"),parse_send_message("/send_from 1 eth"))
        self.assertEqual((1.2,"ETH"),parse_send_message("/send_from 1.2 ETH"))

