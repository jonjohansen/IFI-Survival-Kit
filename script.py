#!/usr/local/bin/python3
import json
import os
from src import *
import time

def main():
    # Get the packages necessary
    import_or_install('requests', textColor, emoji)
    # Parse the arguments, get whats missing
    username, token, configFile = parseArgs(textColor)
    # Get config and create elements
    folderConfig = readConfig(configFile)
    print(username, token)
    # Init host repository
    for folder in folderConfig['folders']:
        parseFolder(folder, "", token)
        print("Im creating a subrepo!")
        #submodule()
    removeCredentials('./', username, token)    
    # Remove credentials
def readConfig(config):
    try: 
        with open(config) as file:
            jsonConfig = file.read()
    except:
        raise NoSuchFileError(config)
    return json.loads(jsonConfig)


def parseFolder(folder, path, token):
    # Create repository
    #createRepository(folder['name'], folder['description'], token)
    print(path+folder['name'])
    # Initialize it as a submodule in the right place
    submodule(path+folder['name'])
     
    # Iterate through the sub-folders, and repeat the process
    if 'folders' in folder:
        for child in folder['folders']:
            subname = parseFolder(child, path+folder['name']+"/", token)
            # Create submodule
            print("\t creating submodule", subname)
        # Remove all credentials
    else:
        print("End")
    return folder['name']

def submodule(path):
    # Should be submodules at path - name
    # Add repository as submodule
    pass

if __name__ == "__main__":
    emoji = Emojis()
    textColor = TextColor()
    try:
        main()
    except Exception as error:
        print(error)
    #os.remove('script.py')
