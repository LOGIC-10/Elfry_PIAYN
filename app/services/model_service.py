
from sqlalchemy.orm import Session
from ..db.database import ModelsAPI
from fastapi import HTTPException

async def get_model_credentials(db: Session, model_name: str, provider: str = None):
    query = db.query(ModelsAPI).filter(
        ModelsAPI.is_active == True,
        ModelsAPI.model_name == model_name
    )
    
    if provider:
        query = query.filter(ModelsAPI.provider == provider)
    
    model = query.first()
    
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"No active API key found for model {model_name}"
        )
    
    return {
        "api_key": model.api_key,
        "base_url": model.base_url,
        "config": model.config or {}
    }