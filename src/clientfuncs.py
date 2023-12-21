from telethon.tl.patched import Message
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import sys
import time
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
            #print(total_size)
            dl=0
            chunk_size = int(total_size/100)
            if chunk_size>32000:
                chunk_size = int(chunk_size/10)
            if chunk_size<1:
                chunk_size=1
            with open(f'{file_path}\\{filename}', 'wb') as handle:
                t1 = time.time()
                async for chunk in client.iter_download(message.media, chunk_size=chunk_size):
                    dl += len(chunk)
                    handle.write(chunk)
                    t2=time.time()
                    download_speed = (dl/(t2-t1))/1000
                    eta = int((total_size-dl)/download_speed)
                    download_speed = round(download_speed, 2)
                    done = int(50 * dl / total_size)
                    sys.stdout.write(f"\r|%s%s|" % ('█' * done, ' ' * (50-done)) )
                    sys.stdout.write(f" {round((dl/total_size * 100), 2)} %  in {int(t2-t1)}s  [{download_speed} Kbps, eta : {eta}s]")
                    sys.stdout.flush()
            break
            #await message.download_media(file=f'E:\\telegit\\{filename}')
            #break
        else:
            print(message.id)
    print(f"downloaded {file_path}\{filename} !!")

#msg_id = totele("E:/telegit/zero.new", "changedname.txt")
#print(msg_id)
#with client:
 #   stat = client.loop.run_until_complete(fromtele(95, "E:\\telegit", "newzero.new"))
#    print('saved')
