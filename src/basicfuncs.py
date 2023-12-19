from github import Github
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

def togit(path: str, folder, filename: str, gitoken: str, repo: str, desc: str):
    app = Github(gitoken)

    repo = app.get_repo(repo)

    with open(path, mode='r') as file:
        data = file.read()

    contents = repo.get_contents("")
    total_files=[]
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            total_files.append(file_content.path)

    if folder != None:
        if f'{folder}/{filename}' in total_files:
            file_contents = repo.get_contents(f'{folder}/{filename}', ref="main")
            repo.update_file(file_contents.path, desc, data, file_contents.sha, branch='main')
        else:
            repo.create_file(f'{folder}/{filename}', desc, data, branch='main')
    else:
        if filename in total_files:
            file_contents = repo.get_contents(f'{filename}', ref="main")
            repo.update_file(file_contents.path, desc, data, file_contents.sha, branch='main')
        else:
            repo.create_file(f'{filename}', desc, data, branch='main')
    print(f'pushed {filename} successfully!!')

togit("E:/gitdrive/basicfuncs.py", 'src', 'basicfuncs.py', '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', 'me-pikachu/gitdrive', 'updated todrive')

def todrive(path: str, filename: str, folderid):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()        
    drive = GoogleDrive(gauth) 

    if folderid != None:
        f = drive.CreateFile({
            "title":filename,
            "parents":[
                {
                    "id":folderid
                }
            ]
        })
    else:
        f=drive.CreateFile({
            "title":filename
        })
    f.SetContentFile(path)
    f.Upload()
    f=None

    print(f"Uploaded {filename} to drive Successfully")

# todrive("E:/gitdrive/testpush.txt", "testpush", None)
# put client_secrets.json in same dir as basicfuncs.py 