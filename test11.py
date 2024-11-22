from curses.ascii import US
from datetime import datetime

from models import Answer, Question, User
from sqlalchemy import outerjoin

q=Question(subject='pybo가뭔가?',content="pybo에대해 알고싶다",create_date=datetime.now())
from database import SessionLocal

db=SessionLocal()
q=Question(subject='fastapi질문',content='id자동생성?',create_date=datetime.now())
db.add(q)
db.commit()
db.query(Question).all()
db.query(Question).get(1)
# get은 1건만리턴 filter는 여러개
db.query(Question).filter(Question.subject.ilike('%fastapi%')).all()
q=db.query(Question).get(2)
db.commit()
q=db.query(Question).get(1)
db.delete(q)
db.commit()
q=db.query(Question).get(2)
a=Answer(question=q,content='네 자동으로생성',create_date=datetime.now())
from datetime import datetime

# a생성했다고끝이아니고 add후 commit까지해야 db에 적용되는것
from database import SessionLocal
from models import Question

db=SessionLocal()
for i in range(300):
    q=Question(subject='테스트데이터[%03d]' % i ,content='내용무[%03d]' %i,
               create_date=datetime.now())
    db.add(q)
db.commit()
from database import SessionLocal
from models import Answer, Question

db=SessionLocal()
db.query(Question).count()
# Question
db.query(Answer).count()
# Question과 Answer교집합 대신 Question만삭제되고 남ㄴ아있는 answer있음
db.query(Question).join(Answer).count()
db.query(Question).outerjoin(Answer).count()
db.query(Question).outerjoin(Answer).filter(
    Question.content.ilike('%파이썬%') |
    Answer.content.ilike('%파이썬%')).distinct()
    # 테이블이 두개기때문에쓰는거가능
# Question모델과 연결된 다른모델 검색시 Answer,User를 아우터조인해야함
# 모델자체 사용하는거보다 모델을 묶어서 Question에서 outerjoin하는게편할듯
# Question에서 join하는거라 quesiton_id넣는거
subquery=db.query(Answer.question_id,Answer.content,User.username)\
.outerjoin(User,Answer.user_id==User.id).subquery()
    # relationship배제할거 User가 Answer을 조회못하게하는것
db.query(Question).outerjoin(subquery,subquery.c.question_id==Question.id) \
    .filter(subquery.c.content.ilike('%파이썬%') |
            subquery.c.username.ilike('$파이썬')
            ).distinct().count()
    # Answer과 Question은 교집합이라 Quiestion이있는 Answer+
# 모든 Question을 넣은 Question 
# 해서 Question+Answer과 같다
# db.query(Question).outerjoin(Answer).count().distinct()해서
# 왼쪽 Outerjoin되어있는 question 1개만필요하므로 distinct() 왼쪽데이터를 한다
# sqlalchemy에서 정의한대로함
# Question 왼쪽 Answer 오른쪽
# 그냥 조건을 넣어버리면 그건 sqlalchemy relationship을 배제함
# relationship은 join으로 자동으로 연관짓게만드는거임원래
# outerjoin은 기본적으로 left조인임

# 이럴경우 질문+답변있는것만 출력

# Question+Answer다 포함한것만 남아있음
# 즉 Answer이 없는 Question만 얻어와라
# Answer이 0인건 제외됨
# Question 과 Answer을 조인시 검색하는건
# Question에도 조건 'ㅇㅇ'과 answer에도 'ㅇㅇ'
# 이 있는것만 filter가능
# 내가원하는건 question ㅇㅇ 
# question에는 ㅇㅇ이없지만 answer에 ㅇㅇ 이있는거


