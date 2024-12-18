from fastapi import APIRouter, HTTPException
from ..services.tools_service import search, webscraper, calculate

# 移除 prefix，因为已经在 main.py 中定义了
router = APIRouter()

@router.get("/search")
async def search_tool(query: str):
    """
    Performs an asynchronous search operation based on the provided query.

    Args:
        query (str): The search query string to be processed.
    """
    result = await search(query)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/webscraper") 
async def webscraper_tool(url: str):
    """
    Asynchronously scrapes content from a given URL using the webscraper function.

    Args:
        url (str): The target URL to scrape content from.
    """
    result = await webscraper(url)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/calculate")
async def calculate_tool(expression: str):
    """
    Asynchronously calculates the result of a mathematical expression.

    This function takes a mathematical expression as a string and processes it using the 
    calculate function. If the calculation fails, it raises an HTTP 400 error.

    Args:
        expression (str): The mathematical expression to be calculated
    """
    result = await calculate(expression)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result