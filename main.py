import StringIO
import json
import logging
import random
import urllib
import urllib2

# for sending images
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

import credentials
BASE_URL = 'https://api.telegram.org/bot' + credentials.TELEGRAM_TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))



import calculate_arb,formatting,trade
def hello(fr):
    return "Hello %s!\nID:%s" % (fr.get("first_name"),fr.get('id'))

def handle_send_from(exchange,text):
    (amount,currency) = formatting.parse_send_message(text)
    if exchange == "coinbase":
        return trade.send_coinbase_coindelta(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET,amount,currency)
    else:
        raise UserWarning("Unknown exchange: %s" % exchange)

def get_transaction(id):
    from exchanges import coinbase_api
    client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
    transaction = coinbase_api.tx(client,id)
    return transaction

def get_tx_info(text,reply_to_text):
    if reply_to_text is None:
        return "Reply to a transaction message to get it's info!"
    from exchanges import coinbase_api
    # First parse to find transaction id 
    id = trade.parse_coinbase_transaction_id(reply_to_text)
    tx = get_transaction(id)
    return trade.coinbase_transaction_info(tx)

def replyToTelegram(msg,chat_id,message_id):
    resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
        'chat_id': str(chat_id),
        'text': msg.encode('utf-8'),
        'parse_mode' : 'Markdown',
        'disable_web_page_preview': 'true',
        'reply_to_message_id': str(message_id),
    }), timeout = 30).read()
    logging.info('send response:')
    logging.info(resp)

def enqueueTxTask(tx,chat_id,message_id,max_count=30,count=0,countdown=60):
    if tx.network.status == "confirmed" and tx.network.confirmations > 10 and count > 0:
        return

    if count > max_count:
        return

    from google.appengine.ext import deferred
    deferred.defer(get_tx_info_task, tx.id,chat_id,message_id,max_count,count,countdown,_countdown=countdown)

def get_tx_info_task(tx_id,chat_id,message_id,max_count,count,countdown):
    if count >= max_count:
        logging.log("Reached max count for task")
        return 

    transaction = get_transaction(tx_id)
    if transaction:
        msg = trade.coinbase_transaction_info(transaction)
        replyToTelegram(msg,chat_id,message_id)
        enqueueTxTask(transaction,chat_id,message_id,max_count,count=count+1,countdown=countdown)


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        try:
            message = body['message']
        except:
            message = body['edited_message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        reply_to_text = None 
        reply_to_message = message.get("reply_to_message")
        if reply_to_message:
            reply_to_text = reply_to_message.get("text")

        if not text:
            logging.info('no text')
            return

        def reply(msg):
            return replyToTelegram(msg,chat_id,message_id)

        try:
            if text.startswith('/'):
                if text == '/start':
                    reply('Bot enabled')
                    setEnabled(chat_id, True)
                elif text == '/stop':
                    reply('Bot disabled')
                    setEnabled(chat_id, False)
                elif text.startswith('/hello'):
                    reply(hello(fr))
                elif text.startswith('/arb'):
                    reply(formatting.text_of_arbs(calculate_arb.coinbase_coindelta()))
                    reply(formatting.text_of_arbs(calculate_arb.binance_kucoin()))
                elif text.startswith('/send_from_coinbase'):
                    if credentials.ID_VARUN_KOHLI == fr.get('id'):
                        tx = handle_send_from("coinbase",text)
                        tx_text = trade.coinbase_transaction_info(tx)
                        reply(tx_text)
                        enqueueTxTask(tx,chat_id,message_id)
                    else:
                        reply("You are not allowed to initiate send from coinbase")
                elif text.startswith('/coinbase_balance'):
                    reply(trade.get_coinbase_balance(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET))
                elif text.startswith('/tx_info'):
                    reply(get_tx_info(text,reply_to_text))
                elif text.startswith('/enqueueTxTask'):
                    tx = get_transaction(text.split(' ')[1])
                    enqueueTxTask(tx,chat_id,message_id,max_count=3,countdown=5)
                else:
                    reply('What command?')

            # CUSTOMIZE FROM HERE
            elif 'who are you' in text:
                reply('telebot starter kit, created by yukuku: https://github.com/yukuku/telebot')
            elif 'what time' in text:
                reply('look at the corner of your screen!')
            else:
                if getEnabled(chat_id):
                    reply('I got your message! (but I do not know how to answer)')
                else:
                    logging.info('not enabled for chat_id {}'.format(chat_id))

        except UserWarning as e:
            #print e
            reply(str(e))
        except Exception as e:
            logging.exception(e,exc_info=True)
            reply("Unknown error!")
        except:
            logging.error("Unknown error")
            reply("Unknown error!")
 
app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
