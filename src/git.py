import subprocess
from subprocess import Popen, DEVNULL
from .errors import CreateRepoError 
import requests

def submodule(path, repo, user, branch='master'):
    ''' Creates a submodule referencing repo at given path
    Branch is set to master by default'''
    url = ("https://%s@github.com/%s/%s.git") % (user.token, user.username, repo)
    addModule = ("git submodule add -b %s %s") % (branch, url)
    cmd = ""
    # Check if we have to cd
    if path != "":
        cmd = 'cd ' + path + ' && '
    cmd += addModule
    proc = subprocess.Popen(cmd, shell=True, stdout=DEVNULL)
    proc.wait()

def commitChanges(path, repo, user, msg):
    ''' CDs into a path and Commits and pushes changes to Github.
    If empty path is given, it will not attempt to clear credentials beforehand 
    
    Note: This action will clone this repository at given path
    '''

    if path != '':
        removeCredentials(path, user)
    cd = 'cd '+ path + '  && '
    cmd = cd + 'git add .'
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    # Commit 
    author = ("%s <%s>") % (user.username, user.email) 
    cmd = cd + ('git commit --author="%s" -m "%s"') % (author, msg)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    # Push
    url = ("https://%s@github.com/%s/%s.git") % (user.token, user.username, repo)
    cmd = cd + 'git push ' + url
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
      
def createRepository(name, description, token, auto_init=True):
    ''' Create a repository using a token, should return the clone url for that token'''
    gitConfig = {
        "name": name,
        "description": description,
        "private": True,
        "has_issues": False,
        "has_projects": False,
        "has_wiki": False,
        "auto_init": auto_init
        }
    
    url = ("https://api.github.com/user/repos?access_token=%s") % (token)
    response = requests.post(url, json=gitConfig) # This is not undefined. 

    if (response.status_code == 201):
        url = response.json()['clone_url']
        return url
    elif (response.status_code == 422):
        if (response.json()['errors'].message == 'name already exists on this account'):
            print('Repository already exists. Will use this in the structure')
            # Lets return the url to this
            return 
        else:
            print('Request was well formed, but there were some semantic errors')
    else:
        raise CreateRepoError

def removeCredentials(path, user):
    ''' Removes token from the path added by submodules '''
    cd = 'cd '+ path + '  && '
    # MacOS actually requires you to pass an emptystring to -i with sed
    # to not create a file. We'll just delete it if it exists
    cmd = cd + ("sed -i -e 's/%s//g' .gitmodules && rm .gitmodules-e") % (user.token+'@')
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def addRemote(remote):
    ''' Simply wraps "git remote add origin"'''
    cmd = ('git remote add origin %s') % (remote)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def createLocalRepository():
    '''Simply wraps "git init"'''
    proc = subprocess.Popen('git init', shell=True)
    proc.wait()
