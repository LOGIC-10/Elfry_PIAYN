from fastapi import FastAPI
from app.api import tools, chat, embedding, database

app = FastAPI(title="My API") # 这里请你修改合适的title

app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(embedding.router, prefix="/embedding", tags=["embedding"])
app.include_router(database.router, prefix="/database", tags=["database"])

# 这里如何实现统一的接口管理？比如启动和关闭