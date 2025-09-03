from pydantic import BaseModel, Field
class add(BaseModel):
    """ Add 2 integers"""
    a: int = Field(..., description="First int")
    b: int = Field(..., description="Second int")
    c: int = Field(..., description="Third int")
class multiply(BaseModel):
    """ Multiply 2 integers"""
    a: int = Field(..., description="First int")
    b: int = Field(..., description="Second int")
    c: int = Field(..., description="Third int")

class sub(BaseModel):
    """ Subtract  integers"""
    a: int = Field(..., description="First int")
    b: int = Field(..., description="Second int")
    c: int = Field(..., description="Third int")
tools = [add, multiply, sub]

import getpass
import os
apiKey = os.environ['MM_API']

from langchain.chat_models import init_chat_model
llm = init_chat_model("gpt-4o", model_provider="openai", api_key=apiKey)
llm_with_tools = llm.bind_tools(tools=tools)
query = "What is 15-15-2?"

ans = llm_with_tools.invoke(query)
if ans.tool_calls:
    for tool_call in ans.tool_calls:
        tool_name = tool_call['name']
        args = tool_call['args']
        if tool_name == "multiply":
            result = args['a'] * args['b'] * args["c"]
            print(f"Result: {result}")
        elif tool_name == "add":
            result = args['a'] + args['b'] + args['c']
            print(f"Result: {result}")
        elif tool_name == "sub":
            result = args['a'] - args['b'] - args['c']
            print(f"Result: {result}")
else:
    print(ans.content)
