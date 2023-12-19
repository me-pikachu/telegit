import os
from datetime import datetime
import pickle # to read and write the cache data

def getmtime(file_path: str):
    # fetch the modification time of the file
    fstat = os.stat(file_path)
    modtime = fstat.st_mtime
    return datetime.fromtimestamp(modtime)

def getctime(file_path: str):
    # fetch the creation time of the file
    fstat = os.stat(file_path)
    cretime = fstat.st_ctime
    return datetime.fromtimestamp(cretime)

def getsize(file_path: str):
    # it returns the size of the file in bytes
    fstat = os.stat(file_path)
    return fstat.st_size

def getcache(startdir: str):
    # it reads from the cache file if any using pickle
    cache_path = startdir + "\\.telegit\\cache.pkl"
    if (os.path.exists(cache_path)):
        fcache = open(cache_path, "rb")
        cache = pickle.load(fcache)
        fcache.close()
        return cache
    else:
        return {}

def writecache(startdir: str, cache: dict):
    # it saves the data into cache file using pickle
    cache_path = startdir + "\\.telegit\\cache.pkl"
    if (os.path.exists(cache_path)):
        fcache = open(cache_path, "wb") # wb because the file is in binary format not string
        pickle.dump(cache, fcache)
        fcache.close()
    else:
        # create the directory first
        os.mkdir(startdir + "\\" + ".telegit")
        fcache = open(cache_path, "wb") # wb because the file is in binary format not string
        pickle.dump(cache, fcache)
        fcache.close()

def getfolder(file_path: str):
    # get the folder or the directory name from the file path
    return os.path.dirname(file_path)

def getfilename(file_path: str):
    # gets the file name with ext from the file path
    return os.path.basename(file_path)

def getfilename_withoutext(file_path: str):
    # gets the file name without ext from the file path
    fname = os.path.basename(file_path)
    return (fname.split("."))[0]

def getfilext(file_path: str):
    filename = getfilename(file_path)
    return filename.split(".")[1]

def get_gitfolder(startdir: str, file_path: str):
    dir = os.path.dirname(file_path)
    dir.replace(startdir,"")
    if (dir != ""): # if this condition is not checked then dir[0] may give errors
        if (dir[0] == '\\' or dir[0] == '/'):
            dir = dir[1:] # remove the first character of the string
            if (dir == ""):
                return None
    else:
        return None
    return dir

def get_gitloc(startdir: str, file_path: str):
    return f"{get_gitfolder(startdir, file_path)}\\{getfilename(file_path)}"

def getsubdir(curdir: str):
    # using scandir
    dir = []
    files = os.scandir(curdir)
    for f in files:
        if (f.is_dir()): # initially it was f.is_dir and was True even for file also
            # we also need to ignore .telegit and .git folders
            if (f.name != ".telegit" and f.name != ".git"):
                dir.append(f.path) # f.path is the complete path
    return dir

def getfiles(curdir: str):
    # using scandir
    files = []
    freader = os.scandir(curdir)
    for f in freader:
        if (f.is_file()):
            files.append(f.path)
    return files

def totalfiles(startdir: str, curdir: str = None, count: int = 0):
    if (curdir == None):
        curdir = startdir
    
    subdir = getsubdir(curdir)
    for dir in subdir:
        count = totalfiles(startdir, dir, count)
    
    subfiles = getfiles(curdir)
    count += len(subfiles)
    return count





