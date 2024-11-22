from turtle import st

from pydantic import *
from pydantic_core.core_schema import FieldValidationInfo

# `sessionmaker` is a function typically used in SQLAlchemy, a popular Python SQL toolkit and Object-Relational Mapping (ORM) library. In SQLAlchemy, `sessionmaker` is used to create a session factory, which is responsible for producing new `Session` instances. These `Session` instances are used to interact with the database and perform various operations like querying, adding, updating, and deleting data.

class User(BaseModel):
    id:int
    username:str
    email:str
    

class UserCreate(BaseModel):
    username:str
    password1:str
    password2:str
    email:EmailStr
    
    @field_validator('username','password1','password2','email')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈값x')
        return v
    @field_validator('password2')
    def passwords_match(cls,v,info : FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호불일치')
        return v
class Token(BaseModel):
    access_token:str
    token_type:str
    username:str
# It seems like there is a typo in the code snippet you provided. The line `sessionmake` is not a valid Python statement or function call. It appears to be incomplete or incorrect. If you intended to use a function or method related to creating a session, please provide more context or correct the code so I can assist you further.
