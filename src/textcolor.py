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
  