import streamlit as st
from supabase import create_client, Client
from google import genai
import requests
import json
from datetime import datetime

# ==========================================
# 1. تهيئة الإعدادات والأسرار
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_SECRET_KEY")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ يرجى التأكد من ضبط SUPABASE_URL و SUPABASE_KEY في ملف secrets.toml")
    st.stop()

# ==========================================
# 2. إنشاء عملاء الاتصال (Supabase & Gemini Flash)
# ==========================================
@st.cache_resource
def init_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_resource
def init_gemini_client():
    if GEMINI_API_KEY:
        return genai.Client(api_key=GEMINI_API_KEY)
    return None

supabase = init_supabase_client()
gemini_client = init_gemini_client()

# ==========================================
# 3. دوال الذكاء الاصطناعي وقاعدة البيانات
# ==========================================
def generate_ad_content(prompt: str) -> str:
    """توليد نص الإعلان باستخدام Gemini 3.6 Flash"""
    if not gemini_client:
        return "⚠️ مفتاح GEMINI_API_KEY غير مضبوط في الإعدادات."
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"خطأ في التوليد: {str(e)}"

def insert_instant_ad(content: str, message: str, source: str = "Alpha-Core-Nexus"):
    try:
        response = supabase.table("instant_ads").insert({
            "content": content,
            "message": message,
            "source": source
        }).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

def fetch_instant_ads():
    try:
        response = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

# ==========================================
# 4. واجهة المستخدم (Streamlit UI)
# ==========================================
st.set_page_config(page_title="Alpha Core Nexus", layout="centered", page_icon="📢")

st.title("📢 إدارة نظام الإعلانات الفورية (Instant Ads)")
st.markdown("أدخل تفاصيل الإعلان الجديد أو استخدم **Gemini Flash** للمساعدة في صياغته.")

# قسم الذكاء الاصطناعي التفاعلي
with st.expander("✨ توليد إعلان ذكي بواسطة Google Gemini Flash"):
    ai_prompt = st.text_input("عن ماذا تريد إعلانك؟ (مثال: شقة للبيع في مراكش)")
    if st.button("توليد النص بالذكاء الاصطناعي"):
        if ai_prompt:
            with st.spinner("جاري التوليد..."):
                generated_text = generate_ad_content(f"اكتب إعلان احترافي قصير للتسويق عن: {ai_prompt}")
                st.session_state["generated_message"] = generated_text
        else:
            st.warning("يرجى كتابة وصف قصير أولاً.")

# نموذج الإدخال الرئيسي
with st.form("instant_ads_form", clear_on_submit=True):
    content = st.text_input("محتوى الإعلان (Content)")
    
    default_msg = st.session_state.get("generated_message", "")
    message = st.text_area("الرسالة النهائية (Message)", value=default_msg)
    source = st.text_input("المصدر", value="Alpha-Core-Nexus")
    
    submitted = st.form_submit_button("حفظ وإرسال الإعلان")
    
    if submitted:
        if not content or not message:
            st.error("الرجاء ملء حقل المحتوى والرسالة على الأقل.")
        else:
            success, result = insert_instant_ad(content, message, source)
            if success:
                st.success("✅ تم حفظ الإعلان بنجاح في قاعدة البيانات!")
            else:
                st.error(f"❌ حدث خطأ أثناء الحفظ: {result}")

st.divider()

# عرض الإعلانات
st.subheader("📋 الإعلانات الفورية الحالية في النظام")
success, ads_data = fetch_instant_ads()

if success:
    if ads_data:
        for ad in ads_data:
            with st.expander(f"إعلان: {ad.get('content')} | المصدر: {ad.get('source')}"):
                st.write(f"**الرسالة:** {ad.get('message')}")
                st.caption(f"تاريخ الإنشاء: {ad.get('created_at')}")
    else:
        st.info("لا توجد إعلانات حالياً.")
else:
    st.error(f"تعذر جلب الإعلانات: {ads_data}")
