import file_handler
import telegit_handler

max_fsize = 50*1024*1024 # 50MB in bytes

def update_cache(folder: str):
    return file_handler.getcache(folder)

def push_file(file_path: str, git: dict, file_cache: dict, max_fsize: int):
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
                print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for gdrive upload")
                # uploading the file for gdrive

                # creating .telegit file for the current file

                # pushing the .telegit file
                
            else:
                print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                # pushing the current file
                telegit_handler.to_git(path = file_path, folder = file_handler.getfolder(file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file {file_path} is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i == "y"):
                if (cursize > max_fsize):
                    print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for gdrive upload")
                    # uploading the file for gdrive

                    # creating .telegit file for the current file

                    # pushing the .telegit file

                else:
                    print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                    # pushing the current file                
                    telegit_handler.to_git(path = file_path, folder = file_handler.getfolder(file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])
    else:
        if (mtime == file_cache["mtime"]):
            # size is different but modification time is different
            # this case can be complicated as in if push is required or not
            print(f"Warning: Size is different but Modification time is the same for the file {file_path}")
            if (cursize > max_fsize):
                print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for gdrive upload")
                # uploading the file for gdrive

                # creating .telegit file for the current file

                # pushing the .telegit file

            else:
                print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                # pushing the current file
                telegit_handler.to_git(path = file_path, folder = file_handler.getfolder(file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        elif (mtime > file_cache["mtime"]):
            # size and modification time are different in the file
            print(f"Size and Modification time are different for the file {file_path}")
            if (cursize > max_fsize):
                print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for gdrive upload")
                # uploading the file for gdrive

                # creating .telegit file for the current file

                # pushing the .telegit file

            else:
                print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                # pushing the current file
                telegit_handler.to_git(path = file_path, folder = file_handler.getfolder(file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

        else:
            # the file has been modified before what have been stored in the cache
            cache_mtime = file_cache["mtime"]
            print(f"Error: The Modification time of the file {file_path} is {mtime} but that stored in the cache is {cache_mtime}")
            print("Would you like to force push anyway (y/n)?")
            i = str(input())
            if (i == "y"):
                if (cursize > max_fsize):
                    print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for gdrive upload")
                    # uploading the file for gdrive

                    # creating .telegit file for the current file

                    # pushing the .telegit file

                else:
                    print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
                    # pushing the current file 
                    telegit_handler.to_git(path = file_path, folder = file_handler.getfolder(file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])               
        

def force_push_file(file_path: str, git: dict, max_fsize: int):
    print(f"Forcefully pushing the file '{file_path}'")
    cursize = file_handler.getsize(file_path)
    if (cursize > max_fsize):
        print(f"The size of the '{file_path}' is greater than {max_fsize/(1024*1024)}MB. Preparing file for gdrive upload")
        # uploading the file for gdrive

        # creating .telegit file for the current file

        # pushing the .telegit file

    else:
        print(f"The size of the '{file_path}' is less than or equal to {max_fsize/(1024*1024)}MB. Preparing file for git push")
        # pushing the current file
        telegit_handler.to_git(path = file_path, folder = file_handler.getfolder(file_path), filename = file_handler.getfilename(file_path), gitoken = git["gitoken"], repo = git["repo"], desc = git["desc"])

                    

def push(folder: str):
    cache = update_cache(folder)
    # using DFS approach to push the folders
    # Continue till there are not any folders left
    if (len(cache) == 0):
        # cache is empty
        # forcefully push each file
        print("Cannot locate the cache file. Forcefully pushing everyfile")

    else:
        print("")


def __init__():
    print("Welcome to telegit!")