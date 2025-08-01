import json
import os
import difflib
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from json_service import get_keywords_from_json
from db_service import get_keywords_from_db
# from supabase import create_client, Client

app = Flask(__name__)

# LINE Developers 取得的資訊
LINE_CHANNEL_ACCESS_TOKEN = "j5sT3QjD/hmRVu4hm++LhIvtX0pp/coS15i37jcl7NvLy1YeTzJMq8+FP5NWuxg77ikvTn++Gs/MXi/iJT1SPW7SwajLvELg5nbFPopRkf9ZOXGbpjdPNd0j9G2s7moBpkJn9LrVBke+8dYEjIktZgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "522bd756eb29e25d6c50985a8e4513a0"
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 讀取環境變數 -> 為了資料庫連線
load_dotenv()

# 首頁檢查(get)
@app.route("/", methods=['GET'])
def home():
    return "✅ Line BOT Server 正常運行中！"

# 使用 JSON 檔案的 callback
@app.route("/callback_json", methods=['POST'])
def callback_json():
    return handle_callback(use_json=True)

# 使用 Supabase DB 的 callback
@app.route("/callback_db", methods=['POST'])
def callback_db():
    return handle_callback(use_json=False)

def handle_callback(use_json=False):
    # 取得簽章
    signature = request.headers['X-Line-Signature']
    # 取得請求內容
    body = request.get_data(as_text=True)
    # 先暫存到 request context
    request.environ['USE_JSON'] = use_json  

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK', 200

# 🔹處理訊息 -> 當使用者傳訊息時，回覆邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 使用者傳來的訊息
    # 確認訊息類型為文字
    user_msg = event.message.text.strip().lower()
    #先定義回覆內容參數為 None
    reply = None

    # 在server上印出收到的訊息
    print(f"📩 收到訊息: {user_msg}")

    # 設定模糊匹配的 相似度閾值
    SIMILARITY_THRESHOLD = 0.6

    # 根據 route 判斷來源    
    use_json = request.environ.get('USE_JSON', False)
    keyword_rules = get_keywords_from_json() if use_json else get_keywords_from_db()

    # 模糊比對
    for rule in keyword_rules:
        keywords = rule["keywords"] if isinstance(rule["keywords"], list) else [rule["keyword"]]
        for word in keywords:
            similarity = difflib.SequenceMatcher(None, user_msg, word.lower()).ratio()
            if similarity >= SIMILARITY_THRESHOLD or word in user_msg:
                reply = rule.get("reply", "🤖 沒有定義回覆")
                break
        if reply:
            break

    if not reply:
        reply = f"我還聽不懂「{user_msg}」，請跟我爸爸說！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    print("🚀 Line BOT 伺服器啟動中，請用 http://127.0.0.1:5000 測試")
    app.run(host='0.0.0.0', port=5000)


# 讀取server上的 keywords.json 檔案
'''@app.route("/callback", methods=['POST'])
def callback():
    # 取得簽章
    signature = request.headers['X-Line-Signature']

    # 取得請求內容
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK', 200'''

# 讀取 Supabase keywords 資料表
'''@app.route("/keywords", methods=['GET'])
def get_keywords():
    try:
        response = supabase.table("keyword_rules").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

# 測試 Supabase 連線
'''@app.route("/test_connection", methods=['GET'])
def test_connection():
    try:
        response = supabase.table("keyword_rules").select("id").limit(1).execute()
        return jsonify({"project_url": SUPABASE_URL, "rows": len(response.data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''