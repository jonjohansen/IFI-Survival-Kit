#!/usr/local/bin/python3
import json
import os
from src import Emojis, TextColor, parseArgs, import_or_install

def main():
    fileConfig = readConfig()
    for folder in fileConfig['folders']:
        parseFolder(folder, "")


def readConfig():
    with open("structure.json") as file: # Use file to refer to the file object
        jsonConfig = file.read()

    return json.loads(jsonConfig)


def parseFolder(folder, path):
    # Create folder
    name = folder['name']
    createFolder(path+name)
    print(name)
    # Check for children
    if 'folders' in folder:
        #parseFolder(folder['folders'])
        children = folder['folders']
        for child in children:
            parseFolder(child, path+name+"/")
    else:
        print("\t..")

def createFolder(path):
    # Create folder
    os.mkdir(path)
    # Create github repository
    # Init this repository within this path



if __name__ == "__main__":
    try:
        emoji = Emojis()
        textColor = TextColor()
        import_or_install('requests', textColor, emoji)
        username, token = parseArgs(textColor)
        #print("%s %s" % (username, token))
        #main()
    except Exception as error:
        print(error)
    #os.remove('script.py')
