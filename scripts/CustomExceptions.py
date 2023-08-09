class DirectoryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class FileTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class ObjectExistError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class InputSizeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)