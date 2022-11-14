from ..db.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_users(self):
        stm = select(User)
        users = await self.db.execute(stm)
        users = users.scalars().all()
        return users

    async def create_user(self, user):
        values = user.dict()
        values['password'] = values.get('password1')
        user = User(**values)

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)
        return user
