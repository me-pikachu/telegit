from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import telegram
TOKEN = "6713242583:AAFEEy1jEhOyax8440-yMAF7owu5ClAXLVI"

updater = Updater(TOKEN, use_context = True)
bot = telegram.Bot(token = TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("connection established!!")

    
def totele(path, bot=bot):
    ids = open("E:/telegit/chatids.ids", 'r')
    l=ids.readlines()
    ids.close()
    chat_id = int(l[0])
    document = open(path, 'rb')
    bot.send_document(chat_id, document)

def extractid(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    ids = open("E:/telegit/chatids.ids", 'w+')
    ids.write(str(chat_id))
    ids.close()
    update.message.reply_text("extraction successfull!!")

#totele("E:/telegit/chatids.ids")
#updater.dispatcher.add_handler(CommandHandler('start', start))
#updater.dispatcher.add_handler(CommandHandler('extractme', extractid))
#updater.start_polling()
#updater.idle()



