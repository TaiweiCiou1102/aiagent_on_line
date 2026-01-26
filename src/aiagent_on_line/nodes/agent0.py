from langchain.tools import tool
from tools.geoencoding import get_coordinates
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent

SYSTEM_PROMPT = """You are an AI assistant that can use tools to get information."""


# tools defining
@tool
def get_location_coordinates(address: str) -> str:
    """
    Get the latitude and longitude of a given address
    
    :param address: The address to inquire
    :type address: str
    :return: The results of inquiring the coordinates of the given address
    :rtype: str
    """
    lat, lng = get_coordinates(address)
    if lat is not None and lng is not None:
        return f"The coordinates of '{address}' are Latitude: {lat}, Longitude: {lng}."
    else:
        return f"Could not find coordinates for the address: '{address}'."

tools = [get_location_coordinates]

# model loading
load_dotenv()

model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    model=os.getenv("AZURE_OPENAI_MODEL"),
)

# Add memory
#checkpointer = InMemorySaver()

# agent building
agent = create_agent(
    model, 
    system_prompt = SYSTEM_PROMPT,
    tools = tools) 
    #checkpointer = checkpointer)

# agent invoke function
def stream_agent_updates(user_input: str):
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