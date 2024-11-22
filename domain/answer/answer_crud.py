
from datetime import datetime

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Answer, Question, User
from sqlalchemy.orm import Session


def create_answer(db:Session,question:Question,answer_create:AnswerCreate,
                  user:User):
    # 자료형을 매개변수선언만하는거
    db_answer=Answer(question=question,
                     content=answer_create.content,
                     create_date=datetime.now(),
                     user=user)
    # 한개만등록하라
    db.add(db_answer)
    db.commit()

def get_answer(db: Session,answer_id:int):
    return db.query(Answer).get(answer_id)
# 한개니까 get
def update_answer(db:Session,db_answer: Answer,
                  answer_update:AnswerUpdate):
    db_answer.content=answer_update.content
    # 이미 정의된 content를 가져오는것
    # 그래서 update할때 기존 class를 가져오는것이다
    db_answer.modify_date=datetime.now()
    db.add(db_answer)
    db.commit()

def delete_answer(db: Session,db_answer: Answer):
    db.delete(db_answer)
    db.commit()

def vote_answer(db: Session,db_answer: Answer,db_user:User):
    db_answer.voter.append(db_user)
    db.commit()