#!/usr/local/bin/python3

import json
import os
import argparse
import subprocess
from src import TextColor, NoTokenError, NoUsernameError

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

def parseArgs():
    desc = '''
    This is a small script helping with setting up a folder structure based on a configuration.

    The script will parse through the structure.json file within the same folder, and 
    create a folder structure, with a matching github structure
    '''
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username', metavar="STR", type=str, help='Github username')
    parser.add_argument('-t','--token', metavar="NUM", type=int, help='Personal access token')
    parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    
    if not args.username or args.token:
        print("%sSome parameters was omitted.%s\nChecking global git config for defaults...%s" % (textColor.red, textColor.blue, textColor.blue))
        configUsername = subprocess.Popen("git config --global user.name", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
        configToken = subprocess.Popen("git config --global user.token", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
    
    # Ask user for username
    if not (args.username):
        print("%sPlease enter your Github username:" % (textColor.purple), end='')
        # Check if there was a configUsername, if so supply it as arg
        if (configUsername != ""):
            print("%s (default '%s')%s" % (textColor.green, configUsername, textColor.reset))
        else:
            print("%s (no default found)%s" % (textColor.blue, textColor.reset))
        inputUsername = input()
        if (inputUsername == ""):
            if (configUsername == ""):
                raise NoUsernameError
            else:
                username = configUsername
        else:
            username = inputUsername

    # Ask for user token
    if not (args.token):
        print("%sPlease enter your Github access token:" % (textColor.purple), end='')
        if (configToken != ""):
            print("%s(default '%s') %s" % (textColor.green, configToken, textColor.reset))
        else:
            print("%s (no default found)%s" % (textColor.blue, textColor.reset))
        inputToken = input()
        if (inputUsername == ""):
            if (configToken == ""):
                raise NoTokenError
            else:
                token = configToken
        else:
            token = inputToken

    return username, token

if __name__ == "__main__":
    
    textColor = TextColor()
    try:
        username, token = parseArgs()
        #print("%s %s" % (username, token))
        #main()
    except Exception as error:
        print(error)

