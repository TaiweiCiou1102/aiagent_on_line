# import asyncio
# from typing import Optional
# from contextlib import AsyncExitStack

# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client

# class MCPClient:
#     def __init__(self):
#         self.session: Optional[ClientSession] = None
#         self.exit_stack = AsyncExitStack()

#     async def connect_to_server(self):
#         server_params = StdioServerParameters(
#             command = 'uv',
#             args= [

#             ]
#         )

from langchain_mcp_adapters.client import MultiServerMCPClient
mcp_client = MultiServerMCPClient(
    {
        "mytoolserver": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "src/aiagent_on_line/mcp_server.py"],
        }
    }
) 