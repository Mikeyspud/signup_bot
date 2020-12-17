class Error(Exception):
    pass

class OperationExists(Error):
    pass

class InvalidArguments(Error):
    pass

class InvalidSquad(Error):
    pass
