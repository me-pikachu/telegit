from github import Github
import os
import file_handler

def togit(path: str, folder: str, filename: str, gitoken: str, repo: str, desc: str):
    if (folder.strip() == ""):
        folder = None

    path = path.replace("\\", "/") # git does not treat blackslash as subdirectories
    if (folder is not None):
        folder = folder.replace("\\", "/") # git does not treat blackslash as subdirectories
    
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

    if (folder != None):
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
    print(f"File '{filename}' pushed successfully!!")
    app.close()

# togit("E:/telegit/chatids.txt", 'src/Data', 'chatids.txt', '<YOUR TOKEN>', 'me-pikachu/telegit', 'chatids')

def fromgit(repo: str, path_to_clone_to: str, gitoken: str):
    path_to_clone_to = path_to_clone_to.replace("\\","/") # changing windows file separtor to github file separtor
    path_to_clone_to = f"{path_to_clone_to}/" # adding a / at the end

    app = Github(gitoken)
    repo = app.get_repo(repo)
    contents = repo.get_contents("")
    #to_be_saved=[]
    while contents:
        file_content = contents.pop(0)
        current_path = path_to_clone_to
        if file_content.type == "dir":
            current_path += file_content.path
            
            contents.extend(repo.get_contents(file_content.path))
        else:
            #print(file_content)
            path_to_save_to = path_to_clone_to+file_content.path
            #print(path_to_save_to)
            if (os.path.exists(file_handler.getfolder(path_to_save_to))):
                with open(path_to_save_to, 'wb') as file:
                    file.write(file_content.decoded_content)
            else:
                # create the directory first
                os.mkdir(file_handler.getfolder(path_to_save_to))
                with open(path_to_save_to, 'wb') as file:
                    file.write(file_content.decoded_content)

    app.close()

def delete(repo: str, file: str, desc: str, gitoken: str):
    app = Github(gitoken)
    repo = app.get_repo(repo)
    contents = repo.get_contents(file, ref='main')
    commit_status = repo.delete_file(contents.path, desc, contents.sha, branch='main')
    print(f'Deleted {repo}/{file} successfully!!')
    return commit_status

#commit_status = delete('me-pikachu/telegit', 'test/lauda69.txt', 'test deletion', '<YOUR TOKEN>')
#print(commit_status)
# fromgit('me-pikachu/telegit', 'E:/test clone2/', '<YOUR TOKEN>')
    
