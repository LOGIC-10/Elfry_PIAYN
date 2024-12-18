
from pydantic import BaseModel
from typing import Optional, List, Dict

class Message(BaseModel):
    role: str
    content: str
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    user_id: int
    messages: List[Message]
    model_name: Optional[str] = "gpt-4o-mini"