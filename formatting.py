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

if __name__ == "__main__":
    import calculate_arb
    print(text_of_arbs([]))
    print(text_of_arbs(calculate_arb.coinbase_coindelta()))
    print(text_of_arbs(calculate_arb.binance_kucoin()))
