import argparse
import subprocess
import os
import json
from .errors import NoUsernameError, NoTokenError, NoPackageError, NoSuchFileError
from .textcolor import TextColor, printBlue, printYellow, printPurple, printGreen, printRed, printCyan
from .emojis import Emojis
from pip._internal import main as pipmain
from .user import User
import importlib

def parseArgs():
    ''' Parses arguments and handles all the user input at the initial part of the script
    Should return the final username and token for the script to use 
    '''

    desc = '''
    This is a small script helping with setting up a folder structure based on a configuration.

    The script will parse through the structure.json file within the same folder, and 
    create a folder structure, with a matching github structure
    '''

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username', metavar="<username>", type=str, help='Github username')
    parser.add_argument('-t','--token', metavar="<token>", type=int, help='Personal access token')
    parser.add_argument('-e','--email', metavar="<Email>", type=int, help='Github email')
    parser.add_argument('-c','--config', metavar="<PATH>", type=str, default='structure.json', help='JSON file describing folder structure')

    args = parser.parse_args()
    
    if not args.username or not args.token or not args.email:
        printCyan("%s Welcome to IFI Survival Kit %s" % (Emojis.graduation_cap, Emojis.safety_helmet))
        printBlue("We'll have you sorted and organized in no time %s" % Emojis.fire)
        printRed("\nSome parameters were omitted.")
        printBlue("Checking global git config for default credentials....\n")

        configUsername = subprocess.Popen("git config --global user.name", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
        configToken = subprocess.Popen("git config --global user.token", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
        configEmail = subprocess.Popen("git config --global user.email", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
    
    # Ask user for username
    if not (args.username):
        printPurple("Please enter your Github username:", end='')
        # Check if there was a configUsername, if so supply it as arg
        if (configUsername != ""):
            printGreen(" (default: '%s')" % (configUsername))
        else:
            printBlue(" (no default found)")
        inputUsername = input()
        if (inputUsername == ""):
            if (configUsername == ""):
                raise NoUsernameError
            else:
                username = configUsername
        else:
            username = inputUsername
    else:
        username = args.username
    
    # Ask for user token
    if not (args.token):
        printPurple("Please enter your Github access token:", end='')
        if (configToken != ""):
            printGreen(" (default '%s') " % (configToken))
        else:
            printBlue(" no default found)")
        inputToken = input()
        if (inputToken == ""):
            if (configToken == ""):
                raise NoTokenError
            else:
                token = configToken
        else:
            token = inputToken
    else:
        token = args.token

    # Ask for user email    
    if not (args.email):
        printPurple("Please enter your Github email address:", end='')
        if (configToken != ""):
            printGreen(" (default '%s')" % (configEmail))
        else:
            printBlue(" (no default found)%s")
        inputEmail = input()
        if (inputEmail == ""):
            if (configEmail == ""):
                printYellow("Commits will be made without an author e-mail")
            else:
                email = configEmail
        else:
            email = inputEmail
    else:
        token = args.token
    
    user = User(username, email, token)
    return user, args.config

def import_or_install(package):
    ''' Tries to import a package. If package is not found it prompts the user to install it through pip'''
    try:
        __import__(package)
        globals()[package] = importlib.import_module(package)
    except ImportError:
        print(("%s %sPip package %s%s %sis missing") % (Emojis.package, TextColor.blue, TextColor.purple, package, TextColor.blue))
        print(("%sYou can uninstall this afterwards with %s'pip uninstall %s'") % (TextColor.blue, TextColor.yellow, package) )
        printBlue(("Do you want to install it"), end="")
        res = input(("%s (y/n) ") % (TextColor.green))

        if (res == "y" or res == "Y"):
            pipmain(['install', package])
            globals()[package] = importlib.import_module(package)
        else:
            raise NoPackageError(package)



def readConfig(config):
    try: 
        with open(config) as file:
            jsonConfig = file.read()
    except:
        raise NoSuchFileError(config)
    return json.loads(jsonConfig)
