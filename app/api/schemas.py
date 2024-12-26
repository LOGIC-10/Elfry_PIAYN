from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime

class Message(BaseModel):
    """A Pydantic model representing a message in a conversation.

    This schema is typically used for handling message structures in API communications,
    particularly in chat-like interfaces or AI conversations.

    Attributes:
        role (str): The role of the message sender (e.g., 'user', 'assistant', 'system')
        content (str): The actual text content of the message
        tool_calls (List[Dict], optional): List of tool call objects if any tools were called
        tool_call_id (str, optional): Identifier for a specific tool call
        name (str, optional): Name identifier for the message sender

    Example:
        {
            "role": "user",
            "content": "Hello, how are you?",
            "tool_calls": None,
            "tool_call_id": None,
            "name": "John"
        }
    """
    role: str
    content: str
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    """
    A Pydantic model representing a chat request schema for API validation and data parsing.

    This schema defines the structure of incoming chat requests, validating that:
    - Each request must have a user identifier
    - Contains a list of chat messages
    - Optionally specifies a model name (defaults to "gpt-4o-mini")

    Attributes:
        user_id (int): The unique identifier of the user making the request
        messages (List[Message]): A list of Message objects containing the chat history
        model_name (Optional[str]): The name of the model to be used for chat completion,
                                   defaults to "gpt-4o-mini" if not specified

    Schema用途:
    1. 数据验证：确保请求数据符合预期格式
    2. 类型检查：强制要求正确的数据类型
    3. API文档：自动生成OpenAPI/Swagger文档
    4. 请求解析：自动将JSON请求体解析为Python对象
    """
    user_id: int
    messages: List[Message]
    model_name: Optional[str] = "gpt-4o-mini"

class ToolCreate(BaseModel):
    name: str = Field(..., max_length=255)
    return_char_limit: int = Field(default=6000)
    description: str
    tags: List[str] = Field(default_factory=lambda: ["base"])
    source_type: Optional[str]
    json_schema: Dict
    source_code: Optional[str]

class ToolResponse(ToolCreate):
    id: int
    create_time: datetime
    updated_at: datetime
    is_deleted: bool = False

    class Config:
        from_attributes = True

class CalendarEventRequest(BaseModel):
    """
    A Pydantic model representing a calendar event creation request.

    Attributes:
        title (str): Event title
        begin_time (str): Event start time
        end_time (str): Event end time
        time_zone (str): Event timezone
        remind_time (str): Reminder time
        location (str, optional): Event location
        online_link (str, optional): Online meeting link
        event_type (str, optional): Type of event
        related_people (List[str], optional): List of people related to the event
        appendix (List[str], optional): List of appendices
        repeat (Dict, optional): Event repetition settings
        comment (str, optional): Event comments
        priority (str, optional): Event priority level
    All datetime strings must be in format 'yyyy-MM-dd HH:mm:ss'
    """
    title: str
    begin_time: str
    end_time: str
    time_zone: str
    remind_time: str
    location: str = ""
    online_link: str = ""
    event_type: str = ""
    related_people: Optional[List[str]] = None
    appendix: Optional[List[str]] = None
    repeat: Optional[Dict] = None
    comment: str = ""
    priority: str = "normal"

    @validator('begin_time', 'end_time', 'remind_time')
    def validate_datetime_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            return v
        except ValueError:
            raise ValueError('Datetime must be in format yyyy-MM-dd HH:mm:ss')