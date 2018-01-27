#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger import Bot,Element

import calculate_arb

# https://developers.facebook.com/apps/159034348214729/messenger/settings/
app = Flask(__name__)
ACCESS_TOKEN = 'EAACQpBHVGckBAFstCjzTLaKMAaMxqtvP6m2L5o1yw3YKI7Jv6AH3ti7KfhZBfWmqDny7ovZAqqVKRbVWEvqkezjbyjTsQeN5mHMH4ZBoQStA5Hr4Qnhfps7AIvQIUxRf5EZCZCBogM5vTws8GUd348CfwNes3nOHBzENvtNdHwQZDZD'
VERIFY_TOKEN = 'xeuz0uIE'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          print(event)
          messaging = event['messaging']
          for message in messaging:
            recipient_id = message['sender']['id']
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    handle_response(bot.send_text_message(recipient_id, response_sent_text))
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    handle_response(bot.send_text_message(recipient_id, response_sent_nontext))
            elif message.get('postback'):
                if message['postback'].get('payload'):
                    payload = message['postback']['payload']
                    
                    if payload == "Coinbase-Coindelta":
                        arbs = calculate_arb.coinbase_coindelta()
                        #msg = arbs_to_message(arbs)
                        msg = arbs_to_list_message(arbs)
                        #print(msg)
                        handle_response(bot.send_message(recipient_id,msg))
                    else:
                        handle_response(bot.send_text_message(recipient_id, ("%s not supported yet!" % payload)))

    return "Message Processed"

#def arbs_to_message(arbs):
#    elements = []
#    for arb in arbs:
#        from_,to,coin,gain_perc = arb 
#        subtitle = "%d %% @ %s -> %s" % (gain_perc, from_,to)
#        share_btn = [ 
#            {
#                "type": "element_share",
#                "share_contents": { 
#                    "attachment": {
#                        "type": "template",
#                        "payload": {
#                            "template_type": "generic",
#                            "elements": [
#                                Element(title=("Want to trade %s ?" % coin),subtitle=subtitle)
#                            ]
#                        }
#                    }
#                }
#            }
#        ]
#        element = Element(title=coin, subtitle=subtitle)#,buttons=share_btn)
#        elements.append(element)
#    return elements

def arbs_to_list_message(arbs):
    elements = []
    for arb in arbs:
        from_,to,coin,gain_perc = arb["from"],arb["to"],arb["coin"],arb["gain_perc"]
        subtitle = "%d %% @ %s -> %s" % (gain_perc, from_,to)
        elements.append(Element(title=coin,subtitle=subtitle))

    message = {
        "attachment" : {
            "type" : "template",
            "payload" : { 
                "template_type": "list",
                "top_element_style": "compact",
                "elements": elements
            }
        }
    }
    return message


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def handle_response(res):
    if res.get('error'):
        print(res)

#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

if __name__ == "__main__":
    app.run()
