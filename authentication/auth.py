from datetime import timedelta, datetime
from typing import Annotated
from config.database import SessionLocal
from config.dependencies import db_dependency
from config.models import User
from config.schemas import UserSchema
from config.config import AUTH_ALGORITHM, AUTH_SECRET_KEY
from authentication.schemas import TokenSchema 
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


bcrypt_context = CryptContext(schemes=['bcrypt'])


@router.post('/user/create', status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserSchema, db: db_dependency):
    user_dict = user.dict()

    new_user = User(username=user.username, password=bcrypt_context.hash(user.password))
    db.add(new_user)
    db.commit()

    return {'user': user}


@router.post('/token', response_model=TokenSchema)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires: timedelta):
    enc = {'sub': username, 'id': user_id}
    exp = datetime.utcnow() + expires
    enc.update({'exp': exp})

    return jwt.encode(enc, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
