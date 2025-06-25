class UserNotFoundExeption(Exception):
    detail = 'User not found'


class UserPasswordException(Exception):
    detail = 'Incorrect user password'


class TokenExpired(Exception):
    detail = 'Token has expired'


class TokenNotCorrect(Exception):
    detail = 'Token is not correct'


class TaskNotFound(Exception):
    detail = 'Task is not fount'

