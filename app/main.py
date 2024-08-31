import sys

from fastapi import Request, FastAPI, HTTPException

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import uvicorn
from .config import Settings
from .logger import Logger


setting = Settings()
logger = Logger().get()
# get channel_secret and channel_access_token from your environment variable
if setting.LINE_CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if setting.LINE_CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=setting.LINE_CHANNEL_ACCESS_TOKEN
)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
# INFO: WebhookParser should take channel_secret
parser = WebhookParser(channel_secret = setting.LINE_CHANNEL_SECRET)

@app.get("/")
async def root():
    return {"message": "Welcome to BOOJOOH's LINE Bot!"}

@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = await request.body()
    body = body.decode()
    logger.info(f'Request body: {body}')

    try:
        events = parser.parse(body, signature)
        if not isinstance(events, list):
            events = [events]
    except InvalidSignatureError:
        logger.debug('Invalid signature')
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        if not isinstance(event.reply_token, str ):
            continue

        reply_message_request = ReplyMessageRequest(
                # INFO: reply_token should not use alias
                replyToken=event.reply_token,
                messages=[TextMessage(text=event.message.text, quickReply=None, quoteToken=None)],
                # INFO: notificationDisabled should not use alias
                notificationDisabled=True
            )

        await line_bot_api.reply_message(reply_message_request)

    return 'OK'
