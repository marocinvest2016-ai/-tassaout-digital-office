import streamlit as st
import requests
import urllib.parse
from supabase import create_client

st.set_page_config(page_title="OMEGA AGENTIC", page_icon="👑", layout="wide")
st.markdown('<h1 style="text-align:center;color:#800020;">👑 OMEGA AGENTIC SUPER AI</h1>', unsafe_allow_html=True)

# قراءة من Secrets فقط. ما بقا والو فالكود
META_KEY = st.secrets["MODEL_API_KEY"]
SUPA_URL = st.secrets["SUPABASE_URL"]
SUPA_KEY = st.secrets["SUPABASE_KEY"]
WA_NUM = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "212691897126")

supabase = create_client(SUPA_URL, SUPA_KEY)

def meta_ai(task):
    url = "https://api.meta.ai/v1/responses"
    headers = {"Authorization": f"Bearer {META_KEY}", "Content-Type": "application/json"}
    payload = {"model": "muse-spark-1.2", "input": [{"role": "user", "content": [{"type": "input_text", "text": task}]}]}
    return requests.post(url, headers=headers, json=payload).json()['response'][0]['content'][0]['text']

domaine = st.selectbox("🏛️ المجال", ["العقار", "الهندسة", "التجارة"])
task = st.text_area("🎯 المهمة", "شقق للبيع في قلعة السراغنة")
send_to = st.text_input("📞 رقم الواتساب", WA_NUM)

if st.button("⚡ فعل الوكيل"):
    with st.spinner("MUSE-SPARK يخدم...
