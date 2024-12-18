from fastapi import APIRouter, HTTPException
from ..services.tools_service import search, webscraper, calculate

# 移除 prefix，因为已经在 main.py 中定义了
router = APIRouter()

@router.get("/search")
async def search_tool(query: str):
    result = await search(query)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/webscraper") 
async def webscraper_tool(url: str):
    result = await webscraper(url)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/calculate")
async def calculate_tool(expression: str):
    result = await calculate(expression)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result