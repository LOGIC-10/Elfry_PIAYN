from fastapi import APIRouter
# ...existing code...
router = APIRouter()

@router.post("/")
async def get_embedding(query: str):
    # 调用 OpenAI TextEmbedding003 模型的逻辑
    return {"embedding": [0.1, 0.2, 0.3]}
