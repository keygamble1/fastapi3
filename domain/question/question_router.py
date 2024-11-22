
from database import SessionLocal, get_db
from domain.question import question_crud, question_schema
from domain.user.user_router import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from models import Question, User
from sqlalchemy.orm import Session
from starlette import status

router=APIRouter(
    prefix="/api/question",
)


@router.get("/list",response_model=question_schema.QuestionList)
def question_list(db:Session=Depends(get_db),
                  page:int=0,size:int=10,keyword:str=''):
    # Depends에는 contextmagener를 자동적용하기때문에 없애야함
    
# 라우팅이란 fastapi가 받은 url을해석해 그에맞는 함수를 실행후 리턴하는 행위

#  with get_db() as db:
    total,_question_list=question_crud.get_question_list(db,skip=page*size,
                                                         limit=size,keyword=keyword)
    
    # 이런식으로 계속 초기할바에는 그냥 매개변수로 놓고 돌려쓰는게나음
    # 이 리턴값은 반드시 response_model의 리턴값과 같아야하긴하지만
    # 스키마를 제거하면 자동으로 반영되서 나타남
    # 이건현재 모델값이지 딕셔너리가아님
    # 리턴값이 틀린데, Question모델은 자동으로 schema로 변환되지않음
    # 이때 orm_mode=True하면 이름일치하는 항목들이 스키마에 매핑됨
    # responsemodel과 return은 같아야함
    return {
        'total':total,
        'question_list':_question_list
    }
# 스키마는 외부공개되면안되는게있을수있고, 출력값검증하고싶을때도있음
@router.get('/detail/{question_id}',response_model=question_schema.Question)
def question_detail(question_id:int,db: Session=Depends(get_db)):
    question=question_crud.get_question(db,question_id=question_id)
    return question
# api테스트할시 오른족에 쓰기 값에 key:value이므로

@router.post('/create',status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create:question_schema.QuestionCreate,
                    db: Session=Depends(get_db),
                    current_user:User=Depends(get_current_user)):
    # 의존성주입먼저 해야함?
    question_crud.create_question(db=db,question_create=_question_create,user=current_user)

@router.put('/update',status_code=status.HTTP_204_NO_CONTENT)
def question_update(question_update:question_schema.QuestionUpdate,
                    db: Session=Depends(get_db),
                    currentuser:User=Depends(get_current_user)):
    db_question=question_crud.get_question(db,question_update.question_id)
    # 받아오는게없기때문에 question_id를 추가해서 받아오는거임 put이니까 갱신됨
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    if currentuser.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정x")
    question_crud.update_question(db=db,db_question=db_question,
                                  question_update=question_update)
    # router까지가야 스키마가 들어옴
@router.delete('/delete',status_code=status.HTTP_204_NO_CONTENT)
def question_delete(question_delete:question_schema.QuestionDelete,
                    db: Session=Depends(get_db),
                    current_user:User=Depends(get_current_user)):
    db_question=question_crud.get_question(db,question_id=question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='데이터x')
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='삭제권한x')
    question_crud.delete_question(db,db_question)    

@router.post('/vote',status_code=status.HTTP_204_NO_CONTENT)
def question_vote(question_vote:question_schema.QuesetionVote,
                  db: Session=Depends(get_db),
                  current_user:User=Depends(get_current_user)):
    db_question=question_crud.get_question(db,question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    question_crud.vote_question(db,db_question,current_user)
