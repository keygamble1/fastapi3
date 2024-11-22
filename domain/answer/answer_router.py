
from database import get_db
from domain.answer import answer_crud, answer_schema
from domain.answer.answer_schema import AnswerCreate
from domain.question import question_crud, question_schema
from domain.user.user_router import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from models import Question, User
from sqlalchemy.orm import Session
from starlette import status

router=APIRouter(
    prefix="/api/answer",
)

# status_code=status.HTTP_204_NO_CONTENT 이건 성공적인 응답/응답본문(body)가 없고,성공적으로 처리됨
# 수정 및 삭제했을시 서버가 응답본문을 안보낼때 마침 응답본문 오류가나오면 그건 틀린것 204=빈값
@router.post('/create/{question_id}',status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id:int,
                  _answer_create:AnswerCreate,
                  db:Session=Depends(get_db),
                  current_user:User=Depends(get_current_user)):
    # 스키마만 일치하면되므로 get_existing_user 여기에해당하는 usercreate만만족하면됨
    # User=db.query에서 User로 받아버리는거
    
    question=question_crud.get_question(db=db,question_id=question_id)
    if not question:
        raise HTTPException(status_code=404,detail="question not found")
    answer_crud.create_answer(db=db,question=question,answer_create=_answer_create,user=current_user)
    # 자료형을 매개변수선언만하는거)
#crud와 동일하게맞추기
# post는 새로운 리소스를생성
# put은 생성된 리소스를 갱신 수정하는거
# Depends는 예약어라고보자
@router.delete('/delete',status_code=status.HTTP_204_NO_CONTENT)
@router.delete('/delete',status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(answer_delete:answer_schema.AnswerDelete,
                    db: Session=Depends(get_db),
                    current_user:User=Depends(get_current_user)):
    db_answer=answer_crud.get_answer(db,answer_id=answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='데이터x')
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='삭제권한x')
    answer_crud.delete_answer(db,db_answer)    

@router.get('/detail/{answer_id}',response_model=answer_schema.Answer)
def answer_detail(answer_id:int,
                  db: Session=Depends(get_db)):
    answer=answer_crud.get_answer(db,answer_id)
    return answer
@router.put('/update',status_code=status.HTTP_204_NO_CONTENT)
def answer_update(answer_update:answer_schema.AnswerUpdate,
                    db: Session=Depends(get_db),
                    currentuser:User=Depends(get_current_user)):
    db_answer=answer_crud.get_answer(db,answer_update.answer_id)
    # 받아오는게없기때문에 answer_id를 추가해서 받아오는거임 put이니까 갱신됨
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    if currentuser.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정x")
    answer_crud.update_answer(db,db_answer,answer_update)
@router.post('/vote',status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(answer_vote:answer_schema.AnswerVote,
                  db: Session=Depends(get_db),
                  current_user:User=Depends(get_current_user)):
    db_answer=answer_crud.get_answer(db,answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터x")
    answer_crud.vote_answer(db,db_answer,current_user)