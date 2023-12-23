import file_handler
import clientfuncs
from clientfuncs import client
import os

max_fsize = 50*1024*1024 # 50MB in bytes

def update_cache(folder: str):
    return file_handler.getcache(folder)

def upcache_dir(startdir: str, curdir: str, cache: dict):
    # get into the subdirectories first
    # this functions returns the updates cache dictionary

    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        cache = upcache_dir(startdir, dir, cache)
    
    # now updates all the files in the current directory
    subfiles = file_handler.getfiles(curdir)
    for files in subfiles:
        fdetails = {}
        fdetails["fsize"] = file_handler.getsize(files)
        fdetails["mtime"] = file_handler.getmtime(files)
        fdetails["ctime"] = file_handler.getctime(files)
        cache[f"{file_handler.get_gitfolder(startdir, files)}\\{file_handler.getfilename(files)}"] = fdetails
    
    return cache

def upcache(startdir):
    # this function updates the cache content and write into the .telegit folder
    # same approach as that of push function (DFS)

    print("Updating the cache file")
    cache = upcache_dir(startdir, startdir, {})

    # save this cache into the file
    file_handler.writecache(startdir, cache)
    print("Cache file successfully updated")

def push_update(startdir: str, file_path: str, file_cache: dict):
    # file_cache is the data from the .telegit folder
    
    git_path = file_handler.get_gitloc(startdir, file_path)

    print(f"Checking for any valid push for the file '.{git_path}'")

    cursize = file_handler.getsize(file_path)
    mtime = file_handler.getmtime(file_path)

    if (cursize == file_cache["fsize"]):
        # as file size is the same file need not to be pushed but further checking modification time
        if (mtime == file_cache["mtime"]):
            # modification time is also the same no need for any push
            print(f"Cannot find any relevant push data for the file '.{git_path}'")
            return
        elif (mtime > file_cache["mtime"]):
            # size same but still there is modification in the file
            print(f"Size is same but Modification time is different for the file")
            # uploading the file for Telegram
            file_id = clientfuncs.totele(file_path)

            # creating .telegit file for the current file
            filename = file_handler.to_telegit(file_path)
            ftelegit = open(filename, "w+")
            # firstline is the filename and second line is the file_id
            ftelegit.write(file_handler.getfilename(file_path))
            ftelegit.write("\n")
            ftelegit.write(str(file_id))
            ftelegit.close()

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file '.{git_path}' is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i.lower() == "y"):
                    # uploading the file for Telegram
                    file_id = clientfuncs.totele(file_path)

                    # creating .telegit file for the current file
                    filename = file_handler.to_telegit(file_path)
                    ftelegit = open(filename, "w+")
                    # firstline is the filename and second line is the file_id
                    ftelegit.write(file_handler.getfilename(file_path))
                    ftelegit.write("\n")
                    ftelegit.write(str(file_id))
                    ftelegit.close()
            else:
                print("Cancelling the push of the current file")
                return
    else:
        if (mtime == file_cache["mtime"]):
            # size is different but modification time is different
            # this case can be complicated as in if push is required or not
            print(f"Warning: Size is different but Modification time is the same for the file")
            # uploading the file for Telegram
            file_id = clientfuncs.totele(file_path)

            # creating .telegit file for the current file
            filename = file_handler.to_telegit(file_path)
            ftelegit = open(filename, "w+")
            # firstline is the filename and second line is the file_id
            ftelegit.write(file_handler.getfilename(file_path))
            ftelegit.write("\n")
            ftelegit.write(str(file_id))
            ftelegit.close()

        elif (mtime > file_cache["mtime"]):
            # size and modification time are different in the file
            print(f"Both Size and Modification time are different for the file")
            # uploading the file for Telegram
            file_id = clientfuncs.totele(file_path)

            # creating .telegit file for the current file
            filename = file_handler.to_telegit(file_path)
            ftelegit = open(filename, "w+")
            # firstline is the filename and second line is the file_id
            ftelegit.write(file_handler.getfilename(file_path))
            ftelegit.write("\n")
            ftelegit.write(str(file_id))
            ftelegit.close()
        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file '.{git_path}' is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i == "y"):
                file_id = clientfuncs.totele(file_path)

                # creating .telegit file for the current file
                filename = file_handler.to_telegit(file_path)
                ftelegit = open(filename, "w+")
                # firstline is the filename and second line is the file_id
                ftelegit.write(file_handler.getfilename(file_path))
                ftelegit.write("\n")
                ftelegit.write(str(file_id))
                ftelegit.close()
            else:
                print("Cancelling the push of the current file")
            return



def push_dir(startdir: str, curdir: str, cache: dict, igdir: list, curfilenum: int, totfilenum: int):
    global max_fsize
    # igdir are the directories to be ignored and igfiles are the files to be ignored
    global max_fsize
    # since it is a DFS firstly go to the subdirectories of current directory
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        if (file_handler.foldername(dir) in igdir):
            pass
        else:
            curfilenum = push_dir(startdir, dir, cache, igdir, curfilenum, totfilenum)
    
    subfiles = file_handler.getfiles(curdir)
    for file_path in subfiles:
        curfilenum += 1
        print(f"File: ({curfilenum}/{totfilenum})")
        print(f"Checking file '.{file_handler.get_gitloc(startdir, file_path)}'")
        cursize = file_handler.getsize(file_path)
        if (cursize > max_fsize):
            print(f"The size of the file is greater than {max_fsize/(1024*1024)}MB\nPreparing file for Telegram upload")
            if (file_path in cache):
                push_update(startdir, file_path, cache[file_path])
            else:
                # uploading the file for Telegram
                file_id = clientfuncs.totele(file_path)

                # creating .telegit file for the current file
                filename = file_handler.to_telegit(file_path)
                ftelegit = open(filename, "w+")
                # firstline is the filename and second line is the file_id
                ftelegit.write(file_handler.getfilename(file_path))
                ftelegit.write("\n")
                ftelegit.write(str(file_id))
                ftelegit.close()

            # open the gitignore and add this file in the gitignore
            loc = file_handler.get_gitloc(startdir, file_path)
            loc = loc.replace("\\","/")
            fgitig = open(f"{startdir}\\.gitignore","a+")

            fopen = open(f"{startdir}\\.gitignore", "r+")
            excfile = []
            for file in fopen.readlines():
                excfile.append(file.replace("\n","")) 
            fopen.close()

            if (loc not in excfile):
                fgitig.write(f"\n{loc}")
            fgitig.close()

            print("\nThe .telegit file was successfully created")
        else:
            print(f"The size of the file is less than {max_fsize/(1024*1024)}MB")

    return curfilenum

def push(startdir: str, igdir: list = []):
    totfilenum = file_handler.totalfiles(startdir, startdir, igdir)
    print(f"Found a total of {totfilenum} files")
    print(f"A total of {file_handler.totalfiles_less_fmaxsize(startdir, max_fsize, startdir, igdir)} files have size less than {max_fsize/(1024*1024)}MB")
    cache = update_cache(startdir)
    # using DFS approach to push the folders
    # Continue till there are not any folders left
    if (len(cache) == 0):
        # cache is empty
        # forcefully push each file
        print("Cannot locate the cache file. Forcefully pushing everyfile")
    else:
        print("Cache file located. Pushing all the modifications")

    # using DFS approach to push the folders
    # Continue till there are not any folders left
    push_dir(startdir, startdir, cache, igdir, 0, totfilenum)
    upcache(startdir)
    print("All the files are successfully converted")


def pull_dir(startdir: str, curdir: str, totfilenum: int, curfilenum: int):
    # same approach as that of push function (DFS)
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        curfilenum = pull_dir(startdir, dir, totfilenum, curfilenum)
    
    subfiles = file_handler.getfiles(curdir)
    for files in subfiles:
        curfilenum += 1
        print(f"File: ({curfilenum}/{totfilenum})")
        print(f"Checking file '.{file_handler.get_gitloc(startdir, files)}'")
        if (file_handler.getfilext(files) == "telegit"):
            # we need to read the file and download it's data
            print("The file is a '.telegit' file")
            print("Downloading the original file from Telegram")
            text = file_handler.read(files)
            lines = text.split("\n")
            # lines[0] is the file name
            # lines[1] is the msg.id
            # lines[2] is the version of the file
            file_path = file_handler.change_basename(files, lines[0])
            with client:
                client.loop.run_until_complete(clientfuncs.fromtele(int(lines[1]), file_path))
            print("File successfully downloaded")
        else:
            print("The file is not a '.telegit' file")
    return curfilenum

def pull(startdir: str):
    # the files pulled may have ext .telegit
    # we need to download that files and replace them with the original files

    # now using the DFS approach visiting every file
    totfilenum = file_handler.totalfiles(startdir)
    print(f"Found a total of {totfilenum} files")
    pull_dir(startdir, startdir, totfilenum, 0)
    upcache(startdir)
    print("All the files are successfully converted")

print("Welcome to telegit!")
while (True):
    print("No folder is open. Please enter a directory to open")
    startdir = str(input())
    startdir = file_handler.formatdir(startdir)
    if (os.path.isdir(startdir)):       

        print("Telegit is now ready for git push pull")
        while(True):
            print("For Push to git write 'push'. For Pull from git write 'pull'. To get of the working directory write 'close'")
            cmd = str(input())
            if ("push" in cmd):
                push(startdir, ["Binaries", "Intermediate", "Saved"])
            elif (cmd == "pull"):
                pull(startdir)
            elif (cmd == "close"):
                print("Getting out of the directory")
                break
            else:
                print("Not a valid command")
    else:
        print("Please enter a correct working directory")


