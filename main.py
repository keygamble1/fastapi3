
from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

app=FastAPI()
origins=[
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))
@app.middleware("http")
async def override_static_file_mime(request,call_next):
  if request.url.path.startswith('/assets') and request.url.path.endswith(".js"):
      response=await call_next(request)
      response.header["content-type"]="application/javascript"
      return response
  return await call_next(request)

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")