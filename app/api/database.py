from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from ..db.database import get_db, User, Tool, Conversation, ModelsAPI

router = APIRouter()

@router.get("/conversations")
async def get_conversations(user_id: int, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    return {"conversations": conversations}

@router.get("/tools")
async def get_tools(db: Session = Depends(get_db)):
    tools = db.query(Tool).all()
    return {"tools": tools}

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

@router.post("/users")
async def create_user(username: str, phone: str, db: Session = Depends(get_db)):
    user = User(username=username, phone=phone)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or phone already exists")
    return {"status": "User created", "user": user}

@router.get("/models")
async def get_models(db: Session = Depends(get_db)):
    models = db.query(ModelsAPI).filter(ModelsAPI.is_active == True).all()
    return {"models": models}

@router.post("/models")
async def create_model(
    model_name: str,
    provider: str,
    api_key: str,
    base_url: Optional[str] = None,
    expire_time: Optional[datetime] = None,
    config: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    model = ModelsAPI(
        model_name=model_name,
        provider=provider,
        api_key=api_key,
        base_url=base_url,
        expire_time=expire_time,
        config=config
    )
    db.add(model)
    try:
        db.commit()
        db.refresh(model)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating model API entry")
    return {"status": "Model API created", "model": model}

@router.put("/models/{model_id}")
async def update_model(
    model_id: int,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    expire_time: Optional[datetime] = None,
    is_active: Optional[bool] = None,
    config: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    model = db.query(ModelsAPI).filter(ModelsAPI.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
        
    if api_key: model.api_key = api_key
    if base_url: model.base_url = base_url
    if expire_time: model.expire_time = expire_time
    if is_active is not None: model.is_active = is_active
    if config: model.config = config
    
    try:
        db.commit()
        db.refresh(model)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating model API entry")
    return {"status": "Model API updated", "model": model}
