class InvalidCredentials(Exception):

    def __init__(self, message='Invalid credentials'):
        super().__init__(message)


class ForbiddenException(Exception):

    def __init__(self, message='Access denied'):
        super().__init__(message)


class NotFoundException(Exception):

    def __init__(self, message='Nothing found'):
        super().__init__(message)


class DatabaseException(Exception):

    def __init__(self, message='Something went wrong in db'):
        super().__init__(message)
