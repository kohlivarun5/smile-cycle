def group_arbs_by_direction(arbs_in):
    arbs = sorted(arbs_in,key = lambda x:x["gain_perc"],reverse=True)
    #print(arbs)
    ## Collect by direction first
    direction_dict = {}
    for idx, arb in enumerate(arbs):
        from_,to = arb["from"].title(),arb["to"].title()
        direction = "_%s -> %s_" %(from_,to)
        if direction not in direction_dict:
            direction_dict[direction] = []
        direction_dict[direction].append(arb)
    return direction_dict

def texts_of_arbs(direction_dict):
    texts = []
    for direction, arbs in direction_dict.iteritems():
        text = ""
        for idx, arb in enumerate(arbs):
            from_,to,coin,gain_perc = arb["from"].title(),arb["to"].title(),arb["coin"],arb["gain_perc"]
            if idx == 0:
                text += "\n_%s -> %s_" %(from_,to)
            text += "\n - %s : *%.4g%%*" % (coin,gain_perc)
        texts.append(text)
    
    return texts

def text_of_arbs(arbs_in, default_msg="No arbitrage found!"):
    direction_dict = group_arbs_by_direction(arbs_in)
    texts = texts_of_arbs(direction_dict)
    text = ""
    for s in texts:
        text += s

    if text == "":
        text = default_msg
    #print(text)
    return text

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
