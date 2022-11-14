from fastapi import HTTPException


class PasswordsDontMatch(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Passwords dont match')