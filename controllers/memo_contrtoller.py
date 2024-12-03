from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies import get_db
from models.memo_model import Memo, MemoCreate, MemoUpdate

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# 메모 생성
@router.post("/memo")
async def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    new_memo = Memo(title=memo.title, content=memo.content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return {"id": new_memo.id, "title": new_memo.title, "content": new_memo.content}


# 메모 조회
@router.get("/memos")
async def read_memo_list(request: Request, db: Session = Depends(get_db)):
    memo_list = db.query(Memo).all()
    return templates.TemplateResponse(
        "memos.html", {"request": request, "memos": memo_list}
    )


# 메모 수정
@router.put("/memo/{memo_id}")
async def update_memo(memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()

    if db_memo is None:
        return {"error": "메모가 존재하지 않습니다."}

    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None:
        db_memo.content = memo.content

    db.commit()
    db.refresh(db_memo)

    return {"id": db_memo.id, "title": db_memo.title, "content": db_memo.content}


# 메모 삭제
@router.delete("/memo/{memo_id}")
async def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()

    if db_memo is None:
        return {"error": "메모가 존재하지 않습니다."}

    db.delete(db_memo)
    db.commit()

    return {"message": "메모가 성공적으로 삭제되었습니다."}
