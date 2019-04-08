#!/usr/local/bin/python3
import json
import shutil
import time
import subprocess
import os
from src import (import_or_install, parseArgs, readConfig, 
    removeCredentials, submodule, createRepository, commitChanges,
    createLocalRepository, addRemote, Emojis, TextColor, SourceChangedError)

def main():
    # Get the packages necessary
    import_or_install('requests', textColor, emoji)
    # Parse the arguments, get whats missing
    user, configFile = parseArgs(textColor)
    # Get config and create elements
    folderConfig = readConfig(configFile)
    # Init host repository
    shutil.rmtree('.git')
    url = createRepository('Test0', 'Everything related to my studies', user.token, auto_init=False)
    createLocalRepository()
    addRemote(url)
    for folder in folderConfig['folders']:
        parseFolder(folder, "", user)
    
    # Lets do some cleanups, move assets around
    try:
        moveResources(user)
        shutil.copyfile('resources/README', 'README.md')
        os.remove('.gitignore')
        shutil.copyfile('resources/gitignore', '.gitignore')
        shutil.rmtree('resources')
        shutil.rmtree('src')
        os.remove('script.py')
        os.remove(configFile)
    except:
        raise SourceChangedError
    commitChanges('.', 'Test0', user, 'Set up my entire folder structure!')

def moveResources(user):
    reponame = 'IFI-resources'
    createRepository(reponame, 'Resources used for my stay at IFI-UiT', user.token)
    submodule("", reponame, user)
    shutil.copytree('resources/report_templates', reponame+'/report_templates')
    commitChanges(reponame+'/', reponame, user, 'Initial repo commit')


def parseFolder(folder, path, user):
    # Create repository
    createRepository(folder['name'], folder['description'], user.token)
    print(path+folder['name'])
    # Initialize it as a submodule in the right place
    submodule(path, folder['name'], user)
    # Iterate through the sub-folders, and repeat the process
    if 'folders' in folder:
        for child in folder['folders']:
            parseFolder(child, path+folder['name']+"/", user)
        # Remove all credentials
        if path != '':
            commitChanges(path+folder['name']+"/", folder['name'], user, 'Init submodules.')
        else:
            commitChanges(folder['name'], folder['name'], user, 'Init submodules')

if __name__ == "__main__":
    emoji = Emojis()
    textColor = TextColor()
    try:
        main()
    except Exception as error:
        print(error)
