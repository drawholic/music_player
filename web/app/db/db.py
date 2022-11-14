from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from os.path import join, dirname
from .models import SQLModel


dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

DB_USER = os.getenv('PG_USER')
DB_PASS = os.getenv('PG_PASS')
DB_HOST = os.getenv('PG_HOST')
DB_PORT = os.getenv('PG_PORT')
DB_DB = os.getenv('PG_DB')

db_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DB}'
engine = create_async_engine(db_url, echo=True)

session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with session() as s:
        yield s


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
