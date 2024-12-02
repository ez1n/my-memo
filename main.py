import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# load .env
load_dotenv()
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

app = FastAPI()
templates = Jinja2Templates(directory='templates')

DATABASE_URL = "mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost:3307/my_memo_app"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Memo(Base):
    __tablename__ = 'memo'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(1000))

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
        
Base.metadata.create_all(bind = engine)

# 메모 생성
@app.post("/memos")
async def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    new_memo = Memo(title = memo.title, content = memo.content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return {"id": new_memo.id, "title": new_memo.title, "content": new_memo.content}

# 메모 조회
@app.get("/memos")
async def read_memo_list(db: Session = Depends(get_db)):
    memo_list = db.query(Memo).all()
    return memo_list

# 기존 라우트
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

@app.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}

