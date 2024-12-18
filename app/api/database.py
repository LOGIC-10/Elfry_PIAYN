from fastapi import APIRouter

router = APIRouter()

@router.get("/conversations")
async def get_conversations(user_id: int):
    # 返回指定用户的对话记录
    return {"conversations": []}

@router.get("/tools")
async def get_tools():
    # 返回注册的工具列表
    return {"tools": []}

@router.get("/users")
async def get_users():
    # 返回用户信息
    return {"users": []}

@router.post("/users")
async def create_user(username: str, phone: str):
    # 创建新用户
    return {"status": "User created"}
