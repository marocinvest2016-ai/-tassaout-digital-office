import streamlit as st
from supabase import create_client
from google import genai
import PIL.Image
import pandas as pd
import pdfplumber
from datetime import datetime

# --- إعدادات النظام ---
BOT_NAME = "OMEGA OS - Elite Core"
NOM_ENTREPRISE = "وكالة تساوت الرقمية للخدمات"

# 1. قراءة الأسرار
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ يرجى ضبط ملف الأسرار (st.secrets).")
    st.stop()

# 2. تهيئة الاتصال
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = f"""أنت المهندس السيادي لـ {NOM_ENTREPRISE}.
تخصصاتك: البرمجة، الهندسة المعمارية، وخبراء الصفقات.
أجب دائماً بعمق تقني ومهنية عالية وفق مرسوم الصفقات العمومية المغربي 2.22.431."""

st.set_page_config(page_title=BOT_NAME, layout="wide")

# --- القائمة الجانبية ---
st.sidebar.title(f"👑 {BOT_NAME}")
menu = [
    "المنصة الرئيسية 🏡", 
    "الوكيل الهندسي والتقني 🤖", 
    "رصد الميدان (كاميرا) 📷", 
    "توليد الصور الفوري ✨", 
    "إدارة الصفقات 📋",
    "محلل الصفقات الذكي 🛡️"
]
choice = st.sidebar.radio("الوحدات التشغيلية:", menu)

# --- الوحدة 1: الوكيل الهندسي والتقني ---
if choice == "الوكيل الهندسي والتقني 🤖":
    st.title("🤖 الوكيل الذكي")
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("اطلب استشارة..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("المهندس السيادي يفكر..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-1.5-flash', 
                        contents=prompt,
                        config={'system_instruction': SYSTEM_INSTRUCTION}
                    )
                    st.markdown(response.text)
                    st.session_state.chat.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"⚠️ واجه النظام مشكلة في الاتصال بالمحرك السيادي. (تفاصيل: {str(e)[:50]})")

# --- الوحدة 2: محلل الصفقات الذكي ---
elif choice == "محلل الصفقات الذكي 🛡️":
    st.title("🛡️ Smart Tender Analyzer")
    uploaded_file = st.file_uploader("ارفع ملف الـ CPS (PDF):", type=['pdf'])
    if uploaded_file and st.button("تحليل الصفقة 🚀"):
        with st.spinner("المهندس السيادي يحلل..."):
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages: text += page.extract_text() or ""
            tender_prompt = f"حلل هذا الـ CPS وفق مرسوم 2.22.431. استخرج: المتطلبات، المخاطر، والبروفايلات. النص: {text[:50000]}"
            try:
                response = client.models.generate_content(model='gemini-1.5-flash', contents=tender_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"خطأ في التحليل: {e}")

# --- الوحدات الأخرى (رصد الميدان، إدارة الصفقات) ---
elif choice == "رصد الميدان (كاميرا) 📷":
    img_file = st.camera_input("التقط صورة")
    if img_file:
        response = client.models.generate_content(model='gemini-1.5-flash', contents=["حلل الصورة", PIL.Image.open(img_file)])
        st.markdown(response.text)

elif choice == "إدارة الصفقات 📋":
    st.title("إدارة الصفقات السحابية")
    if st.button("عرض الصفقات 🔄"):
        df = pd.DataFrame(supabase.table("deals").select("*").execute().data)
        st.dataframe(df)

elif choice == "المنصة الرئيسية 🏡":
    st.success("OMEGA OS - Elite Core جاهز للعمل.")
