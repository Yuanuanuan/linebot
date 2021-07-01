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

line_bot_api = LineBotApi('tYoNPQqtlhF3G2rhnsnR5JoHyL7QHqVmJ5+zhJ4SmXzK7pf4vDqfMwbMRkDuf9y1PQ7XbF/i/GqeKJIPzc2CK1x2csJzFUq5ljeObcp3QJq3pJ87Fklv0kk/yKmak+BlIFodfzU2YVFraTAOsTsABQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a9e4c808052f082de1104abf8aaa6dca')


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