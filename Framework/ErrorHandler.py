class UccountError(Exception):
    def __init__(self, argument):
        self.argument = argument


class CreditError(Exception):
    def __init__(self, argument):
        self.argument = argument


class MusicError(Exception):
    def __init__(self, error):
        self.error = error


class YAMLError(Exception):
    def __init__(self, error):
        self.error = error
