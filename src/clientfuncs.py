
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes

entity = 'telegit'
APP_API_ID = 28521183
APP_API_HASH = "e139c4dca684be89f42e609b929f5fad"
phone =  '+917732895355'
client = TelegramClient(entity, APP_API_ID, APP_API_HASH)

#async def connect(client=client):
#    await client.connect()
#    if not client.is_user_authorized():
 #       client.sign_in(phone, input('Enter code: '))
#connect()

#client.start(); 
async def totele(path: str, filename: str, botname = 'Telegit_bot', chatid = -1002023399035):
    msg = await client.send_file(chatid, path)
    return msg.media.document.id
with client:
    id = client.loop.run_until_complete(totele("E:/telegit/zero.new", "blabla"))

async def fromtele(id, chatid = -1002023399035):
    await client.download_media(id)
#with client:
#    client.loop.run_until_complete(fromtele(id))
#print(id)

