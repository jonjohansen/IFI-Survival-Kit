#!/usr/local/bin/python3
import json
import os
from src import Emojis, TextColor, parseArgs, import_or_install, NoSuchFileError
import requests
import time

def main():
    import_or_install('requests', textColor, emoji)
    username, token, configFile = parseArgs(textColor)
    folderConfig = readConfig(configFile)
    print(username, token)
    for folder in folderConfig['folders']:
        parseFolder(folder, "")


def readConfig(config):
    try: 
        with open(config) as file:
            jsonConfig = file.read()
    except:
        raise NoSuchFileError(config)
    return json.loads(jsonConfig)


def parseFolder(folder, path):
    # Create folder
    name = folder['name']
    createFolder(path+name)
    print(emoji.folder+" ", end="")
    # See if there are sub-directories
    if 'folders' in folder:
        for child in folder['folders']:
            parseFolder(child, path+name+"/")
    # If there are no child folders
    else:
        print()

def createFolder(path):
    time.sleep(0.2)
    # Create folder
    #print(path)
    #os.mkdir(path)
    # Create github repository
    # Init this repository within this path



if __name__ == "__main__":
    emoji = Emojis()
    textColor = TextColor()
    try:
        main()
    except Exception as error:
        print(error)
    #os.remove('script.py')
