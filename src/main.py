import file_handler
import telegit_handler

max_fsize = 50*1024*1024 # 50MB in bytes

def update_cache(folder: str):
    return file_handler.getcache(folder)

def push_file(startdir: str, file_path: str, git: dict, file_cache: dict, max_fsize: int):
    # file_cache is the data from the .telegit folder
    # git_data contains all the relevant info about github push
    print(f"Checking for any valid push in '{file_path}'")
    cursize = file_handler.getsize(file_path)
    mtime = file_handler.getmtime(file_path)
    if (cursize == file_cache["fsize"]):
        # as file size is the same file need not to be pushed but further checking modification time
        if (mtime == file_cache["mtime"]):
            # modification time is also the same no need for any push
            print(f"Cannot find any relevant push data for the file '{file_path}'")
        elif (mtime > file_cache["mtime"]):
            # size same but still there is modification in the file
            print(f"Size is same but Modification time is different for the file {file_path}")
            if (cursize > max_fsize):
                print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for Telegram upload")
                # uploading the file for Telegram

                # creating .telegit file for the current file
                ftelegit = open(f"{file_handler.getfolder(file_path)}\\{file_handler.getfilename_withoutext(file_path)}.telegit", "w+")
                ftelegit.write("...links chatid...")
                ftelegit.close()
                # pushing the .telegit file
                telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_withoutext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
            else:
                print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                # pushing the current file
                telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file {file_path} is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i == "y"):
                if (cursize > max_fsize):
                    print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for Telegram upload")
                    # uploading the file for Telegram

                    # creating .telegit file for the current file
                    ftelegit = open(f"{file_handler.getfolder(file_path)}\\{file_handler.getfilename_withoutext(file_path)}.telegit", "w+")
                    ftelegit.write("...links chatid...")
                    ftelegit.close()
                    # pushing the .telegit file
                    telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_withoutext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
                else:
                    print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                    # pushing the current file                
                    telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
    else:
        if (mtime == file_cache["mtime"]):
            # size is different but modification time is different
            # this case can be complicated as in if push is required or not
            print(f"Warning: Size is different but Modification time is the same for the file {file_path}")
            if (cursize > max_fsize):
                print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for Telegram upload")
                # uploading the file for Telegram

                # creating .telegit file for the current file
                ftelegit = open(f"{file_handler.getfolder(file_path)}\\{file_handler.getfilename_withoutext(file_path)}.telegit", "w+")
                ftelegit.write("...links chatid...")
                ftelegit.close()
                # pushing the .telegit file
                telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_withoutext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
            else:
                print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                # pushing the current file
                telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        elif (mtime > file_cache["mtime"]):
            # size and modification time are different in the file
            print(f"Size and Modification time are different for the file {file_path}")
            if (cursize > max_fsize):
                print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for Telegram upload")
                # uploading the file for Telegram

                # creating .telegit file for the current file
                ftelegit = open(f"{file_handler.getfolder(file_path)}\\{file_handler.getfilename_withoutext(file_path)}.telegit", "w+")
                ftelegit.write("...links chatid...")
                ftelegit.close()
                # pushing the .telegit file
                telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_withoutext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
            else:
                print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                # pushing the current file
                telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file {file_path} is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i == "y"):
                if (cursize > max_fsize):
                    print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for Telegram upload")
                    # uploading the file for Telegram

                    # creating .telegit file for the current file
                    ftelegit = open(f"{file_handler.getfolder(file_path)}\\{file_handler.getfilename_withoutext(file_path)}.telegit", "w+")
                    ftelegit.write("...links chatid...")
                    ftelegit.close()
                    # pushing the .telegit file
                    telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_withoutext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
                else:
                    print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                    # pushing the current file 
                    telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])               
        

def force_push_file(startdir: str, file_path: str, git: dict, max_fsize: int):
    print(f"Forcefully pushing the file '{file_path}'")
    cursize = file_handler.getsize(file_path)
    if (cursize > max_fsize):
        print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for Telegram upload")
        # uploading the file for Telegram

        # creating .telegit file for the current file
        ftelegit = open(f"{file_handler.getfolder(file_path)}\\{file_handler.getfilename_withoutext(file_path)}.telegit", "w+")
        ftelegit.write("...links chatid...")
        ftelegit.close()
        # pushing the .telegit file
        telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = f"{file_handler.getfilename_withoutext(file_path)}.telegit", gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
    else:
        print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
        # pushing the current file
        telegit_handler.to_git(path = file_path, folder = file_handler.get_gitfolder(startdir, file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

def ucache_dir(startdir: str, curdir: str, cache: dict):
    # get into the subdirectories first
    # this functions returns the updates cache dictionary

    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        cache = ucache_dir(startdir, dir, cache)
    
    # now updates all the files in the current directory
    subfiles = file_handler.getfiles(curdir)
    for files in subfiles:
        fdetails = {}
        fdetails["fsize"] = file_handler.getsize(files)
        fdetails["mtime"] = file_handler.getmtime(files)
        fdetails["ctime"] = file_handler.getctime(files)
        cache[f"{file_handler.get_gitfolder(startdir, files)}\\{file_handler.getfilename(files)}"] = fdetails
    
    return cache

def ucache(startdir):
    # this function updates the cache content and write into the .telegit folder
    # same approach as that of push function (DFS)
    cache = ucache_dir(startdir, startdir, {})

    # save this cache into the file
    file_handler.writecache(startdir, cache)

def push_dir(startdir: str, git: dict, cache: dict, curdir: str, force_push: bool):
    global max_fsize
    # since it is a DFS firstly go to the subdirectories of current directory
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        push_dir(startdir, git, cache, dir, force_push)
    
    subfiles = file_handler.getfiles(curdir)
    for files in subfiles:
        if (len(cache)!=0 and f"{file_handler.get_gitfolder(startdir, files)}\\{file_handler.getfilename(files)}" in cache):
            file_cache = cache[f"{file_handler.get_gitfolder(startdir, files)}\\{file_handler.getfilename(files)}"]
            if (force_push):
                force_push_file(startdir, files, git, max_fsize)
            else:
                push_file(startdir, files, git, file_cache, max_fsize)
        else:
            # force push the file as it is not in cache
            force_push_file(startdir, files, git, max_fsize)

def push(startdir: str, git: dict):
    cache = update_cache(startdir)
    # using DFS approach to push the folders
    # Continue till there are not any folders left
    if (len(cache) == 0):
        # cache is empty
        # forcefully push each file
        print("Cannot locate the cache file. Forcefully pushing everyfile")
        push_dir(startdir, git, cache, startdir, True)
    else:
        print("Cache file located. Pushing all the modifications")
        push_dir(startdir, git, cache, startdir, False)
    ucache(startdir)

def pull_dir(startdir: str, curdir: str):
    # same approach as that of push function (DFS)
    subdir = file_handler.getsubdir(curdir)
    for dir in subdir:
        pull_dir(startdir, dir)
    
    subfiles = file_handler.getfiels(curdir)
    for files in subfiles:
        if (file_handler.getfilext(files) == "telegit"):
            # we need to read the file and download it's data
            print("Downloading....")

def pull(startdir: str):
    # firstly making the normal github pull requests
    # the files pulled may have ext .telegit
    # we need to download that files and replace them with the original files

    # making pull request from github


    # now using the DFS approach visiting every file
    pull_dir(startdir, startdir)

print("Welcome to telegit!")
'''
git = {}
push("test_dir",git)
'''