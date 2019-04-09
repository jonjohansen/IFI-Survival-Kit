#!/usr/local/bin/python3
import json
import shutil
import time
import subprocess
import os
from src import import_or_install, parseArgs, readConfig, createRepository,\
     createLocalRepository, addRemote, SourceChangedError, commitChanges, \
         createRepository, submodule, printBlue, printYellow, Emojis

def main():
    # Get the packages necessary
    import_or_install('requests')
    user, configFile = parseArgs()
    folderConfig = readConfig(configFile)

    printBlue("\nRead ", end='')
    printYellow(configFile, end='')
    printBlue(' and proceeding to create repositories' + Emojis.pan)
    # Transform host repository
    shutil.rmtree('.git')
    url = createRepository('UiT', 'Everything related to my studies', user, auto_init=False)
    createLocalRepository()
    addRemote(url)
    for folder in folderConfig['folders']:
        parseFolder(folder, "", user)
    
    # Cleaning up, and moving resources to their places
    try:
        moveResources(user)
        shutil.copyfile('resources/README', 'README.md')
        shutil.copyfile('resources/gitignore', '.gitignore')
        shutil.rmtree('resources')
        shutil.rmtree('src')
        os.remove('script.py')
        os.remove(configFile)
    except:
        raise SourceChangedError
    commitChanges('.', 'UiT', user, 'Set up my entire folder structure!')

def moveResources(user):
    '''Handles the resources folder'''
    reponame = 'IFI-resources'
    createRepository(reponame, 'Resources used for my stay at IFI-UiT', user)
    submodule("", reponame, user)
    shutil.copytree('resources/report_templates', reponame+'/report_templates')
    commitChanges(reponame+'/', reponame, user, 'Initial repo commit')


def parseFolder(folder, path, user):
    '''Parses a folder and recursively creates sub-folders'''
    createRepository(folder['name'], folder['description'], user)
    submodule(path, folder['name'], user)
    if 'folders' in folder:
        for child in folder['folders']:
            parseFolder(child, path+folder['name']+"/", user)
        # Remove all credentials
        if path != '':
            commitChanges(path+folder['name']+"/", folder['name'], user, 'Init submodules.')
        else:
            commitChanges(folder['name'], folder['name'], user, 'Init submodules')

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
    subprocess.Popen('cd .. && mv IFI-Survival-Kit UiT')