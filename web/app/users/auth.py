import jwt
from dotenv import load_dotenv
import os

load_dotenv('../.env')

secret = os.getenv('SECRET')


class Auth:

    @classmethod
    def generate_token(cls, email: str):
        token = jwt.encode({'email': email}, secret, algorithm='HS256')
        return token

    @classmethod
    def decode(cls, token: str):
        decoded = jwt.decode(token, secret, algorithms=['HS256'])
        return decoded.get('email')