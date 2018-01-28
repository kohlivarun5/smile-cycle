from telegram.ext import Updater, CommandHandler


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

import calculate_arb
def arb(bot, update):
    arbs = calculate_arb.coinbase_coindelta()
    text = ""
    for idx, arb in enumerate(arbs):
        if idx == 0:
            text += "_%s -> %s_" %(arb["from"],arb["to"])
        text+=("\n - %s : *%.3g%%*" % (arb["coin"],arb["gain_perc"]))

    update.message.reply_text(text,parse_mode="Markdown")


updater = Updater('475606384:AAEmrgc65Cj9FogJNvH8D6LeSNSbB0B0pSU')

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('arb', arb))

updater.start_polling()
updater.idle()
