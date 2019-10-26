import git
import os
import os.path
from os.path import expanduser

#Returns True if path is a repository, and False if not.
def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

#Changes remote url from HTTPS to SSH for all repositories inside a main repository
def change_url(path, user):
    
    os.chdir(path)
    if is_git_repo(os.getcwd()) == True:
        #Gets name of current folder
        foldername = os.path.basename(os.getcwd())
        url = ("git@github.com:%s/%s.git") % (user, foldername)
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
            change_url(new_path, user)
            os.chdir(old_path)
                    
    else:
        print(("%s is not a repository") % (path))
    
    #Change directory to home 
    os.chdir(expanduser("~"))

#Gets github-username and starting directory from user
def user_input():
    
    while True:
        user = input("Enter your github-username: ")
        user_check = input(("Are you sure your username is '%s'? (y/n): ") % (user))
        if (user_check == "n" or user_check == "N"):
            print("Try again") 
        elif (user_check == "y" or user_check == "Y"):
            break;
            
    while True:
        path = input("Enter name of starting directory: ")
        if (os.path.exists(path) == False):
            print(("%s is not a directory, try again") % (path))
        else:
            break
        
    return path, user; 

#Deletes .gitmodules in every repository and creates a new .gitmodules with url = ssh
def change_gitmodules(path, user):
    
    submodules = []
    os.chdir(path)
    folder = (os.path.basename(os.getcwd()))
    all_subdirs = ([name for name in os.listdir(".") if os.path.isdir(name)])
    
    #Appends the name of every directory inside the current directory to an empty list
    for dirs in all_subdirs:
        if dirs == ".git": continue     
        git_check = os.path.exists(("%s/.git") % (dirs))
        if (git_check == True):
            submodules.append(dirs)
    
    if (os.path.isfile(".gitmodules") == True):
        os.remove(".gitmodules")
    
    #Loops through the list and write .gitmodules
    for dirs in submodules:
        url = ("git@github.com:%s/%s.git") % (user, dirs)   
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
        change_gitmodules(new_path, user)
        os.chdir(old_path)

    #Change directory to home
    os.chdir(expanduser("~"))

if __name__ == "__main__":
    os.chdir(expanduser("~"))
    path, user = user_input()
    change_gitmodules(path, user)
    change_url(path, user)
