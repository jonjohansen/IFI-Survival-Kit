from .textcolor import TextColor
from .emojis import Emojis

class NoUsernameError(Exception):
    def __init__(self):
        message = "\n%s%s ERROR: No username was supplied, or was not found in the config%s" % (Emojis.alert, TextColor.red, Emojis.alert)
        super().__init__(message)

class NoPackageError(Exception):
    def __init__(self, package):
        message = ("\n%s%s ERROR: The script cannot continue without installing the following package(s): %s%s %s.") % (Emojis.alert, TextColor.red, TextColor.purple, package, Emojis.alert)
        super().__init__(message)

class NoSuchFileError(Exception):
    def __init__(self, file):
        message = ("\n%s%s ERROR: Woops! Could not find file: %s%s %s.") % (Emojis.alert, TextColor.red, TextColor.purple, file, Emojis.alert)
        super().__init__(message)

class SourceChangedError(Exception):
    def __init__(self):
        message = "\n%s%s ERROR: Source code has changed since you cloned this repository.\n This is causing the code to freak out when attempting to clean up. Please re-clone the source code%s" % (Emojis.alert, TextColor.red, Emojis.alert)
        super().__init__(message)
class BadCredentialError(Exception):
    def __init__(self):
        message = "\n%s%s ERROR: Bad Credentials. Seems like your token is wrong or has expired. %s\n\n" % (Emojis.alert, TextColor.red, Emojis.alert)
        link = ("%sTo find out how to generate a token you can visit\n"
        "https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line %s") % (TextColor.green, Emojis.link)
        super().__init__(message + link)
class NoTokenError(Exception):
    def __init__(self):
        message =   ("\n%s%s ERROR: No token was supplied or was not found in the config%s\n\n") % (Emojis.alert, TextColor.red, Emojis.alert)
        link = ("%sTo find out how to generate a token you can visit\n"
        "https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line %s") % (TextColor.green, Emojis.link)
        super().__init__(message + link)
class GithubError(Exception):
        message = ("\n%s%s ERROR: Something went wrong when communicating with Github %s\n\n") % (Emojis.alert, TextColor.red, Emojis.alert)
        super().__init__(message)