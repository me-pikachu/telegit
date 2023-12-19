from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
import telegram
import requests
import json

TOKEN = "6713242583:AAFEEy1jEhOyax8440-yMAF7owu5ClAXLVI"

updater = Updater(TOKEN, use_context = True)
bot = telegram.Bot(token = TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("connection established!!")

    
def totele(path, bot=bot, TOKEN=TOKEN):
    ids = open("Data/chatids.ids", 'r')
    l=ids.readlines()
    ids.close()
    chat_id = int(l[0])
    document = open(path, "rb")
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    response = requests.post(url, data={'chat_id': chat_id}, files={'document': document})
    content = response.content.decode("utf8")
    js = json.loads(content)
    print("Upload to telegram is successfull")
    return js['result']['document']['file_id']

    

def fromtele(id: str, topath: str, filename: str, bot=bot):
    file = bot.getFile(id)
    if (topath!=None):
        file.download(topath+filename)
    else:
        file.download(filename)
    print("Download from the telegram is successfull")


def extractid(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    ids = open("Data/chatids.ids", 'w+')
    ids.write(str(chat_id))
    ids.close()
    update.message.reply_text("extraction successfull!!")

# file_id = totele("Data/chatids.ids")
# fromtele(file_id, "E:/", "chatids.txt")

#updater.dispatcher.add_handler(CommandHandler('start', start))
#updater.dispatcher.add_handler(CommandHandler('extractme', extractid))
#updater.start_polling()
#updater.idle()



