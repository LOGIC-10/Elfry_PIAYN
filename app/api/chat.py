from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.chat_service import process_chat
from typing import Optional, List, Dict
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    user_id: int
    messages: List[Message]
    model_name: Optional[str] = "gpt-4o-mini"

router = APIRouter()

@router.post("/")
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
