import os
from supabase import create_client, Client
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_keywords_from_db():
    try:
        response = supabase.table("keyword_rules").select("*").execute()
        if not response.data:
            return []
        
        grouped = defaultdict(list)
        for r in response.data:
            grouped[r["reply"]].append(r["keyword"].strip().lower())
        
        return [{"keywords": words, "reply": reply} for reply, words in grouped.items()]
    except Exception as e:
        print(f"❌ 資料庫讀取失敗：{e}")
        return []