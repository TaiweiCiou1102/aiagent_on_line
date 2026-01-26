# FastAPI 
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Header
import uvicorn

# Line Bot
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Environment
import os 
from dotenv import load_dotenv

# Agents 
# from nodes.agent0 import stream_agent_updates
from nodes.agent_with_mcp_tools import initialize_agent, stream_agent_updates

#============================== Code ==============================#

# Load environment variables
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")

# Line Bot API and Webhook Handler initialization
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# FastAPI app with lifespan event to initialize the agent
@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_agent()
    yield

app = FastAPI(lifespan=lifespan)

# Line Bot webhook endpoint
@app.post("/callback")
async def callback(request: Request):

    signature = request.headers.get("X-Line-Signature", "")
    
    body_bytes = await request.body()
    body = body_bytes.decode("utf-8")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"

# Line Bot event handler
@handler.add(MessageEvent, message=TextMessage)
def on_message(event: MessageEvent):

    resp = stream_agent_updates(event.message.text)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=resp)
    )
    
@app.get("/")
def index():
    return "<p>This endpoint is the webhook for Line Bot which developed by Taiwei Ciou.</p>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)