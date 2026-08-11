import boto3
import json
import sys
import os
import asyncio

sys.path.append(os.path.abspath("../mcp-server"))
from server import mcp as enterprise_mcp_server
from fastmcp import Client

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

def run_agent_workflow(user_prompt: str, messages: list):
    messages.append({"role": "user", "content": [{"text": user_prompt}]})
    
    tool_config = {
        "tools": [{
            "toolSpec": {
                "name": "search_internal_docs",
                "description": "Retrieve information from enterprise technical documentation.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            }
        }]
    }

    print(f"\nUser: {user_prompt}")
    
    response = bedrock_client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=messages,
        toolConfig=tool_config
    )
    
    message = response.get("output", {}).get("message", {})
    messages.append(message)
    
    tool_use_block = None
    for content_block in message.get("content", []):
        if "toolUse" in content_block:
            tool_use_block = content_block["toolUse"]
            break
            
    if tool_use_block:
        tool_name = tool_use_block["name"]
        tool_args = tool_use_block["input"]
        tool_use_id = tool_use_block["toolUseId"]
        
        print(f"[Agent executing MCP tool '{tool_name}' with args: {tool_args}]")
        
        client = Client(enterprise_mcp_server)
        
        async def call_tool_async():
            async with client:
                result = await client.call_tool(tool_name, tool_args)
                if isinstance(result, str):
                    return result
                if hasattr(result, 'content') and result.content:
                    return result.content[0].text
                if hasattr(result, 'data') and result.data:
                    return str(result.data)
                return str(result)

        tool_output = asyncio.run(call_tool_async())
        
        tool_result_message = {
            "role": "user",
            "content": [{
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": [{"json": {"result": tool_output}}]
                }
            }]
        }
        messages.append(tool_result_message)
        
        final_response = bedrock_client.converse(
            modelId="us.amazon.nova-lite-v1:0",
            messages=messages,
            toolConfig=tool_config
        )
        
        final_message = final_response.get("output", {}).get("message", {})
        messages.append(final_message)
        
        print("\nAssistant:")
        for block in final_message.get("content", []):
            if "text" in block:
                print(block["text"])
    else:
        print("\nAssistant:")
        for block in message.get("content", []):
            if "text" in block:
                print(block["text"])

def interactive_chat():
    messages = []
    print("=== Enterprise RAG MCP Agent Initialized ===")
    print("Type your questions below. Type 'exit' or 'quit' to end the session.\n")
    
    while True:
        try:
            user_input = input(">> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            run_agent_workflow(user_input, messages)
            print("-" * 50)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    interactive_chat()