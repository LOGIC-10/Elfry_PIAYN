import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Union
import asyncio
from urllib.parse import urlparse
from datetime import datetime

async def search(query: str) -> Dict[str, Any]:
    """Search implementation"""
    try:
        # Simulate async operation
        await asyncio.sleep(0.1)
        
        # Mock search results for now
        results = [
            {"title": f"Result 1 for {query}", "url": "https://example.com/1"},
            {"title": f"Result 2 for {query}", "url": "https://example.com/2"}
        ]
        return {"success": True, "results": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def webscraper(url: str) -> Dict[str, Any]:
    """Web scraper implementation"""
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL format")

        # Use aiohttp/httpx for real async implementation
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ""
        main_content = soup.find('main') or soup.find('body')
        content = main_content.get_text(strip=True)[:1000] if main_content else ""
        
        return {
            "success": True,
            "data": {
                "title": title,
                "content": content,
                "url": url
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def calculate(expression: str) -> Dict[str, Union[bool, str, float]]:
    """Calculator implementation"""
    try:
        # Validation
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
            
        if not expression.strip():
            raise ValueError("Expression cannot be empty")
            
        # Calculate
        result = float(eval(expression))  # Convert to float for consistent return type
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    
async def create_calendar_event(
    title: str,
    begin_time: str,
    end_time: str,
    time_zone: str,
    remind_time: str,
    location: str = "",
    online_link: str = "",
    event_type: str = "",
    related_people: list = None,
    appendix: list = None,
    repeat: dict = None,
    comment: str = "",
    priority: str = "normal"
) -> Dict[str, Any]:
    """Create a calendar event with the specified parameters"""
    try:
        # 转换时间格式为 "yyyy-MM-dd HH:mm:ss"
        def format_datetime(dt_str: str) -> str:
            # 尝试解析各种可能的时间格式
            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S']:
                try:
                    dt = datetime.strptime(dt_str, fmt)
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
            return dt_str  # 如果都解析失败，返回原字符串

        event = {
            "title": title,
            "begin_time": format_datetime(begin_time),
            "end_time": format_datetime(end_time),
            "time_zone": time_zone,
            "remind_time": format_datetime(remind_time),
            "location": location,
            "online_link": online_link,
            "type": event_type,
            "related_people": related_people or [],
            "appendix": appendix or [],
            "repeat": repeat or {
                "is_repeat": False,
                "begin_time": "",
                "end_time": "",
                "frequency": ""
            },
            "comment": comment,
            "priority": priority
        }
        return {"success": True, "event": event}
    except Exception as e:
        return {"success": False, "error": str(e)}