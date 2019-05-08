import os, sys, subprocess
from subprocess import Popen, DEVNULL, STDOUT
from .errors import BadCredentialError, GithubError
from .textcolor import TextColor, printBlue, printYellow
from .emojis import Emojis

def TestToken(token):
    url = 'https://api.github.com?access_token=%s' % token
    import requests
    res = requests.get(url)
    if res.status_code == 200:
        return True
    else:
        raise BadCredentialError

def submodule(repo, user, branch='master'):
    ''' Creates a submodule
    Branch is set to master by default'''
    url = ("https://%s@github.com/%s/%s.git") % (user.token, user.username, repo)

    cmd = ("git submodule add -b %s %s") % (branch, url)
    proc = subprocess.Popen(cmd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    proc.wait()

def commitChanges(repo, user, msg):
    '''Commits and pushes changes to Github.
    If empty path is given, it will not attempt to clear credentials beforehand 
    
    Note: This action will clone this repository at given path
    '''
    # Remove the token from submodules before commiting. Always
    removeCredentials(user)
    
    # Add all the files
    cmd = 'git add .'
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()

    # Commit 
    author = ("%s <%s>") % (user.username, user.email) 
    cmd = 'git commit --author="%s" -m "%s"' % (author, msg)
    proc = subprocess.Popen(cmd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    proc.wait()

    # Push
    url = ("https://%s@github.com/%s/%s.git") % (user.token, user.username, repo)
    cmd = 'git push ' + url
    proc = subprocess.Popen(cmd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    proc.wait()
      
def createRepository(name, description, user, auto_init=True):
    ''' Create a repository using user.token, should return the clone url for that token'''
    gitConfig = {
        "name": name,
        "description": description,
        "private": True,
        "has_issues": False,
        "has_projects": False,
        "has_wiki": False,
        "auto_init": auto_init
        }
    
    url = ("https://api.github.com/user/repos?access_token=%s") % (user.token)
    import requests
    response = requests.post(url, json=gitConfig) # This is not undefined.
    # Give some user response
    sys.stdout.write(Emojis.folder + " ")
    sys.stdout.flush()
    if (response.status_code == 201):
        url = response.json()['clone_url']
        return url
    elif (response.status_code == 422):
        if (response.json()['errors'][0]['message'] == 'name already exists on this account'):
            printBlue(('\n%s The repository') % (Emojis.dissy), end=' ')
            printYellow(name, end=' ')
            printBlue('already exists on your account and could not be created.')
            printBlue("We'll include the existing repository in this folder instead %s" % Emojis.linked_paperclip)
            # Lets return the url to this
            return ('https://github.com/%s/%s.git') % (user.username, name)
        else:
            #Request was well formed, but there were some semantic errors
            raise GithubError
    elif (response.status_code == 401):
        # Bad credentials
        raise BadCredentialError
    else:
        raise GithubError

def removeCredentials(user):
    ''' Removes token from the path added by submodules '''
    if os.path.isfile('.gitmodules'):
        # MacOS actually requires you to pass an emptystring to -i with sed
        # to not create a file. We'll just delete it if it exists
        cmd = ("sed -i -e 's/%s//g' .gitmodules && rm .gitmodules-e") % (user.token+'@')
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()

def addRemote(remote):
    ''' Simply wraps "git remote add origin"'''
    cmd = ('git remote add origin %s') % (remote)
    proc = subprocess.Popen(cmd, shell=True, stdout=DEVNULL, stderr=STDOUT)
    proc.wait()

def createLocalRepository():
    '''Simply wraps "git init"'''
    proc = subprocess.Popen('git init', shell=True, stdout=DEVNULL, stderr=STDOUT)
    proc.wait()
