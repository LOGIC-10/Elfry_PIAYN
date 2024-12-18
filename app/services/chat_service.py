from openai import OpenAI
from sqlalchemy.orm import Session
from .database_service import get_model_config
from ..db.database import Conversation
from typing import List
from ..api.chat import Message

async def process_chat(db: Session, user_id: int, messages: List[Message], model_name: str = "gpt-4o-mini"):
    # Get model configuration
    model_config = get_model_config(db, model_name)
    if not model_config:
        raise ValueError(f"Model {model_name} not found or inactive")
    
    # Initialize OpenAI client with model-specific configuration
    client = OpenAI(
        api_key=model_config.api_key,
        base_url=model_config.base_url if model_config.base_url else None
    )

    # Format messages for OpenAI API
    formatted_messages = [msg.dict(exclude_none=True) for msg in messages]

    # Create chat completion
    completion = client.chat.completions.create(
        model=model_name,
        messages=formatted_messages
    )
    
    response = completion.choices[0].message

    # Store conversation
    conversation = Conversation(
        user_id=user_id,
        request_data={"messages": [msg.dict() for msg in messages], "model": model_name},
        response_data={"response": response.model_dump()}
    )
    db.add(conversation)
    db.commit()

    return response
