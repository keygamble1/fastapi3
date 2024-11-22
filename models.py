
from database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

# 둘다 프라이머리키므로 한번에 한개만가능
question_voter=Table(
'question_voter',
     Base.metadata,
    Column('user_id',Integer,ForeignKey('user.id'),primary_key=True),
    #  user.id 각각 한개씩가져옴
    Column('question_id',Integer,ForeignKey('question.id'),primary_key=True)
)
answer_voter=Table(
'answer_voter',
     Base.metadata,
    Column('user_id',Integer,ForeignKey('user.id'),primary_key=True),
    #  user.id 각각 한개씩가져옴
    Column('answer_id',Integer,ForeignKey('answer.id'),primary_key=True)
)
class User(Base):
    __tablename__ ="user"
    # 다 1개씩만등록 여러개조회는 backref로 안보임
    id=Column(Integer,primary_key=True)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    # BACKREF로 questions를 갖져옴
    # backref로 answers를 가져옴
class Question(Base):
    __tablename__ ="question"
    modify_date=Column(DateTime,nullable=True)
    id=Column(Integer,primary_key=True)
    subject=Column(String,nullable=False)
    content=Column(String,nullable=False)
    create_date=Column(DateTime,nullable=False)
    # BACKREF로 ANSERS를 가져옴
    # 1개만가져옴
    user_id=Column(Integer,ForeignKey("user.id"),nullable=True)
    
    # question에서 user.id접속
    # question에서 여러개의 users를 얻기
    # 1개만가져옴
    user=relationship("User",backref="question_users")
    voter=relationship('User',secondary=question_voter,backref='question_voter')
    # secondary로하면 이제 다대다라서 단일은아니며,
    # Question.voter를 통해 여러개의 user, User는 User.quesiton_voter로 가능함
    # 
    # user에서도 조회가능하지만 User에서는 쿼리를 한후에 보이기때문에 쿼리한후
    # 단 question을 조회하는것
    # backref는 서로를 통함 이제 user에서 question_id만맞으면 얻을수있음
    # 기본적으로 nullable은 true false로하는게나음

class Answer(Base):
    __tablename__ ="answer"
    modify_date=Column(DateTime,nullable=True)
    id=Column(Integer,primary_key=True)
    content=Column(String,nullable=False)
    create_date=Column(DateTime,nullable=False)
    question_id=Column(Integer,ForeignKey('question.id'))
    # answer에서는 question_id를 가져오고
    # question_id에 해당하는 
    # question.id=Question모델의 id와같다
    # 나중에 Question.id==answer.qusetion_id 이런게나올수있음
    # answer에 해당하는 question을 가져오라단일 quseiton
    question=relationship("Question",backref="answers")
    user_id=Column(Integer,ForeignKey('user.id'),nullable=True)
    user=relationship("User",backref='answer_users')
    voter=relationship('User',secondary=answer_voter,backref='answer_voter')
    # 하지만 Question에서는 answers를 다 가져올수있음
    # answre에서 모든 question조회하고 questionㄴ도 answer을 조회가능하다
    # question에서는 answer이라는게 없기때문에 단일 answer를 조회함
    # 모든 answer을 등록한 question모음들을 가져오는거
    # 나중에 Quesetion.answers를해서 answers의 여러 리스트들을 가져오는게가능
    # revision은 .py를제외한 fed239025과같은 버전번호를 가리킴 리비져ㄴ은 autogenerate수행시 무작위만들어짐
    # 리비젼파일은 테이블생성 or 변경하는 실행문들이 들어있다