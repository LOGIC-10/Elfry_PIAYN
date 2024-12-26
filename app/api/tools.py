from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from ..services.tools_service import search, webscraper, calculate, create_calendar_event
from .schemas import CalendarEventRequest

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


@router.post("/create_calendar_event")
async def create_calendar_event_tool(request: CalendarEventRequest):
    """
    Asynchronously creates a calendar event with the specified parameters.
    
    Args:
        request (CalendarEventRequest): The calendar event details
    """
    result = await create_calendar_event(
        title=request.title,
        begin_time=request.begin_time,
        end_time=request.end_time,
        time_zone=request.time_zone,
        remind_time=request.remind_time,
        location=request.location,
        online_link=request.online_link,
        event_type=request.event_type,
        related_people=request.related_people,
        appendix=request.appendix,
        repeat=request.repeat,
        comment=request.comment,
        priority=request.priority
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result