
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='sqlite:///./myapi.db'
# sqlite3데이터파일을 프로젝트루트디렉토리에저장
# ///=상대경로 ./db파일이 현재 디렉터리에 존재함을 의미 .은 현재데이터베이스를의미
# 절대는 루트부터 상대는 현재위치에서부터
engine=create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}
)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
# commit이되어야만 실제저장됨,커넥션풀 create_engine 커넥션풀을생성, 객체를 일정갯수마큼 만들고 돌려가며 사용
Base=declarative_base()
# 인덱스등 제약조건은 metadata클래스를이용해 써야함
# 없을경우 에러가나옴
# copy and move 전략쓰려면 render_as_batch써얗암
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata=MetaData(naming_convention=naming_convention)
def get_db():
    db=SessionLocal()
    try:
        yield db
        # 실행도중 멈추고 이걸 호출자에게 넘기고 호출자는 받아서 실행
        # 함수를 제네레이터로 바꾸고, 제네레이터는 값을 순차적으로 생성하는 함수,
        # get_db가멈추가 db를 건내준다 중간리턴후 돌아온다고보면됨 return은보통 끝에서끊기는데 이건
        # 중간 return급
        
    finally:
        # 실행이끝나면 db를 닫는것
        db.close()