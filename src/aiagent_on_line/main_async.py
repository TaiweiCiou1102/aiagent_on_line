# FastAPI 
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Header
import uvicorn

# Line Bot
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

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
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
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
@handler.add(MessageEvent, message=TextMessageContent)
def on_message(event: MessageEvent):

    resp = stream_agent_updates(event.message.text)
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=resp)]
            )
        )
    
@app.get("/")
def index():
    return "<p>This endpoint is the webhook for Line Bot which developed by Taiwei Ciou.</p>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)