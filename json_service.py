import json
import os

# 讀取關鍵字對應檔案(json) -> 每次部屬時讀取 keywords.json
'''file_path = os.path.join(os.path.dirname(__file__), "keywords.json")

with open(file_path, "r", encoding="utf-8") as f:
    keyword_rules = json.load(f)

if not isinstance(keyword_rules, dict):
    print("⚠️ 讀取 keywords.json 失敗，資料不是 dict:", type(keyword_rules))
    keyword_rules = {}
else:
    print("✅ JSON 載入成功:", keyword_rules)
'''

def get_keywords_from_json():

    # 每次讀取server上最新的 keywords.json    
    file_path = os.path.join(os.path.dirname(__file__), "keywords.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            keyword_rules = json.load(f)
            if isinstance(keyword_rules, dict):
                return [{"keywords": v.get("keywords", []), "reply": v.get("reply", "")} for v in keyword_rules.values()]
            return keyword_rules
    except Exception as e:
        print(f"❌ 讀取 keywords.json 失敗：{e}")
        return []


    # 依據使用者傳來訊息，用程式判斷關鍵字來回覆
    '''if any(word in user_message for word in ["hello", "嗨", "你好", "こんにちは"]):
        reply_text = "Hi~ 你好！👋"

    elif any(word in user_message for word in ["bye", "掰掰", "再見", "bye bye"]):
        reply_text = "掰掰，下次見！👋"

    else:
        reply_text = f"我還聽不懂{user_message}，請跟我爸爸說！"
    '''
    # 依據使用者傳來訊息，根據keywords.json內容的關鍵字來回覆 (無模糊比對)
    '''for key, rule in keyword_rules.items():
        if isinstance(rule, dict) and "keywords" in rule and isinstance(rule["keywords"], list):
            if any(word in user_msg for word in rule["keywords"]):
                reply = rule.get("reply", "🤖 沒有定義回覆")
                break'''