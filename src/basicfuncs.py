from github import Github
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

# togit("E:/telegit/basicfuncs.py", 'src', 'basicfuncs.py', '<YOUR TOKEN>', 'me-pikachu/telegit', 'initial')
