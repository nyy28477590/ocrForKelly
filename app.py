from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('/Br5l3h+vNfOduKH/QH9nI5Y5NqWVEFkiwmU0s87Hza4fLNlv4J70JeL/ZVGGekBxDFIBbSjyAGG3buejv2k/pvE0zKNRS3wOlmUN+OryTjmy/VZ1ubRbxjHtnPQDmMrv/gAICbNK22UuJjyawcdpAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4105cd88b0dd3514856ab40be453d06f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()