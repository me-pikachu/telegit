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

def getcache(folder: str):
    # it reads from the cache file if any using pickle
    cache_path = folder + "\.telegit\cache.pkl"
    fcache = open(cache_path, "rb")
    cache = pickle.load(fcache)
    fcache.close()
    return cache

def writecache(folder: str, cache: dict):
    # it saves the data into cache file using pickle
    cache_path = folder + "\.telegit\cache.pkl"
    fcache = open(cache_path, "wb")
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

def getsubdir(curdir: str):
    # using scandir
    dir = []
    files = os.scandir(curdir)
    for f in files:
        if (f.is_dir):
            dir.append(f.path) # f.path is the complete path
    return dir

def getfiles(curdir: str):
    # using scandir
    files = []
    freader = os.scandir(curdir)
    for f in freader:
        if (f.is_file):
            files.append(f.path)
    return files



