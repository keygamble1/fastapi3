import datetime

from domain.user.user_schema import User
from pydantic import BaseModel, field_validator


class AnswerCreate(BaseModel):
    content:str
    # 필드가 들어갈때 검증하려고 cls를 쓰는경우가많음
    # 자동으로
    @field_validator('content')
    def not_empty(cls,v):
       if not v or not v.strip():
           raise ValueError('빈값허용 x')
       return v 
#    오류가안나면 v.strip()에 not을안쓴거
           #    v.strip()=양쪽끝에있는 공백이런거 제거
    # if등등다있을듯
    # cls로 등록한다는건 AnswerCreate(content="xx")와 같이 인스턴스 생성시
    # 클래스메서드인 def가 실행된다느것
    # post에서는 pydantic스키마로 일겅야하기때뭉네 
    # post,put,delete입력값은  스키마로만하기때문에
    # 빈값일경우의 오류를 지정해줘야함
    # post 메서드따로 get메서드 따로
    # get은 제약조건일ㅃ누이지만 post는 값이 들어가는형태임
    # fieldvalidator는 단일필드 검증 여러필드는 model-vaildator
class AnswerVote(BaseModel):
    answer_id:int

class Answer(BaseModel):
    id:int
    content:str
    create_date:datetime.datetime
    user:User|None
    question_id:int
    modify_date:datetime.datetime | None=None
    voter:list[User]=[]
    # Answer.voter를 svelte에넘기고싶으면해야함
    
class AnswerUpdate(AnswerCreate):
    answer_id:int

class AnswerDelete(BaseModel):
    answer_id:int
    