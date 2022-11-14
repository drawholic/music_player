from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .crud import UserCrud
from ..db.db import get_session
from ..db.models import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

token_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(prefix='/user', tags=['User'])


@router.get('')
async def get_users(db: AsyncSession = Depends(get_session)):
    return await UserCrud(db).get_users()


@router.post('')
async def sign_up(user: UserCreate, db: AsyncSession = Depends(get_session)):
    print('before usercrud')
    return await UserCrud(db).create_user(user)


@router.post('/login')
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    return form_data