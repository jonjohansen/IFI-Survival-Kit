import subprocess
from subprocess import Popen, DEVNULL
import requests
def submodule(path, repo, user):
    url = ("https://%s@github.com/%s/%s.git") % (user.token, user.username, repo)
    addModule = "git submodule add -b master "+ url
    cmd = ""
    # Check if we have to cd
    if path != "":
        cmd = 'cd ' + path + ' && '
    cmd += addModule
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True, stdout=DEVNULL)
    proc.wait()

def commitChanges(path, repo, user, msg):
    if path != '':
        removeCredentials(path, user)
    print(("PUSHING %s TO %s" % (path, repo)), flush=True)
    cd = 'cd '+ path + '  && '
    cmd = cd + 'git add .'
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    author = ("%s <%s>") % (user.username, user.email) 
    cmd = cd + ('git commit --author="%s" -m "%s"') % (author, msg)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    url = ("https://%s@github.com/%s/%s.git") % (user.token, user.username, repo)
    cmd = cd + 'git push ' + url
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
      
def createRepository(name, description, token, auto_init=True):
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
    # Need to take a closer look into this
    
    
    if (response.status_code != 201):
        print(response.status_code)
        print("Something went wrong")
        raise EnvironmentError
        # 422 = Unprocessable entry aka already exists
    else:
        url = response.json()['clone_url']
        return url

def removeCredentials(path, user):
    cd = 'cd '+ path + '  && '
    # MacOS actually requires you to pass an emptystring to -i with sed
    # to not create a file. We'll just delete it if it exists
    cmd = cd + ("sed -i -e 's/%s//g' .gitmodules && rm .gitmodules-e") % (user.token+'@')
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def addRemote(remote):
    cmd = ('git remote add origin %s') % (remote)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

def createLocalRepository():
    proc = subprocess.Popen('git init', shell=True)
    proc.wait()
