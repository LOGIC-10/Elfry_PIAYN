messages = [
    {'role': 'user', 'content': '法国总理现在是谁'}, 
    {'role': 'assistant', 'tool_calls': [
        {'function': {'arguments': '{"query":["法国总理现在是谁","当前法国总理","法国总理"]}', 'name': 'search'}, 
         'id': 'call_uXOaHdNeRnoILKtPvNtr0pYq', 'type': 'function'}]
    }, 
    {'role': 'tool', 
    'tool_call_id': 'call_uXOaHdNeRnoILKtPvNtr0pYq', 
    'name': 'search', 
    'content': '{\'法国总理现在是谁\': \'\\nQuery: 法国总理现在是谁\\nSearch Results:\\n--------------------------------------------------\\n[1]:\\nTITLE: 马克龙新任命总理终于来了，他是谁？_腾讯新闻\\nURL: https://news.qq.com/rain/a/20241214A01KDY00\\nCONTENT: 01 法国总统埃马纽埃尔-马克龙在一周时间内任命73岁的弗朗索瓦·贝鲁为新总理。 02 贝鲁曾多次为马蒂尼翁所提及，但从未被任命过，如今终于执掌 ...\\n--------------------------------------------------\\n法新社13日刊文称，现年73岁的贝鲁是法国民主运动党领导人。该党与马克龙 ...\\n--------------------------------------------------\'}'
    }
]

messages = [
    {
        'role': 'system',
        'content': '你可以使用工具调用tool call来获得结果、回答问题，但是一旦你使用工具调用，你必须在给出具体的参数的同时在content里面给出选择和使用这个工具的原因，必须要非常的清晰，具体和详细'
    },
    {
        'role': 'user', 
        'content': '这个表达式等于多少：45678651+22'
    }
]

tools = [{'type': 'function', 'function': {'name': 'search_tool', 'description': 'Performs an asynchronous search operation based on the provided query.', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'The search query string to be processed.'}}, 'required': ['query'], 'additionalProperties': False}}}, {'type': 'function', 'function': {'name': 'webscraper_tool', 'description': 'Asynchronously scrapes content from a given URL using the webscraper function.', 'parameters': {'type': 'object', 'properties': {'url': {'type': 'string', 'description': 'The target URL to scrape content from.'}}, 'required': ['url'], 'additionalProperties': False}}}, {'type': 'function', 'function': {'name': 'calculate_tool', 'description': 'Asynchronously calculates the result of a mathematical expression.\n\nThis function takes a mathematical expression as a string and processes it using the \ncalculate function. If the calculation fails, it raises an HTTP 400 error.', 'parameters': {'type': 'object', 'properties': {'expression': {'type': 'string', 'description': 'The mathematical expression to be calculated'}}, 'required': ['expression'], 'additionalProperties': False}}}]


from openai import OpenAI
import base64

image_path = "/Users/logic/Downloads/elf.png"
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')


def call_llm(messages, model="gpt-4o-mini", max_tokens=300, tools=[]):
    """
    Call LLM with support for text, images and tool calls
    Args:
        messages: List of message objects
        model: Model name to use
        max_tokens: Maximum tokens in response
    Returns:
        Response content from LLM
    """
    client = OpenAI(
        api_key="sk-g4dpUpPsZQcQjFp0B01165Ea87264e6eA521D33aC35b7aD2",
        base_url="https://toollearning.cn/v1/",
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            tools=tools
        )
        return response.choices[0].message
    except Exception as e:
        return str(e)
    

# Example usage:
# For text only:
result = call_llm(
    messages=messages,
    model="gpt-4o-mini",
    tools=tools
)
print(result)

# # For image:
# image_message = {
#     "role": "user", 
#     "content": [
#         {"type": "text", "text": "What's in this image?"},
#         {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}} # 这里传输的是图片的ascii编码
#     ]
# }
# print(type(base64_image))
# result = call_llm([image_message])
# print(result)



# stream call llm 

# def stream_openai_response(model="gpt-4o-mini", messages=messages, tools=tools):
#     client = OpenAI(
#         api_key="sk-g4dpUpPsZQcQjFp0B01165Ea87264e6eA521D33aC35b7aD2",
#         base_url="https://toollearning.cn/v1/",
#     )
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         tools=tools,
#         stream=True
#     )
    
#     for chunk in response:
#         # if chunk.choices[0].delta.content is not None:
#         yield chunk

# for chunk in stream_openai_response():
#     # print(chunk, end='', flush=True)
#     print(chunk)


# # choices[0].delta.content