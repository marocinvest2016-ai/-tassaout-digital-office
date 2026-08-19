import streamlit as st
from supabase import create_client
from google import genai
import PIL.Image
import pandas as pd
from datetime import datetime

# --- إعدادات النظام ---
BOT_NAME = "OMEGA OS - Elite Core"
NOM_ENTREPRISE = "وكالة تساوت الرقمية للخدمات"

# 1. قراءة الأسرار من st.secrets
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("⚠️ يرجى التأكد من إعداد ملف الأسرار secrets.toml بشكل صحيح.")
    st.stop()

# 2. تهيئة الاتصال
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# استخدام المكتبة الجديدة والنموذج المطلوب
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = f"""أنت المهندس السيادي لـ {NOM_ENTREPRISE}.
تخصصاتك: البرمجة، الهندسة المعمارية، وخبراء الصفقات.
أجب دائماً بعمق تقني ومهنية عالية وباللغة العربية المغربية."""

st.set_page_config(page_title=BOT_NAME, layout="wide")

# --- القائمة الجانبية ---
st.sidebar.title(f"👑 {BOT_NAME}")
menu = ["المنصة الرئيسية 🏡", "الوكيل الهندسي والتقني 🤖", "رصد الميدان (كاميرا) 📷", "توليد الصور الفوري ✨", "إدارة الصفقات 📋"]
choice = st.sidebar.radio("الوحدات التشغيلية:", menu)

# --- 2. الوكيل الهندسي والتقني ---
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
                    # استخدام النموذج المحدث
                    response = client.models.generate_content(
                        model='gemini-3.6-flash', 
                        contents=prompt,
                        config={'system_instruction': SYSTEM_INSTRUCTION}
                    )
                    st.markdown(response.text)
                    st.session_state.chat.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"⚠️ خطأ في المحرك: {e}")

# --- 3. رصد الميدان (كاميرا) ---
elif choice == "رصد الميدان (كاميرا) 📷":
    st.title("📷 رصد الميدان بالذكاء الاصطناعي")
    img_file = st.camera_input("التقط صورة")
    if img_file:
        project_name = st.text_input("اسم المشروع:")
        if st.button("تحليل الورش ميدانياً 🔍"):
            img = PIL.Image.open(img_file)
            prompt = "حلل الصورة وقدم تقريراً تقنياً مفصلاً."
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[prompt, img]
            )
            st.markdown(response.text)
