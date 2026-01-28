from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "8249024452:AAGY662l3RWlogT06RHLlDq5viTKm-gBLhM"

def debug(update, context):
    print("chat_id:", update.message.chat_id)

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text, debug))

updater.start_polling()
updater.idle()
