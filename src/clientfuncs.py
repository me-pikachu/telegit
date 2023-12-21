from telethon.tl.patched import Message
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import sys

entity = 'telegit'
APP_API_ID = 28521183
APP_API_HASH = "e139c4dca684be89f42e609b929f5fad"
phone =  '+917732895355'
client = TelegramClient(entity, APP_API_ID, APP_API_HASH)
async def connect(client):
    await client.connect()

async def sender(path: str, caption, botname = 'Telegit_bot', chatid = -1002023399035):
    msg = await client.send_file(chatid, path, caption=str(caption))
    return msg

def totele(filepath, caption, client=client):
    with client:
        msg = client.loop.run_until_complete(sender(filepath, caption))
    #print(type(msg.media))
    return msg.id

async def fromtele(msg_id, file_path, filename:str, client=client, chatid = -1002023399035):
    async for message in client.iter_messages(chatid):
        if (message.id==msg_id):
            total_size = message.media.document.size
            dl=0
            with open(f'{file_path}\\{filename}', 'wb') as handle:
                async for chunk in client.iter_download(message.media, chunk_size=int(total_size/10)):
                    dl += len(chunk)
                    handle.write(chunk)
                    done = int(50 * dl / total_size)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()
            break
            #await message.download_media(file=f'E:\\telegit\\{filename}')
            #break
        else:
            print(message.id)
    print(f"downloaded {file_path}\{filename} !!")

#msg_id = totele("E:/telegit/lauda2.txt", "changedname.txt")
#print(msg_id)
#with client:
#    stat = client.loop.run_until_complete(fromtele(msg_id, "E:\\telegit", "lauda69.txt"))
#    print('saved')
