import os
import os.path
from os.path import expanduser
from subprocess import Popen, PIPE


def is_github():
    '''
        Check if repo is stored on github. Only change url for github
    '''

    pipe = Popen("git config --get remote.origin.url", shell=True, stdout=PIPE).stdout
    output = pipe.read().strip()

    if "github" in str(output):
        return 1
    else:
        return -1


def parse_url():
    '''
        Parses the username and name of repository for the change to ssh
    '''

    pipe = Popen("git config --get remote.origin.url", shell=True, stdout=PIPE).stdout
    output = pipe.read().strip()

    url = str(output).strip("'")
    
    if "git@github" in url:
        start = url.find(':') + 1
        url = url[start:]
    else:
        start = url.find('com/') + 4
        url = url[start:]

    return url

def is_git_repo(path):
    ''' 
        Takes a path to a directory and returns a boolean representing 
        if the given directory is a git repository
    '''
    if os.path.isfile(path):
        # Handle paths leading to files first
        return False

    return '.git' in os.listdir(path)

def change_url(path):
    '''
        Recursively changes remote url from HTTPS to SSH for all repositories within the given path
    '''
    os.chdir(path)
    if (is_git_repo(os.getcwd())):
        #Gets name of current folder
    
        github = is_github()

        if github == 1:
            foldername = os.path.basename(os.getcwd())
            new_url = parse_url()
            url = ("git@github.com:%s") % (new_url)
            ssh_url = ("git remote set-url origin %s") % (url)
            print(("Changing URL from HTTPS to SSH in %s") % (foldername))
            os.system(ssh_url) 
            
            #Get names of all directories in a directory.
            all_subdirs = ([name for name in os.listdir(".") if os.path.isdir(name)])
            # print(all_subdirs)
            for dirs in all_subdirs:
                if dirs == ".git": continue

                old_path = os.getcwd()
                new_path = ("%s/%s") % (old_path, dirs)
                change_url(new_path)
                os.chdir(old_path)
                    
    else:
        print(("%s is not a repository") % (path))
    
    #Change directory to home 
    os.chdir(expanduser("~"))

def user_input():
    '''
        Gets starting directory from user
    '''
    abs_path = os.path.expanduser("~")
    while True:
        path = input("Enter name of starting directory starting from home: ")
        if (os.path.exists(path) == False):
            print(("\n%s is not a directory, try again") % (path))
            print("If starting directory is for example ~/UiT, write UiT.\nIf it's ~/UiT/test, write UiT/test\n")
        else:
            break
        
    return path 

def get_repo_info(path):
    '''
        Adds name of folder and username to a dictionary
    '''

    usernames = {}
    for dir in path:

        old_path = os.getcwd()
        os.chdir(dir)
        cwd = os.getcwd()

        pipe = Popen("git config --get remote.origin.url", shell=True, stdout=PIPE).stdout
        output = pipe.read().strip()

        url = str(output).strip("'")
        username = ""

        if "http" in url:
            start = url.find('://') + 3
            end = url.rfind("/")
            username = url[start:end]
        else:
            start = url.find(":") + 1
            end = url.rfind("/")
            username = url[start:end]

        usernames[dir] = username
        os.chdir(old_path)
        
    return usernames



def change_gitmodules(path):
    '''
        Deletes .gitmodules in every repository and creates a new .gitmodules with url in ssh format
    '''
    submodules = []
    username = {}
    os.chdir(path)
    folder = (os.path.basename(os.getcwd()))
    all_subdirs = ([name for name in os.listdir(".") if os.path.isdir(name)])
    
    #Appends the name of every directory inside the current directory to an empty list
    for dirs in all_subdirs:
        if dirs == ".git": continue     
        git_check = os.path.exists(("%s/.git") % (dirs))
        if (git_check == True):
            submodules.append(dirs)

    url_dict = get_repo_info(submodules)
    
    if (os.path.isfile(".gitmodules") == True):
        os.remove(".gitmodules")
    
    #Loops through the list and write .gitmodules
    for dirs in url_dict:

        url = ("git@github.com:%s/%s.git") % (url_dict[dirs], dirs)   
        f = open(".gitmodules", "a+")
        print(("Editing .gitmodules in %s") % (os.getcwd()))
        f.write(("""
[submodule "%s"]
    path = %s
    url = %s
    branch = master
                """) % (dirs, dirs, url))
        
        f.close()
            
        old_path = os.getcwd()
        new_path = ("%s/%s") % (old_path, dirs)
        change_gitmodules(new_path)
        os.chdir(old_path)

    #Change directory to home
    os.chdir(expanduser("~"))

if __name__ == "__main__":
    print("Use this at your own risk. Should work on the UiT-structure for submodules, but there\nare some bugs with submodules that's not on github, but gitlab for example.\n")
    os.chdir(expanduser("~"))
    path = user_input()
    change_gitmodules(path)
    change_url(path)

