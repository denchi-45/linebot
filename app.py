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
import os

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 退出処理
    if event.message.text == "帰って":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("うっうっ"))

        #グループトークからの退出処理
        if hasattr(event.source,"group_id"):
            line_bot_api.leave_group(event.source.group_id)

        #ルームからの退出処理
        if hasattr(event.source,"room_id"):
            line_bot_api.leave_room(event.source.room_id)

        return
    
    elif event.message.text == "ごめんね":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("いいよ"))

    # オウム返し
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
    
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)