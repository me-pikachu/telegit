from telethon.tl.patched import Message
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
import sys
import time
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

def totele(filepath, caption: str = "", client=client):
    with client:
        msg = client.loop.run_until_complete(sender(filepath, caption))
    #print(type(msg.media))
    return msg.id

async def fromtele(msg_id: int, file_path:str, client=client, chatid = chatid):
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
            with open(file_path, 'wb') as handle:
                t1 = time.time()
                async for chunk in client.iter_download(message.media, chunk_size=chunk_size):
                    dl += len(chunk)
                    handle.write(chunk)
                    t2=time.time()
                    download_speed = (dl/(t2-t1))/1000
                    eta = int((total_size-dl)/download_speed)/1000
                    done = int(50 * dl / total_size)
                    sys.stdout.write(f"\r|%s%s|" % ('█' * done, ' ' * (50-done)))

                    if (download_speed < 1.0):
                        # speed is less than 1 kbps
                        download_speed = round(download_speed*1024, 2)
                        if (eta < 60):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} bytes persec, eta : {eta}s]")
                        elif (eta < 3600):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} bytes persec, eta : {time.strftime('%M:%S', time.gmtime(eta))}]")
                        else:
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} bytes persec, eta : {time.strftime('%H:%M:%S', time.gmtime(eta))}]")
                    elif (download_speed < 1024):
                        # speed between 1 kbps to 1 mbps
                        download_speed = round(download_speed, 2)
                        if (eta < 60):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} KBps, eta : {eta}s]")
                        elif (eta < 3600):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} KBps, eta : {time.strftime('%M:%S', time.gmtime(eta))}]")
                        else:
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} KBps, eta : {time.strftime('%H:%M:%S', time.gmtime(eta))}]")
                    elif (download_speed < 1024 * 1024):
                        # speed between 1mbps to 1gbps
                        download_speed = round(download_speed/1024, 2)
                        if (eta < 60):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} MBps, eta : {eta}s]")
                        elif (eta < 3600):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} MBps, eta : {time.strftime('%M:%S', time.gmtime(eta))}]")
                        else:
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} MBps, eta : {time.strftime('%H:%M:%S', time.gmtime(eta))}]")
                    else:
                        # speed greater than equal to 1gbps
                        download_speed = round(download_speed/(1024*1024), 2)
                        if (eta < 60):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} MBps, eta : {eta}s]")
                        elif (eta < 3600):
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} MBps, eta : {time.strftime('%M:%S', time.gmtime(eta))}]")
                        else:
                            sys.stdout.write(f" {round((dl/total_size * 100), 2)}%  in {int(t2-t1)}s  [{download_speed} MBps, eta : {time.strftime('%H:%M:%S', time.gmtime(eta))}]")
                    sys.stdout.flush()
            break
            #await message.download_media(file=f'E:\\telegit\\{filename}')
            #break
        else:
            print(message.id)
    print(f"File '{file_path}' downloaded successfully!!")

#msg_id = totele("E:/telegit/zero.new", "changedname.txt")
#print(msg_id)
#with client:
#    stat = client.loop.run_until_complete(fromtele(95,"E:\\telegit\\newzero.new"))
#    print('saved')
