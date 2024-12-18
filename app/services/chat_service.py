import json
import logging
from openai import OpenAI
from sqlalchemy.orm import Session
from .database_service import get_model_config
from ..db.database import Conversation
from typing import List, Dict, Any
from ..api.schemas import Message
from .tools_service import search, webscraper, calculate
from .tools_manager import ToolManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def colorize_message(msg: str, color: str) -> str:
    colors = {
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    return f"{colors.get(color, '')}{msg}{colors['end']}"

async def process_chat(db: Session, user_id: int, messages: List[Message], model_name: str = "gpt-4o-mini"):
    # Get model configuration
    model_config = get_model_config(db, model_name)
    if not model_config:
        raise ValueError(f"Model {model_name} not found or inactive")
    
    client = OpenAI(
        api_key=model_config.api_key,
        base_url=model_config.base_url if model_config.base_url else None
    )

    # Get available tools and their schemas
    available_tools = ToolManager.get_all_schemas() 

    # Create chat completion with tools
    formatted_messages = [msg.dict(exclude_none=True) for msg in messages]
    
    while True:
        completion = client.chat.completions.create(
            model=model_name,
            messages=formatted_messages,
            tools=available_tools
        )
        
        response = completion.choices[0].message
        logger.info(f"\n\nModel response: {response.content}")  

        # 先将模型的响应添加到消息列表中
        formatted_messages.append({
            "role": "assistant",
            "content": response.content if response.content else None,
            "tool_calls": response.tool_calls if response.tool_calls else None
        })
        
        # If no tool calls, break the loop
        if not response.tool_calls:
            break

        # Process tool calls
        for tool_call in response.tool_calls:
            logger.info(f"Processing tool call: {tool_call.function.name}")
            method_name = tool_call.function.name
            method_args = tool_call.function.arguments
            method_args_dict = json.loads(method_args)

            # Execute tool if available
            tool_method = ToolManager.get_tool(method_name) # 请注意这里是直接调用了端点函数endpoint
            ## 解释上面直接调用端点函数
            # 绕过了 FastAPI 的路由系统，跳过了 HTTP 请求/响应周期，没有经过 FastAPI 的中间件处理(如认证、错误处理等)，执行速度更快(因为少了网络请求开销)，直接在内存中操作，使用同一个进程
            # TODO 但是注意：如果将来需要添加通用的请求处理逻辑(如认证、日志等)，直接调用可能会绕过这些重要的处理步骤。

            if tool_method:
                try:
                    method_result = await tool_method(**method_args_dict)
                    logger.info(f"Tool {tool_call.function.name} execution result: {method_result}")
                    
                    # Add tool execution result to messages
                    formatted_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": method_name,
                        "content": str(method_result)
                    })
                    
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    formatted_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": method_name,
                        "content": f"Error: {str(e)}"
                    })

    # Store final conversation with all messages
    conversation = Conversation(
        user_id=user_id,
        request_data={"messages": [msg.dict() for msg in messages], "model": model_name},
        response_data={
            "response": response.model_dump(),
            "messages": formatted_messages  # Store all messages including tool interactions
        }
    )
    db.add(conversation)
    db.commit()

    return {"content": response.content}
