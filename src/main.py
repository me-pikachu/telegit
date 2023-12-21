import file_handler
import gitfuncs
import clientfuncs
import os

currentdir = os.path.dirname(os.path.abspath(__file__))

max_fsize = 50*1024*1024 # 50MB in bytes

def update_cache(folder: str):
    return file_handler.getcache(folder)

def push_file(startdir: str, file_path: str, git: dict, file_cache: dict, max_fsize: int):
    # file_cache is the data from the .telegit folder
    # git_data contains all the relevant info about github push
    
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

                # pushing the .telegit file
                print("Preparing the .telegit file for git push")
                ftelegit = file_handler.to_telegit(file_path)
                gitfuncs.togit(path = ftelegit, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_rmext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

            else:
                print(f"The size of the file is less than {max_fsize/(1024*1024)}MB\nPreparing file for git push")
                # pushing the current file
                gitfuncs.togit(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file {file_path} is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i.lower() == "y"):
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

                    # pushing the .telegit file
                    print("Preparing the .telegit file for git push")
                    ftelegit = file_handler.to_telegit(file_path)
                    gitfuncs.togit(path = ftelegit, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_rmext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

                else:
                    print(f"The size of the file is less than {max_fsize/(1024*1024)}MB\nPreparing file for git push")
                    # pushing the current file
                    gitfuncs.togit(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
            else:
                print("Cancelling the push of the current file")
                return
    else:
        if (mtime == file_cache["mtime"]):
            # size is different but modification time is different
            # this case can be complicated as in if push is required or not
            print(f"Warning: Size is different but Modification time is the same for the file")
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

                # pushing the .telegit file
                print("Preparing the .telegit file for git push")
                ftelegit = file_handler.to_telegit(file_path)
                gitfuncs.togit(path = ftelegit, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_rmext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

            else:
                print(f"The size of the file is less than {max_fsize/(1024*1024)}MB\nPreparing file for git push")
                # pushing the current file
                gitfuncs.togit(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        elif (mtime > file_cache["mtime"]):
            # size and modification time are different in the file
            print(f"Both Size and Modification time are different for the file")
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

                # pushing the .telegit file
                print("Preparing the .telegit file for git push")
                ftelegit = file_handler.to_telegit(file_path)
                gitfuncs.togit(path = ftelegit, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_rmext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

            else:
                print(f"The size of the file is less than {max_fsize/(1024*1024)}MB\nPreparing file for git push")
                # pushing the current file
                gitfuncs.togit(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file {file_path} is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i == "y"):
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

                    # pushing the .telegit file
                    print("Preparing the .telegit file for git push")
                    ftelegit = file_handler.to_telegit(file_path)
                    gitfuncs.togit(path = ftelegit, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_rmext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

                else:
                    print(f"The size of the file is less than {max_fsize/(1024*1024)}MB\nPreparing file for git push")
                    # pushing the current file
                    gitfuncs.togit(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
            
            else:
                print("Cancelling the push of the current file")
            return

    print(f"Successfull pushing of the file '.{git_path}'")


def force_push_file(startdir: str, file_path: str, git: dict, max_fsize: int):
    git_path = file_handler.get_gitloc(startdir, file_path)

    print(f"Forcefully pushing the file '.{git_path}'")

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

        # pushing the .telegit file
        print("Preparing the .telegit file for git push")
        ftelegit = file_handler.to_telegit(file_path)
        gitfuncs.togit(path = ftelegit, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_rmext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])


    else:
        print(f"The size of the file is less than {max_fsize/(1024*1024)}MB\nPreparing file for git push")
        # pushing the current file
        gitfuncs.togit(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

    print(f"Successfull pushing of the file '.{git_path}'")

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

def upgitcred(startdir, git: dict):
    print("Updating gitcred.file")
    fpull = open(f"{startdir}\\.telegit\\gitcred.file","w+")
    fpull.write(git["repo"])
    fpull.write("\n")
    fpull.write(git["gitoken"])
    fpull.close()
    print("gitcred.file successfully updated")

'''
def push_dir(startdir: str, git: dict, cache: dict, curdir: str, gitignore: dict, force_push: bool, curfilenum: int, totfilenum: int):
    # igdir are the directories to be ignored and igfiles are the files to be ignored
    global max_fsize
    # since it is a DFS firstly go to the subdirectories of current directory
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        if (dir not in gitignore["dir"]):
            curfilenum = push_dir(startdir, git, cache, dir, force_push, curfilenum, totfilenum)
    
    subfiles = file_handler.getfiles(curdir)
    for files in subfiles:
        curfilenum += 1
        print(f"File: ({curfilenum}/{totfilenum})")
        if ((file_handler.getfilename(files) == gitignore["filename"]) or file_handler.comploc(files,gitignore)):
            print(f"The file was found in .gitignore. Ignoring the file {file_handler.get_gitloc(startdir, files)}")
        else:
            if (len(cache)!=0 and file_handler.get_gitloc(startdir, files) in cache):
                file_cache = cache[file_handler.get_gitloc(startdir, files)]
                if (force_push):
                    force_push_file(startdir, files, git, max_fsize)
                else:
                    push_file(startdir, files, git, file_cache, max_fsize)
            else:
                # force push the file as it is not in cache
                print(f"No previous data available for the file {file_handler.get_gitloc(startdir, files)}")
                force_push_file(startdir, files, git, max_fsize)
            
    return curfilenum
'''

def push_dir(startdir: str, git: dict, cache: dict, curdir: str, force_push: bool, curfilenum: int, totfilenum: int):
    # igdir are the directories to be ignored and igfiles are the files to be ignored
    global max_fsize
    # since it is a DFS firstly go to the subdirectories of current directory
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        curfilenum = push_dir(startdir, git, cache, dir, force_push, curfilenum, totfilenum)
    
    subfiles = file_handler.getfiles(curdir)
    for files in subfiles:
        curfilenum += 1
        print(f"File: ({curfilenum}/{totfilenum})")
        if (len(cache)!=0 and file_handler.get_gitloc(startdir, files) in cache):
            file_cache = cache[file_handler.get_gitloc(startdir, files)]
            if (force_push):
                force_push_file(startdir, files, git, max_fsize)
            else:
                push_file(startdir, files, git, file_cache, max_fsize)
        else:
            # force push the file as it is not in cache
            print(f"No previous data available for the file {file_handler.get_gitloc(startdir, files)}")
            force_push_file(startdir, files, git, max_fsize)
            
    return curfilenum

def push(startdir: str, git: dict):
    totfilenum = file_handler.totalfiles(startdir)
    print(f"Found a total of {totfilenum} files")
    cache = update_cache(startdir)
    # using DFS approach to push the folders
    # Continue till there are not any folders left
    if (len(cache) == 0):
        # cache is empty
        # forcefully push each file
        print("Cannot locate the cache file. Forcefully pushing everyfile")
        push_dir(startdir, git, cache, startdir, True, 0, totfilenum)
    else:
        print("Cache file located. Pushing all the modifications")
        push_dir(startdir, git, cache, startdir, False, 0, totfilenum)
    upcache(startdir)
    print("All the files are successfully pushed to github")

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
            file_path = file_handler.change_basename(files, lines[0])
            clientfuncs.fromtele(int(lines[1]), file_path)
            print("File successfully downloaded")
        else:
            print("The file is not a '.telegit' file")
    return curfilenum

def pull(startdir: str, git: dict):
    # firstly making the normal github pull requests
    # the files pulled may have ext .telegit
    # we need to download that files and replace them with the original files
    repo = git["repo"]
    if (repo == ""):
        print("Either the gitcred.file is corrupted or does not exist")
    else:
        # making pull request from github
        print(f"Pulling from the git repository '{repo}'")
        gitfuncs.fromgit(repo, path_to_clone_to = startdir, gitoken = git["gitoken"])
        print("Pulled from github successfullly")
        # now using the DFS approach visiting every file
        totfilenum = file_handler.totalfiles(startdir)
        print(f"Found a total of {totfilenum} files")
        pull_dir(startdir, startdir, totfilenum, 0)
        upcache(startdir)
        upgitcred(startdir, git)
        print("All the files are successfully pulled from github")


print("Welcome to telegit!")
while (True):
    print("No folder is open. Please enter a directory to open")
    startdir = str(input())
    startdir = file_handler.formatdir(startdir)
    if (os.path.isdir(startdir)):
        git = file_handler.read_gitcred(startdir)
        if (git["repo"]==""):
            print("No git credentials found!")
            print("Enter Github repository: ")
            repo = str(input())
            git["repo"] = repo
            print("Enter Github token: ")
            gitoken = str(input())
            git["gitoken"] = gitoken
            os.mkdir(f"{startdir}\\.telegit")
            upgitcred(startdir, git)
            print("Git credentials updated!")
        print("Telegit is now ready for git push pull")
        while(True):
            print("For Push to git write 'push desc'. For Pull from git write 'pull'. To get of the working directory write 'close'")
            cmd = str(input())
            if ("push" in cmd):
                git["desc"] = cmd.replace("push","").strip()
                push(startdir, git)
            elif (cmd == "pull"):
                pull(startdir, git)
            elif (cmd == "close"):
                print("Getting out of the directory")
                break
            else:
                print("Not a valid command")
    else:
        print("Please enter a correct working directory")


