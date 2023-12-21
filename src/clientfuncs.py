from telethon.tl.patched import Message
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import pickle
import os


currentdir = os.path.dirname(os.path.abspath(__file__))
# reading the telegram.file for API details
file = open(f"{currentdir}\\Data\\telegram.file","r")
data = file.read().split("\n")

entity = data[0]
botname = data[1]
chatid = int(data[2])
APP_API_ID = int(data[3])
APP_API_HASH = data[4]
phone =  data[5]

client = TelegramClient(entity, APP_API_ID, APP_API_HASH)
async def connect(client):
    await client.connect()

async def sender(path: str, caption: str = "", botname = botname, chatid = chatid):
    msg = await client.send_file(chatid, path, caption=str(caption))
    return msg

def totele(filepath: str, caption: str = "", client=client):
    with client:
        msg = client.loop.run_until_complete(sender(filepath, caption))
        
    return msg.id

async def fromtele(msg_id, file_path: str, client=client, chatid = chatid):
    async for message in client.iter_messages(chatid):
        if (message.id==msg_id):
            await message.download_media(file=f"{file_path}")
            break
        else:
            print(message.id)

#msg_id = totele("E:/telegit/test.txt", "changedname.txt")
#print(msg_id)
#with client:
#    stat = client.loop.run_until_complete(fromtele(msg_id, "lauda3.txt"))
#    print('saved')
