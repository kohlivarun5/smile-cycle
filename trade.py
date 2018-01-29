from exchanges import coinbase,coindelta
def send_coinbase_coindelta(COINBASE_API_KEY,COINBASE_API_SECRET,amount,currency):
    cb_client = coinbase.client(COINBASE_API_KEY,COINBASE_API_SECRET)
    coinbase.send(client,coindelta.ADDRESSES["currency"],amount,currency)
