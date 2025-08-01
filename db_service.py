import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_keywords_from_db():
    try:
        response = supabase.table("keyword_rules").select("*").execute()
        if not response.data:
            return []
        return [{"keywords": [r["keyword"]], "reply": r["reply"]} for r in response.data]
    except Exception as e:
        print(f"❌ 資料庫讀取失敗：{e}")
        return []