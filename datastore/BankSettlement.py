from google.appengine.ext import ndb

class BankSettlement(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    chat_id = ndb.IntegerProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    sender_id = ndb.IntegerProperty(required=True)
    amount_usd = ndb.FloatProperty(required=True)
    amount_inr = ndb.FloatProperty(required=True)
