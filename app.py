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
أجب دائماً بعمق تقني، ومهنية عالية، وباللغة العربية المغربية أو الفرنسية التقنية حسب السياق، وفق مرسوم الصفقات العمومية المغربي 2.22.431."""

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

# --- 1. الوكيل الهندسي والتقني ---
if choice == "الوكيل الهندسي والتقني 🤖":
    st.title("🤖 الوكيل الذكي")
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("اطلب استشارة..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("المهندس السيادي يفكر..."):
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config={'system_instruction': SYSTEM_INSTRUCTION}
                )
                st.markdown(response.text)
                st.session_state.chat.append({"role": "assistant", "content": response.text})

# --- 2. محلل الصفقات الذكي ---
elif choice == "محلل الصفقات الذكي 🛡️":
    st.title("🛡️ Smart Tender Analyzer")
    uploaded_file = st.file_uploader("ارفع ملف الـ CPS (PDF):", type=['pdf'])
    if uploaded_file and st.button("تحليل الصفقة 🚀"):
        with st.spinner("المهندس السيادي يحلل..."):
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages: text += page.extract_text() or ""
            
            tender_prompt = f"""حلل هذا الـ CPS كخبير صفقات مغربي (AMO) وفق مرسوم 2.22.431.
            استخرج بدقة: 
            1. المتطلبات التقنية الإلزامية.
            2. المخاطر القانونية والمالية.
            3. البروفايلات المطلوبة.
            4. مسودة Note Méthodologique بالفرنسية التقنية.
            نص الـ CPS: {text[:60000]}"""
            
            response = client.models.generate_content(model='gemini-3.6-flash', contents=tender_prompt)
            st.markdown(response.text)

# --- 3. رصد الميدان ---
elif choice == "رصد الميدان (كاميرا) 📷":
    st.title("📷 رصد الميدان بالذكاء الاصطناعي")
    img_file = st.camera_input("التقط صورة للورش")
    if img_file:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=["حلل هذه الصورة تقنياً وقدم تقريراً لـ OMEGA OS", PIL.Image.open(img_file)]
        )
        st.markdown(response.text)

# --- 4. إدارة الصفقات ---
elif choice == "إدارة الصفقات 📋":
    st.title("📋 إدارة الصفقات السحابية")
    if st.button("عرض الصفقات من Supabase 🔄"):
        df = pd.DataFrame(supabase.table("deals").select("*").execute().data)
        st.dataframe(df)

# --- 5. المنصة الرئيسية ---
elif choice == "المنصة الرئيسية 🏡":
    st.title(f"مرحباً عامر في {NOM_ENTREPRISE}")
    st.success("OMEGA OS - Elite Core: النظام في وضع السيادة التامة.")
