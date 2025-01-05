from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.chat_service import process_chat
from .schemas import ChatRequest
import uvicorn

router = APIRouter()

@router.post("/")  # 改为明确的斜杠
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        # 将响应转换为 StreamingResponse
        return StreamingResponse(
            process_chat( 
                db=db,
                user_id=request.user_id,
                messages=request.messages,
                model_name=request.model_name
            ),
            media_type="text/event-stream"
        )
        # return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.api.chat:router", host="0.0.0.0", port=8016, reload=True)