import streamlit as st
import subprocess
import json
import requests
import random
from datetime import datetime
from supabase import create_client

# ================== الإعدادات الأساسية ==================
# ملاحظة: استبدل القيم أدناه ببياناتك أو استخدم st.secrets
SUPABASE_URL = "ضع_رابط_SUPABASE"
SUPABASE_KEY = "ضع_مفتاح_SUPABASE"
WHATSAPP_TOKEN = "ضع_التوكن_هنا"
WHATSAPP_PHONE_ID = "ضع_PHONE_ID_هنا"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
CITIES = ["قلعة السراغنة", "مراكش", "بني ملال", "الدار البيضاء"]
SECTORS = ["العقار", "الفلاحة", "الاستثمار", "التجارة"]

# ================== محرك Meta Muse Spark ==================
def meta_generate(prompt):
    result = subprocess.run(["meta", "generate", prompt], capture_output=True, text=True, timeout=40)
    return result.stdout.strip()

def meta_search(query):
    result = subprocess.run(["meta", "search", query], capture_output=True, text=True, timeout=30)
    return result.stdout.strip()

# ================== عقل الوكيل الذكي ==================
def super_brain():
    sector = random.choice(SECTORS)
    city = random.choice(CITIES)
    search_data = meta_search(f"أخبار {sector} في {city}")
    
    prompt = f"البيانات: {search_data}. أعطني فرصة استثمارية في {sector} بـ {city} بصيغة JSON."
    ai_json = meta_generate(prompt)
    
    try:
        data = json.loads(ai_json)
        return f"👑 *Meta Tassaout*\n\n🏙️ {data.get('city')}\n📊 {data.get('sector')}\n🎯 {data.get('opportunity')}\n📈 {data.get('prediction')}\n📞 0691897126"
    except:
        return f"👑 *Meta Tassaout*\n\nالفرصة متاحة في {city} بقطاع {sector}.\nاتصل بنا للمزيد: 0691897126"

def send_whatsapp(phone, message):
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": message}}
    requests.post(url, headers=headers, json=payload)

# ================== واجهة القيادة ==================
st.title("👑 Meta Tassaout - القيادة اليدوية")

if st.button("🚀 توليد فرصة"):
    result = super_brain()
    st.session_state.last_op = result
    st.write(result)

if "last_op" in st.session_state:
    phone = st.text_input("رقم العميل:", "212691897129")
    if st.button("📤 إرسال"):
        send_whatsapp(phone, st.session_state.last_op)
        st.success("تم الإرسال")
