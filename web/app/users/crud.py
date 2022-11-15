from ..db.models import User, UserUpdate
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .exceptions import UserDoesNotExistOrDisabled


class UserCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_users(self) -> List[User]:
        stm = select(User).where(User.is_active)
        users = await self.db.execute(stm)
        users = users.scalars().all()
        return users

    async def get_user_by_id(self, id: int) -> User:
        stm = select(User).where(and_(User.id == id, User.is_active))
        stm = await self.db.execute(stm)
        user = stm.scalars().first()
        if user is None:
            raise UserDoesNotExistOrDisabled
        return user

    async def get_user_by_email(self, email: str) -> User:
        stm = select(User).where(and_(User.email == email, User.is_active))
        stm = await self.db.execute(stm)
        user = stm.scalars().first()
        if user is None:
            raise UserDoesNotExistOrDisabled
        return user

    async def create_user(self, user) -> User:
        values = user.dict()
        values['password'] = values.get('password1')
        user = User(**values)

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_email: str, user_data: UserUpdate) -> User:
        user = await self.get_user_by_email(email=user_email)
        data = user_data.dict(exclude_unset=True)

        for key in data.keys():
            setattr(user, key, data[key])

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_email: str) -> None:
        user = await self.get_user_by_email(email=user_email)
        await self.db.delete(user)

    async def disable_user(self, user_email: str):
        user = await self.get_user_by_email(email=user_email)
        setattr(user, 'is_active', False)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

