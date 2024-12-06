
from datetime import datetime, timedelta
from os import access

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context
from domain.user.user_schema import UserCreate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

config=Config('.env')
# Config사용시 .env파일 설정변수읽을수있음

ACCESS_TOKEN_EXPIRE_MINUTES=int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY=config('SECRET_KEY')
ALGORITHM = "HS256"
oauth2_schema=OAuth2PasswordBearer(tokenUrl="/api/user/login")
router=APIRouter(
    prefix='/api/user',
)
def get_current_user(token:str=Depends(oauth2_schema),
                    #  미리 yield하는게있을거임 Depends니까 그걸받아서 쓰면됨
                    #  bearer끝나면 token에 알아서 넣음
                     db: Session=Depends(get_db)
                     ):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
    except JWTError:
        raise credentials_exception
    else:
        user=user_crud.get_user(db,username=username)
        if user is None:
            raise credentials_exception
        return user
@router.post('/login',response_model=user_schema.Token)
def login_for_access_token(form_data:OAuth2PasswordRequestForm =Depends(),
                           db: Session=Depends(get_db)):
    # form_data는 이제 메서드 다실행되면 끝에 Oatuth가 다 처리해줄거임
    
    user=user_crud.get_user(db,form_data.username)
    # not도 써야함
    if not user or not pwd_context.verify(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data={
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    }
    access_token=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
# 리턴값없으므로 status로 그냥 응답하면됨 get이면 스키마에서 알아서 처리하나?
@router.post('/create',status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_create:UserCreate,
                db: Session=Depends(get_db)):
    user=user_crud.get_existing_user(db=db,user_create=user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미있는사용자")
    user_crud.create_user(db=db,user_create=user_create)
