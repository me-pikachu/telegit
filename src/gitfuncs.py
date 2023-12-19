from github import Github
import os

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

togit("E:/telegit/gitfuncs.py", 'src', 'gitfuncs.py', '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', 'me-pikachu/telegit', 'added fromgit')

def fromgit(repo: str, path_to_clone_to: str, gitoken: str):
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
            with open(path_to_save_to, 'wb') as file:
                file.write(file_content.decoded_content)

# fromgit('me-pikachu/telegit', 'E:/test clone2/', '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')
    