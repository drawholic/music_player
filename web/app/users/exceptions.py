from fastapi import HTTPException


class PasswordsDontMatch(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Passwords dont match')


class UserDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='User Does Not Exist')


class UserDoesNotExistOrDisabled(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='User does not exist or disabled')

