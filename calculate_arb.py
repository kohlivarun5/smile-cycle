"""
Each function returns the results in  a dict containing:
    { 
        "from" : "From Exchange",
        "to"   : "To Exchange",
        "gain_perc" : "Gain in %",
        "coin"  : "Base coin"
    }
"""

def coinbase_coindelta():
    return [
        {"from" : "Coinbase","to":"Coindelta","coin" : "LTC", "gain_perc" : 11.39},
        {"from" : "Coinbase","to":"Coindelta","coin" : "ETH", "gain_perc" : 10.53}
    ]
