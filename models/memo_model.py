from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database import Base


class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(1000))


class MemoCreate(BaseModel):
    title: str
    content: str


class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
