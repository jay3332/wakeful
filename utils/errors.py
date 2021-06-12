class wakefulError(Exception):
    pass

class TooLong(wakefulError):

    def __init__(self):
        pass

    def __str__(self):
        return "The video cannot be longer than 5 minutes"