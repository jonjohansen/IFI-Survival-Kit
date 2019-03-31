from .textcolor import TextColor
from .emojis import Emojis

class NoTokenError(Exception):
    def __init__(self):
        textColor = TextColor()
        emoji = Emojis()
        message =   ("\n%s%s ERROR: No token was supplied or was not found in the config%s\n\n") % (emoji.alert, textColor.red, emoji.alert)
        link = ("%sTo find out how to generate a token you can visit\n"
        "https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line %s") % (textColor.green, emoji.link)
        super().__init__(message + link)

class NoUsernameError(Exception):
    def __init__(self):
        textColor = TextColor()
        emoji = Emojis()
        message = "\n%s%s ERROR: No username was supplied, or was not found in the config%s" % (emoji.alert, textColor.red, emoji.alert)
        super().__init__(message)