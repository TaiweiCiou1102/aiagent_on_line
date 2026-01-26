from langchain.tools import tool
from tools.geoencoding import get_coordinates
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from mcp_client import mcp_client

SYSTEM_PROMPT = """You are an AI assistant that can use tools to get information."""

# model loading
load_dotenv()

model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    model=os.getenv("AZURE_OPENAI_MODEL"),
)

# agent building
agent = None

async def initialize_agent():
    global agent
    mcp_tools = await mcp_client.get_tools()
    tools = [mcp_tools['mytoolserver_get_coordinates']]
    agent = create_agent(
        model, 
        system_prompt = SYSTEM_PROMPT,
        tools = tools) 

# agent invoke function
def stream_agent_updates(user_input: str):
    if agent is None:
        return "Agent is initializing, please wait..."

    for chunk in agent.stream(
        {
            "messages":[
                {
                    "role":"user",
                    "content": user_input
                }
            ]
        },
        stream_mode = "updates"
    ):
        for step, data in chunk.items():
            
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")
            content = data['messages'][-1].content_blocks
            if step == 'model' and content[-1]['type'] == 'text':
                return content[-1]['text']