from google.appengine.ext import ndb

class CoinbaseCoindeltaTransaction(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    chat_id = ndb.IntegerProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    tx_id = ndb.StringProperty(required=True)
    buyer_id = ndb.IntegerProperty(required=True)
    seller_id = ndb.IntegerProperty()
    cost_in_usd = ndb.FloatProperty(required=True)
    forex_rate_inr_in_usd = ndb.FloatProperty(required=True)
    inr_settlement = ndb.FloatProperty()
    fees_to_buy_in_usd = ndb.FloatProperty()
