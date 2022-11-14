from sqlmodel import SQLModel, Field
from pydantic import validator
from ..users.exceptions import PasswordsDontMatch


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)


class UserCreate(UserBase):
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values):
        print(values)
        if 'password1' in values and v != values['password1']:
            raise PasswordsDontMatch
        return v


class User(UserBase, table=True):
    id: int = Field(primary_key=True, index=True)
    password: str

