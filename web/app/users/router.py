from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .crud import UserCrud
from .auth import Auth
from ..db.db import get_session
from ..db.models import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import UserDoesNotExist

token_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')

router = APIRouter(prefix='/user', tags=['User'])


@router.get('')
async def get_users(db: AsyncSession = Depends(get_session)):
    return await UserCrud(db).get_users()


@router.post('')
async def sign_up(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await UserCrud(db).create_user(user)


@router.post('/token')
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(),
                  db: AsyncSession = Depends(get_session)):
    user = await UserCrud(db).get_user_by_email(form_data.username)
    if user is None:
        raise UserDoesNotExist
    token = Auth.generate_token(email=user.email)
    return {'access_token': token, 'token_type': 'bearer'}


@router.patch('/update')
async def update_user(user: UserUpdate,
                      token: str = Depends(token_scheme),
                      db: AsyncSession = Depends(get_session)):
    email = Auth.decode(token)
    return await UserCrud(db).update_user(user_email=email, user_data=user)


@router.delete('/delete_user')
async def delete_user(user_email: str,
                      token: str = Depends(token_scheme),
                      db: AsyncSession = Depends(get_session)):
    email = Auth.decode(token)
    curr_user = await UserCrud(db).get_user_by_email(email=email)
    if curr_user.is_staff:
        await UserCrud(db).delete_user(user_email=user_email)


@router.delete('/disable')
async def disable_user(user_email: str,
                       token: str = Depends(token_scheme),
                       db: AsyncSession = Depends(get_session)):
    email = Auth.decode(token)
    curr_user = await UserCrud(db).get_user_by_email(email=email)
    if curr_user.is_staff or curr_user.email == user_email:
        await UserCrud(db).disable_user(user_email=user_email)

