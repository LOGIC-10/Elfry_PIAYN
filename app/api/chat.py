from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.chat_service import process_chat
from .schemas import ChatRequest

router = APIRouter()

# 修改路由路径，使用明确的路径
@router.post("")  # 或者使用 "/"
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        response = await process_chat(
            db=db, 
            user_id=request.user_id,
            messages=request.messages,
            model_name=request.model_name
        )
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
