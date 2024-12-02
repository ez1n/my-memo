from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database import Base, engine
from memo_contrtoller import router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)


# 기존 라우트
@app.get("/")
async def read_root():
    return RedirectResponse(url="/memos")
