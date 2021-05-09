import os

class ApiException(Exception):
    pass


class ErrorCode:
    ACCESS_DB_CONNECTION_ERROR = 'E10000'

    INTERNEL_ERROR = 'E20000'

    INVALID_BODY = 'E30000'
    INVALID_SALT = 'E30001'
    INVALID_USERNAME = 'E30002'
    WRONG_PASSWORD = 'E30003'
    LOGIN_NEEDED = 'E30004'

class ErrorMessage:
    ACCESS_DB_CONNECTION_ERROR = 'Cannot get database connection string'

    INTERNEL_ERROR = 'Unexpected internal error'

    INVALID_BODY = 'Invalid request body'
    INVALID_SALT = 'Invalid salt, please request a new salt'
    INVALID_USERNAME = 'User does not exists'
    WRONG_PASSWORD = 'Password is incorrect'
    LOGIN_NEEDED = 'Need to login'

class Constants:
    CONST_SALT = os.environ.get('CONST_SALT')
    SALT_LEN = 6
    SALT_EXPIRE_TIME = 360
    TOKEN_EXPIRE_TIME = 3600
    