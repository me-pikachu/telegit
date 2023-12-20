from telethon.tl.patched import Message
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import pickle

entity = 'telegit'
APP_API_ID = 28521183
APP_API_HASH = "e139c4dca684be89f42e609b929f5fad"
phone =  '+917732895355'
client = TelegramClient(entity, APP_API_ID, APP_API_HASH)
async def connect(client):
    await client.connect()

async def sender(path: str, filename: str, botname = 'Telegit_bot', chatid = -1002023399035):
    msg = await client.send_file(chatid, path, file_name=filename)
    return msg

def totele(filepath, filename, client=client):
    with client:
        msg = client.loop.run_until_complete(sender(filepath, filename))
        
    return msg.id

async def fromtele(msg_id, filename:str, client=client, chatid = -1002023399035):
    async for message in client.iter_messages(chatid):
        if (message.id==msg_id):
            await message.download_media(file=f'E:\\telegit\\{filename}')
            break
        else:
            print(message.id)

#msg_id = totele("E:/telegit/lauda.txt", "lauda.txt")
#print(msg_id)
#with client:
#    stat = client.loop.run_until_complete(fromtele(msg_id, "lauda3.txt"))
#    print('saved')
