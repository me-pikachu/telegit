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
    
    
def read(file_path: str):
    # reads the text out a file and if FILE DOES NOT EXISTS returns a empty string
    if (os.path.exists(file_path)):
        file = open(file_path, "r")
        data = file.read()
        file.close()
        return data
    else:
        return ""
    
def read_gitcred(startdir: str):
    # reads gitcred.file and returns a dictionary
    if (os.path.exists(f"{startdir}\\.telegit\\gitcred.file")):
        file = open(f"{startdir}\\.telegit\\gitcred.file", "r")
        data = (file.read()).split("\n")
        file.close()
        git = {}
        git["repo"] = data[0]
        git["gitoken"] = data[1]
        git["desc"] = ""
    else:
        git = {}
        git["repo"] = ""
        git["gitoken"] = ""
        git["desc"] = ""
    return git


def writecache(startdir: str, cache: dict):
    # it saves the data into cache file using pickle
    cache_path = startdir + "\\.telegit\\cache.pkl"
    if (os.path.exists(cache_path)):
        fcache = open(cache_path, "wb") # wb because the file is in binary format not string
        pickle.dump(cache, fcache)
        fcache.close()
    else:
        # create the directory first
        if (not os.path.isdir(startdir + "\\" + ".telegit")):
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

def getfilename_rmext(file_path: str):
    # gets the file name without ext from the file path
    fname = os.path.basename(file_path)
    return (fname.split("."))[0]

def getfilext(file_path: str):
    # returns the file extension
    filename = getfilename(file_path).split(".")
    if (len(filename) == 1):
        return "" # there is no extension
    return filename[1]

def get_gitfolder(startdir: str, file_path: str):
    # return the corresponding the git folder location from the file_path
    dir = os.path.dirname(file_path)
    dir = dir.replace(startdir,"")
    if (dir != ""): # if this condition is not checked then dir[0] may give errors
        if (dir[0] == '\\' or dir[0] == '/'):
            dir = dir[1:] # remove the first character of the string
            if (dir == ""):
                return ""
    else:
        return ""
    return dir

def foldername(dir: str):
    ls = dir.split("\\")
    return ls[len(ls)-1]

def get_gitloc(startdir: str, file_path: str):
    # gets the git location of a file
    # i.e. removes the start directory from the complete path
    return f"{get_gitfolder(startdir, file_path)}\\{getfilename(file_path)}"

def to_telegit(file_path: str):
    # changes extension of a file to telegit
    return f"{getfolder(file_path)}\\{getfilename_rmext(file_path)}.telegit"

def change_ext(file_path: str, new_ext: str):
    # changes the extension of a file to new_ext
    return f"{getfolder(file_path)}\\{getfilename_rmext(file_path)}.{new_ext}"

def change_basename(file_path: str, basename: str):
    # changes the basename in the file_path
    return f"{getfolder(file_path)}\\{basename}"

def formatdir(dir: str):
    dir = dir.replace("/","\\")
    if (dir[len(dir)-1] == '\\'):
        dir = dir[:-1]
    return dir

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

def totalfiles(startdir: str, curdir: str = "", igdir: list = [], count: int = 0):
    # counts the total number of files in a particular directory
    if (curdir == ""):
        curdir = startdir
    
    subdir = getsubdir(curdir)
    for dir in subdir:
        if (foldername(dir) in igdir):
            pass
        else:
            count = totalfiles(startdir, dir, igdir, count)
    
    subfiles = getfiles(curdir)
    count += len(subfiles)
    return count
    
def totalfiles_less_fmaxsize(startdir: str, fmaxsize: int, curdir: str = "", igdir: list = [], count: int = 0):
    # counts the total number of files in a particular directory
    if (curdir == ""):
        curdir = startdir
    
    subdir = getsubdir(curdir)
    for dir in subdir:
        if (foldername(dir) in igdir):
            pass
        else:
            count = totalfiles_less_fmaxsize(startdir, fmaxsize, dir, igdir, count)
    
    subfiles = getfiles(curdir)
    for files in subfiles:
        if (getsize(files) < fmaxsize):
            count += 1
    return count

def comploc(path1: str, path2: str, startdir: str = ""):
    # compare two location (path2 can be a git location)
    path1 = path1.replace("/","\\")
    path2 = path2.replace("/","\\")
    if (startdir == ""):
        return (path1 == path2)
    else:
        # replace all / with \\
        startdir = startdir.replace("/","\\")
        # path2 can or cannot be complete path
        return (path1 == path2 or path1 == (startdir+path2))

        





