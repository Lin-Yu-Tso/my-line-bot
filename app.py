from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 這裡改成你在 LINE Developers 取得的資訊
LINE_CHANNEL_ACCESS_TOKEN = "j5sT3QjD/hmRVu4hm++LhIvtX0pp/coS15i37jcl7NvLy1YeTzJMq8+FP5NWuxg77ikvTn++Gs/MXi/iJT1SPW7SwajLvELg5nbFPopRkf9ZOXGbpjdPNd0j9G2s7moBpkJn9LrVBke+8dYEjIktZgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "522bd756eb29e25d6c50985a8e4513a0"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=['GET'])
def home():
    return "✅ Line BOT Server 正常運行中！"

@app.route("/callback", methods=['POST'])
def callback():
    # 取得簽章
    signature = request.headers['X-Line-Signature']

    # 取得請求內容
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK', 200

# 當使用者傳訊息時，回覆相同內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 設定關鍵字回覆規則
    if any(word in user_msg for word in ["hello", "嗨", "你好", "こんにちは"]):
        reply_text = "Hi~ 你好！👋"

    elif any(word in user_msg for word in ["bye", "掰掰", "再見", "bye bye"]):
        reply_text = "掰掰，下次見！👋"

    else:
        reply_text = f"我還聽不懂{user_message}，請跟我爸爸說！"


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    print("🚀 Line BOT 伺服器啟動中，請用 http://127.0.0.1:5000 測試")
    app.run(host='0.0.0.0', port=5000)
