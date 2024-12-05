
import mimetypes

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
app=FastAPI()
origins=[
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory=r"C:\Users\User\fastapiworkspace\myapi\frontend\dist\assets"))
# router의 apirouter를통해 함수 해석후 fastapi에 리턴함
@app.get("/")
def index():
    return FileResponse(r"C:\Users\User\fastapiworkspace\myapi\frontend\dist\index.html")