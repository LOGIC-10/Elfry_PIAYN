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

def convert_chunk_to_json(chunk): return {"id": chunk.id, "object": chunk.object, "created": chunk.created, "model": chunk.model, "system_fingerprint": chunk.system_fingerprint, "choices": [{"index": choice.index, "delta": choice.delta.dict() if choice.delta else {}, "logprobs": choice.logprobs, "finish_reason": choice.finish_reason} for choice in chunk.choices]}

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
    
    def serialize_tool_call(tool_call):
        return {
            "id": tool_call.id,
            "type": tool_call.type,
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }
        }
    
    final_content = ""  # 用于收集完整响应
    
    while True:
        print(formatted_messages)
        completion = client.chat.completions.create(
            model=model_name,
            messages=formatted_messages,
            tools=available_tools,
            stream=True  # 启用流式响应
        )
        
        # 初始化变量
        full_content = ""
        function_name = None
        function_args = ""
        tool_calls_list = [] # 应对并行工具调用，建立一个id，工具名字、工具参数、type的映射存储列表

        # 处理流式响应
        for chunk in completion:
            delta = chunk.choices[0].delta
            # from IPython import embed; embed()
            # print("delta:", delta)
            # print("chunk.choices[0]:\n", chunk.choices[0])
            # 处理工具调用信息
            if delta.tool_calls:
                print("delta.tool_calls:", delta.tool_calls)
                tool_call = delta.tool_calls[0]
                if tool_call.function:
                    if tool_call.function.name and tool_call.id: # 注意流式输出只有第一个token带有工具的名字（如果并行tool_calls的话有被覆盖的风险）。这两个属性同时出现的时候代表一个新的工具调用开始

                        print(f"\n\nDetecting tool call, the id is {tool_call.id} and the function name is {tool_call.function.name}\n\n")

                        function_name = tool_call.function.name # 这是每个工具specific的
                        tool_call_id = tool_call.id # 这也是每个工具specific的
                        tool_call_type = tool_call.type # 这里默认基本都是 function
                        tool_call_dict = {
                            "id": tool_call_id,
                            "type": tool_call_type,
                            "function": {
                                "name": function_name,
                                "arguments": '' # 这里先留空，因为是流式输出，还没有接受完整
                            }
                        }
                    if tool_call.function.arguments:
                        function_args += tool_call.function.arguments
                        print(function_args)
                        
            # elif delta.content: # 如果没有工具调用，就是处理正常的对话内容
            else: # 如果没有工具调用，就是处理正常的对话内容
                if delta.content == None:
                    yield_result = json.dumps(convert_chunk_to_json(chunk),ensure_ascii=False)
                    yield "data: "+str(yield_result)
                else:
                    content_chunk = delta.content
                    full_content += content_chunk

                yield_result = json.dumps(convert_chunk_to_json(chunk),ensure_ascii=False)
                print("yield_result:\n", yield_result)
                yield "data: "+str(yield_result)
                # print("chunk:\n", chunk)
                # yield chunk

            # Move the finish_reason check here, outside the delta.tool_calls block
            print("chunk.choices[0].finish_reason:", chunk.choices[0].finish_reason)
            if chunk.choices[0].finish_reason == "tool_calls":

                print(f"\n\nCurrent Tool call finished...the id is {tool_call_id} and the function name is {function_name}\n\n")
                tool_call_dict["function"]["arguments"] = function_args
                tool_calls_list.append(tool_call_dict)

        # 检查是否有工具名称
        if tool_calls_list:
            print("tool_calls_list detected:", tool_calls_list)
            # 添加工具调用信息到消息列表
            formatted_messages.append({
                "role": "assistant",
                "tool_calls": tool_calls_list
            })

            for tool_call_dict in tool_calls_list:
                function_name = tool_call_dict["function"]["name"]
                function_args = tool_call_dict["function"]["arguments"]
                method_args_dict = json.loads(function_args)

                # 执行工具函数
                tool_method = ToolManager.get_tool(function_name)
                if tool_method:
                    try:
                        method_result = await tool_method(**method_args_dict)

                        print("method_resultz:", method_result)
                        # 将工具结果添加到消息列表
                        formatted_messages.append({ # 这里记录的是 tool 的执行结果
                            "role": "tool",
                            "tool_call_id": tool_call_dict["id"],
                            "name": function_name,
                            "content": str(method_result)
                        })

                    except Exception as e:
                        formatted_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_dict["id"],
                            "name": function_name,
                            "content": f"Error: {str(e)}"
                        })
                else:
                    # 工具未找到
                    formatted_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call_dict["id"],
                        "name": function_name,
                        "content": f"Error: Tool '{function_name}' not found"
                    })


        else:
            # 没有工具调用，添加完整的对话响应内容
            formatted_messages.append({
                "role": "assistant",
                "content": full_content
            })
            break  # 结束循环

    # 确保 response 和 formatted_messages 中的所有对象都是可序列化的
    serializable_response = full_content
    serializable_formatted_messages = formatted_messages  # 已经在上面序列化过

    # Store final conversation with all messages
    conversation = Conversation(
        user_id=user_id,
        request_data={"messages": [msg.dict() for msg in messages], "model": model_name},
        response_data={
            "response": serializable_response,  
            "messages": serializable_formatted_messages  # 包含了完整的消息历史
        }
    )
    db.add(conversation)
    db.commit()

    # 删除 return 语句，因为这是一个生成器函数
