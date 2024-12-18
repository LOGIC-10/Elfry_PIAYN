from fastapi import FastAPI
from app.api import tools, chat, embedding, database
from .services.tools_manager import ToolManager
from .db.database import SessionLocal
import uvicorn

app = FastAPI(title="AI Assistant API")

app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(embedding.router, prefix="/embedding", tags=["embedding"])
app.include_router(database.router, prefix="/database", tags=["database"])

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        # 每次启动服务的时候，初始化工具
        ToolManager.initialize_tools(db) # 现在所有的工具schema都在ToolManager._schemas中
        print("Available tools:", ToolManager.get_available_tools())
        print("\nAll schemas:", ToolManager.get_all_schemas())
        print("\n\n\n_tools:", ToolManager._tools)
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("app.main:app",
                host="0.0.0.0", 
                port=8000,
                reload=True,           # 启用热重载
                reload_dirs=["app"])   # 监视 app 目录下的文件变化