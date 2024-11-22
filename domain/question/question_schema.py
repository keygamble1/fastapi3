import datetime

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User
from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class QuesetionVote(BaseModel):
    question_id:int
    
class QuestionDelete(BaseModel):
    question_id:int
    
class Question(BaseModel):
    id:int
    subject:str
    content:str
    create_date:datetime.datetime
    answers:list[Answer]=[]
    user:User|None
    # 나중에할당
    modify_date:datetime.datetime | None=None
    voter:list[User]=[]
    # None이어도되고 할당안되도됨
    # 필드만받고 api갱신되므로 html바로 넣을수있음 그냥 옵션추가만하는거니까
    # schema로 받아버릴수도있음이때 그냥 업데이트됨
    # 스키마는 스키마끼리 받을수있음
    # 이걸받으면 위 네개만가능
    # create_date빼면 create_date빼고 가져간다여기서 조절가능함
    # default값없어서 필수항목 
    # 필수항목아니게 설정하고싶을시 subject str |None = None하면됨
    class Config:
        orm_mode=True

class QuestionCreate(BaseModel):
    subject:str
    content:str

    @field_validator('subject','content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈값x')
        return v
class QuestionList(BaseModel):
    total:int=0
    question_list:list[Question]=[]
    # scema는 리턴하는 값을 조절하기위해 쓴다고보자

class QuestionUpdate(QuestionCreate):
    question_id:int
    # 새로 return할 updated quesiton_id포함한
    
    