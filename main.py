import StringIO
import json
import logging
import random
import urllib
import urllib2

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
def hello(fr,chat_id):
    return "Hello %s!\nID:%s\nChatID:%s" % (fr.get("first_name"),fr.get('id'),chat_id)

def handle_send_from(from_exch,to_exch,text):
    (amount,currency) = formatting.parse_send_message(text)
    if from_exch == "coinbase" and to_exch == "coindelta":
        return trade.send_coinbase_coindelta(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET,amount,currency)
    elif from_exch == "coinbase" and to_exch == "koinex":
        return trade.send_coinbase_koinex(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET,amount,currency)
    else:
        raise UserWarning("Unknown send for %s -> %s" % (from_exch,to_exch))

def get_transaction(id):
    from exchanges import coinbase_api
    client = coinbase_api.client(credentials.COINBASE_API_KEY,credentials.COINBASE_API_SECRET)
    transaction = coinbase_api.tx(client,id)
    return transaction

def get_tx_info(text,reply_to_text):
    if reply_to_text is None:
        return "Reply to a transaction message to get it's info!"
    id = trade.parse_coinbase_transaction_id(reply_to_text)
    tx = get_transaction(id)
    return trade.coinbase_transaction_info(tx)

def save_tx(reply_to_text,chat_id,buyer_id):
    if reply_to_text is None:
        return "Reply to a transaction message to get it's info!"
    tx_id = trade.parse_coinbase_transaction_id(reply_to_text)
    tx = get_transaction(tx_id)
    return trade.save_tx(tx,chat_id,buyer_id)

def update_tx(reply_to_text,inr_settlement=None,seller_id=None,fees_to_buy_in_usd=None):
    if reply_to_text is None:
        return "Reply to a transaction message to get it's info!"
    tx_id = trade.parse_coinbase_transaction_id(reply_to_text)
    return trade.update_tx(tx_id,
                           inr_settlement=inr_settlement,
                           seller_id=seller_id,
                           fees_to_buy_in_usd=fees_to_buy_in_usd)

def replyToTelegram(msg,chat_id,message_id=None):
    resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
        'chat_id': str(chat_id),
        'text': msg.encode('utf-8'),
        'parse_mode' : 'Markdown',
        'disable_web_page_preview': 'true',
        'reply_to_message_id': str(message_id) if message_id else message_id,
    }), timeout = 30).read()
    logging.info('send response:')
    logging.info(resp)

def enqueueTxTask(tx,chat_id,message_id,target_confirmations=None,max_count=60,count=0,countdown=120):
    if target_confirmations is None:
        target_confirmations = 10

    if tx.network.status == "confirmed" and tx.network.confirmations >= target_confirmations and count > 0:
        return

    if count > max_count:
        return

    from google.appengine.ext import deferred
    deferred.defer(get_tx_info_task, tx.id,chat_id,message_id,max_count,count,countdown,target_confirmations,_countdown=countdown)

def get_tx_info_task(tx_id,chat_id,message_id,max_count,count,countdown,target_confirmations):
    if count >= max_count:
        logging.info("Reached max count for task")
        replyToTelegram("Reached max count for task. Request status manually now!",chat_id,message_id)
        return 

    transaction = get_transaction(tx_id)
    if transaction:
        msg = trade.coinbase_transaction_info(transaction)
        replyToTelegram(msg,chat_id,message_id)
        enqueueTxTask(transaction,chat_id,message_id,max_count,count=count+1,countdown=countdown,target_confirmations=target_confirmations)


SUBSCRIPTION_CHAT_IDS = [
    #529093774, # Mine
    -308873143, #Pallav and Rahul
    #-255808834, #Rahul and Me
]
class NotifyArbHandler(webapp2.RequestHandler):
    def get(self):
        texts = [formatting.text_of_arbs(calculate_arb.coinbase_coindelta()),
                 formatting.text_of_arbs(calculate_arb.coinbase_koinex())]
        for text in texts:
            for chat_id in SUBSCRIPTION_CHAT_IDS:
                replyToTelegram(text,chat_id)

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

                # Info
                elif text.startswith('/hello'):
                    reply(hello(fr,chat_id))

                # Arb commands
                elif text.startswith('/arb_koinex'):
                    reply(formatting.text_of_arbs(calculate_arb.coinbase_koinex()))
                elif text.startswith('/arb_crypto'):
                    reply(formatting.text_of_arbs(calculate_arb.binance_kucoin()))
                elif text.startswith('/arb'):
                    reply(formatting.text_of_arbs(calculate_arb.coinbase_coindelta()))

                # Trade commands
                # Balance
                elif text.startswith('/coinbase_balance'):
                    reply(trade.get_coinbase_balance(
                            credentials.COINBASE_API_KEY,
                            credentials.COINBASE_API_SECRET))

                # Initiate trade
                elif text.startswith('/send_coinbase_to_coindelta'):
                    if credentials.ID_VARUN_KOHLI == fr.get('id'):
                        tx,target_confirmations = handle_send_from("coinbase","coindelta",text)
                        tx_text = trade.coinbase_transaction_info(tx)
                        reply(tx_text)
                        enqueueTxTask(tx,chat_id,message_id,target_confirmations=target_confirmations)
                        trade.save_tx(tx,chat_id,fr.get('id'))
                    else:
                        reply("You are not allowed to initiate send from coinbase")

                elif text.startswith('/send_coinbase_to_koinex'):
                    if credentials.ID_VARUN_KOHLI == fr.get('id'):
                        tx,target_confirmations = handle_send_from("coinbase","koinex",text)
                        tx_text = trade.coinbase_transaction_info(tx)
                        reply(tx_text)
                        enqueueTxTask(tx,chat_id,message_id,target_confirmations=target_confirmations)
                        trade.save_tx(tx,chat_id,fr.get('id'))
                    else:
                        reply("You are not allowed to initiate send from coinbase")

                # Transaction info
                elif text.startswith('/tx_info'):
                    reply(get_tx_info(text,reply_to_text))

                # Record extra fees 
                elif text.startswith('/tx_extra_fees'):
                    text = update_tx(
                                reply_to_text,
                                fees_to_buy_in_usd=float(text.split(' ')[1]))
                    reply(text)

                # Settled in INR
                elif text.startswith('/tx_sold_inr'):
                    text = update_tx(
                                reply_to_text,
                                seller_id=fr.get('id'),
                                inr_settlement=float(text.split(' ')[1]))
                    reply(text)

                # Settled in INR
                elif text.startswith('/sent_to_chase'):
                    text = trade.save_bank_settlement(
                                    chat_id,fr.get('id'),
                                    float(text.split(' ')[1]))
                    reply(text)


                # Helper TX save
                elif text.startswith('/tx_save'):
                    reply(save_tx(reply_to_text,chat_id,fr.get('id')))

                # History
                elif text.startswith('/history'):
                    (total_cost_usd,
                     total_profit_per_person_usd,
                     text) = trade.tx_list_summary(chat_id)
                    reply(text)

                    (total_amount_usd,text) = trade.bank_settlement_summary(chat_id)
                    reply(text)

                    text = trade.summary_of_history(
                                    total_cost_usd,
                                    total_profit_per_person_usd,
                                    total_amount_usd)
                    reply(text)

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
    ('/notify_arb', NotifyArbHandler),
], debug=True)
