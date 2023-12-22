import file_handler
import clientfuncs
from clientfuncs import client
import os

max_fsize = 50*1024*1024 # 50MB in bytes

def push_dir(startdir: str, curdir: str, curfilenum: int, totfilenum: int):
    global max_fsize
    # igdir are the directories to be ignored and igfiles are the files to be ignored
    global max_fsize
    # since it is a DFS firstly go to the subdirectories of current directory
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        curfilenum = push_dir(startdir, dir, curfilenum, totfilenum)
    
    subfiles = file_handler.getfiles(curdir)
    for file_path in subfiles:
        curfilenum += 1
        print(f"File: ({curfilenum}/{totfilenum})")
        print(f"Checking file '.{file_handler.get_gitloc(startdir, file_path)}'")
        cursize = file_handler.getsize(file_path)
        if (cursize > max_fsize):
            print(f"The size of the file is greater than {max_fsize/(1024*1024)}MB\nPreparing file for Telegram upload")
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

def push(startdir: str):
    totfilenum = file_handler.totalfiles(startdir)
    print(f"Found a total of {totfilenum} files")
    # using DFS approach to push the folders
    # Continue till there are not any folders left
    push_dir(startdir, startdir, 0, totfilenum)
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
                push(startdir)
            elif (cmd == "pull"):
                pull(startdir)
            elif (cmd == "close"):
                print("Getting out of the directory")
                break
            else:
                print("Not a valid command")
    else:
        print("Please enter a correct working directory")


