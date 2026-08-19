import streamlit as st
from supabase import create_client
from google import genai
import PIL.Image
import pandas as pd
import pdfplumber
from datetime import datetime
from fpdf import FPDF

# --- 1. تهيئة الاتصال والأسرار ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ يرجى ضبط ملف الأسرار st.secrets بشكل صحيح.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-1.5-flash-latest"

# --- 2. نظام تسجيل الدخول السيادي ---
if 'user' not in st.session_state:
    st.session_state.user = None

def login():
    st.set_page_config(page_title="OMEGA OS - Login", layout="centered")
    st.title("👑 OMEGA OS - Elite Core")
    st.subheader("تسجيل الدخول السيادي - وكالة تساوت الرقمية")
    email = st.text_input("الإيميل المهني")
    password = st.text_input("كلمة السر", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("دخول", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("خطأ: الإيميل أو كلمة السر غير صحيحة")
    with col2:
        if st.button("إنشاء حساب جديد", use_container_width=True):
            try:
                supabase.auth.sign_up({"email": email, "password": password})
                st.success("تم إنشاء الحساب. تحقق من الإيميل")
            except Exception as e:
                st.error(f"خطأ: {e}")

def logout():
    supabase.auth.sign_out()
    st.session_state.user = None
    st.rerun()

if st.session_state.user is None:
    login()
    st.stop()

# --- 3. الكود الرئيسي ---
user_id = st.session_state.user.id
user_email = st.session_state.user.email

BOT_NAME = "OMEGA OS - Elite Core"
NOM_ENTREPRISE = "وكالة تساوت الرقمية للخدمات"

SYSTEM_INSTRUCTION = f"""أنت المهندس السيادي لـ {NOM_ENTREPRISE}.
تخصصاتك: البرمجة، الهندسة المعمارية، وخبراء الصفقات.
أجب دائماً بعمق تقني، ومهنية عالية، وفق مرسوم الصفقات العمومية المغربي 2.22.431."""

st.set_page_config(page_title=BOT_NAME, layout="wide")

# --- القائمة الجانبية ---
st.sidebar.title(f"👑 {BOT_NAME}")
st.sidebar.write(f"المستخدم: {user_email}")
if st.sidebar.button("تسجيل الخروج 🚪"):
    logout()

menu = ["المنصة الرئيسية 🏡", "الوكيل الهندسي 🤖", "رصد الميدان 📷", "إدارة الصفقات 📋", "محلل الصفقات 🛡️"]
choice = st.sidebar.radio("الوحدات التشغيلية:", menu)

# --- 1. الوكيل الهندسي ---
if choice == "الوكيل الهندسي 🤖":
    st.title("🤖 الوكيل الذكي والسيادي")
    if "chat" not in st.session_state: st.session_state.chat = []
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if prompt := st.chat_input("اطلب استشارة تقنية أو هندسية..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("المهندس السيادي يفكر..."):
                response = client.models.generate_content(model=MODEL_ID, contents=prompt, config={'system_instruction': SYSTEM_INSTRUCTION})
                st.markdown(response.text)
                st.session_state.chat.append({"role": "assistant", "content": response.text})

# --- 2. محلل الصفقات ---
elif choice == "محلل الصفقات 🛡️":
    st.title("🛡️ Smart Tender Analyzer")
    uploaded_file = st.file_uploader("ارفع ملف الـ CPS (PDF):", type=['pdf'])
    if uploaded_file and st.button("تحليل الصفقة 🚀"):
        with st.spinner("جاري التحليل..."):
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages: text += page.extract_text() or ""
            tender_prompt = f"حلل هذا الـ CPS كخبير صفقات مغربي وفق مرسوم 2.22.431. النص: {text[:50000]}"
            response = client.models.generate_content(model=MODEL_ID, contents=tender_prompt)
            st.markdown(response.text)

# --- 3. رصد الميدان ---
elif choice == "رصد الميدان 📷":
    st.title("📷 رصد الميدان والورش")
    col1, col2 = st.columns(2)
    with col1: img_file_cam = st.camera_input("التقط صورة 📸")
    with col2: img_file_up = st.file_uploader("أو ارفع صورة", type=['jpg', 'jpeg', 'png'])
    img_file = img_file_cam or img_file_up
    
    if img_file:
        st.image(img_file, caption="الصورة المختارة", use_container_width=True)
        project_name = st.text_input("اسم المشروع أو الورش:")
        if st.button("تحليل الورش وحفظ التقرير 🔍"):
            with st.spinner("يحلل..."):
                img = PIL.Image.open(img_file)
                response = client.models.generate_content(model=MODEL_ID, contents=["حلل هذه الصورة تقنياً وقدم تقريراً مفصلاً", img])
                st.markdown(response.text)
                
                if project_name:
                    supabase.table("reports").insert({
                        "project_name": project_name, "report_content": response.text,
                        "date": datetime.now().isoformat(), "type": "image_analysis", "user_id": user_id
                    }).execute()
                    st.success("✅ تم حفظ التقرير")

# --- 4. إدارة الصفقات ---
elif choice == "إدارة الصفقات 📋":
    st.title("📋 إدارة الصفقات السحابية")
    with st.expander("➕ إضافة صفقة جديدة"):
        with st.form("new_deal", clear_on_submit=True):
            nom = st.text_input("اسم الصفقة")
            montant = st.number_input("المبلغ MAD", min_value=0)
            if st.form_submit_button("حفظ"):
                supabase.table("deals").insert({"nom": nom, "montant": montant, "user_id": user_id, "date_creation": datetime.now().isoformat()}).execute()
                st.success("تمت الإضافة")
    
    if st.button("تحديث وعرض الصفقات 🔄"):
        res = supabase.table("deals").select("*").eq("user_id", user_id).execute()
        df = pd.DataFrame(res.data)
        st.dataframe(df, use_container_width=True)

# --- 5. المنصة الرئيسية ---
elif choice == "المنصة الرئيسية 🏡":
    st.title(f"مرحباً بك يا عامر في {NOM_ENTREPRISE}")
    st.success("OMEGA OS - Elite Core: النظام يعمل بسيادة تامة.")
