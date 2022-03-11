class RuntimeError(Exception):
    def __init__(self, token, message):
        Exception.__init__(message)
        self.token = token