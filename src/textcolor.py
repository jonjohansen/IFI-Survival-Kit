import sys
class TextColor(object):
    def __init__(self):
        # Add dictionary of text colors
        self.__dict__.update(
            {
            "black" : "\033[1;30;49m",
            "red" : "\033[1;31;49m",
            "green" : "\033[1;32;49m",
            "yellow" : "\033[1;33;49m",
            "blue" : "\033[1;34;49m",
            "purple" : "\033[1;35;49m",
            "cyan" : "\033[1;36;49m",
            "white" : "\033[1;37;49m",
            "reset" : "\033[m",
            })
    def __getattr__(self, name):
        raise AttributeError("%r instance has no attribute %r" % (self, name))

def printBlack(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;30;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printRed(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;31;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printGreen(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;32;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printYellow(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;33;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printBlue(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;34;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printPurple(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;35;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printCyan(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;36;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)
def printWhite(msg, sep='', end='\n', file=sys.stdout, flush=False):
    print("\033[1;37;49m" + msg + "\033[m", sep=sep, end=end, file=file, flush=False)