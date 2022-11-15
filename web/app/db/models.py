from sqlmodel import SQLModel, Field
from pydantic import validator, EmailStr
from ..users.exceptions import PasswordsDontMatch
from typing import Optional


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)


class UserCreate(UserBase):
    password1: str
    password2: str
    is_staff: bool

    @validator('password2')
    def passwords_match(cls, v, values):
        print(values)
        if 'password1' in values and v != values['password1']:
            raise PasswordsDontMatch
        return v


class UserUpdate(SQLModel):
    username: Optional[str]
    password1: Optional[str]
    password2: Optional[str]

    @validator('password2')
    def passwords_match(cls, v, values):
        print(values)
        if 'password1' in values and v != values['password1']:
            raise PasswordsDontMatch
        return v


class User(UserBase, table=True):
    id: int = Field(primary_key=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_staff: bool = Field(default=False)


class SongBase(SQLModel):
    title: str


class Song(SongBase, table=True):
    id: int = Field(primary_key=True, index=True)
