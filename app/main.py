from fastapi import FastAPI
from app.api import tools, chat, embedding, database
from .services.tools_manager import ToolManager
from .db.database import SessionLocal

app = FastAPI(title="AI Assistant API")

app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(embedding.router, prefix="/embedding", tags=["embedding"])
app.include_router(database.router, prefix="/database", tags=["database"])

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        ToolManager.initialize_tools(db)
    finally:
        db.close()

# 这里如何实现统一的接口管理？比如启动和关闭