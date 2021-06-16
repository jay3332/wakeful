class Error(Exception):
    pass

class TooLong(Error):

    def __init__(self):
        pass

    def __str__(self):
        return "The video cannot be longer than 15 minutes"
