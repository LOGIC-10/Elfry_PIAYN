from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.embedding_service import process_embedding
from pydantic import BaseModel

router = APIRouter()

class EmbeddingRequest(BaseModel):
    """
    Request model for text embedding
    """
    text: str
    model_name: str = "text-embedding-3-small"

@router.post("")
async def create_embedding(
    request: EmbeddingRequest,
    db: Session = Depends(get_db)
):
    """
    Creates embeddings for the given text using specified model
    
    Args:
        request (EmbeddingRequest): Contains text to embed and optional model name
        db (Session): Database session
    """
    try:
        result = await process_embedding(
            db=db,
            text=request.text,
            model_name=request.model_name
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

