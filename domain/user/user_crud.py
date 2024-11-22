
import email

from domain.user.user_schema import UserCreate
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db:Session,
                user_create:UserCreate):
    # 입력받은걸해쉬값으로 저장하라
    db_user=User(username=user_create.username,
                 password=pwd_context.hash(user_create.password1),
                 email=user_create.email)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session,
                      user_create: UserCreate):
    return db.query(User).filter(
        #괄호없을시 순서대로하므로 괄호있어야함
        (User.username==user_create.username)|
        (User.email==user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
# 전체 Username에서 모개변수에있는 username을 찾아라