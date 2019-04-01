from .textcolor import TextColor
from .emojis import Emojis

class CustomException():
    def __init__(self):
        self.textColor = TextColor()
        self.emoji = Emojis()
class NoTokenError(Exception, CustomException):
    def __init__(self):
        CustomException.__init__(self)
        message =   ("\n%s%s ERROR: No token was supplied or was not found in the config%s\n\n") % (self.emoji.alert, self.textColor.red, self.emoji.alert)
        link = ("%sTo find out how to generate a token you can visit\n"
        "https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line %s") % (self.textColor.green, self.emoji.link)
        super().__init__(message + link)

class NoUsernameError(Exception, CustomException):
    def __init__(self):
        message = "\n%s%s ERROR: No username was supplied, or was not found in the config%s" % (self.emoji.alert, self.textColor.red, self.emoji.alert)
        super().__init__(message)

class NoPackageError(Exception, CustomException):
    def __init__(self, package):
        CustomException.__init__(self)
        message = ("\n%s%s ERROR: The script cannot continue without installing the following package(s): %s%s %s.") % (self.emoji.alert, self.textColor.red, self.textColor.purple, package, self.emoji.alert)
        super().__init__(message)

class NoSuchFileError(Exception, CustomException):
    def __init__(self, file):
        CustomException.__init__(self)
        message = ("\n%s%s ERROR: Woops! Could not find file: %s%s %s.") % (self.emoji.alert, self.textColor.red, self.textColor.purple, file, self.emoji.alert)
        super().__init__(message)