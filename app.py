import streamlit as st
from supabase import create_client, Client
import requests
import json
from datetime import datetime

# ==========================================
# 1. إعدادات المساعد والكونفجريشن (Tassaout Config)
# ==========================================
API_URL = "https://cloud.studio51universal.ai/agent/A3-REALTY/init"
BEARER_TOKEN = "SIGNATURE_AMEUR_KEY"
WHATSAPP = "+212691897126"

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

A3_REALTY_CONFIG = {
    "agent_id": "A3-REALTY",
    "mission": "agent_immobilier_commercial",
    "status": "active",
    "version": "2.0",
    "timestamp": datetime.now().isoformat(),
    "regions": [
        "Marrakech",
        "El Haouz", 
        "Tassaout"
    ],
    "languages": ["ar", "fr"],
    "language_detection": True,
    "default_language": "ar",
    "tone": "professionnel_respectueux",
    "capabilities": {
        "lead_generation": True,
        "property_evaluation": True,
        "visit_scheduling": True,
        "contract_generation": True,
        "whatsapp_auto_reply": True,
        "property_matching": True
    },
    "branding": {
        "watermark": "APPROUVÉ PAR AMEUR",
        "seal": "Tassaout Vision Verified © 2026",
        "colors": ["#D4AF37", "#800020"]
    }
}

# ==========================================
# 2. تهيئة الإعدادات والتحقق من الأسرار (Supabase)
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_SECRET_KEY = st.secrets.get("SUPABASE_SECRET_KEY")

if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
    st.error("⚠️ يرجى التأكد من ضبط SUPABASE_URL و SUPABASE_SECRET_KEY في ملف secrets.toml")
    st.stop()

@st.cache_resource
def init_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

supabase = init_supabase_client()

# ==========================================
# 3. الدوال البرمجية لإدارة العمليات (Database Operations)
# ==========================================
def insert_instant_ad(content: str, message: str, source: str = "streamlit-admin"):
    """إدراج إعلان فوري جديد في قاعدة البيانات"""
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
    """جلب قائمة الإعلانات الحالية مرتبة تنازلياً"""
    try:
        response = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return True, response.data
    except Exception as e:
        return False, str(e)

# ==========================================
# 4. واجهة المستخدم (Streamlit UI)
# ==========================================
st.set_page_config(page_title="إدارة الإعلانات الفورية", layout="centered")

st.title("📢 إدارة نظام الإعلانات الفورية (Instant Ads)")
st.markdown("أدخل تفاصيل الإعلان الجديد ليتم حفظه بشكل آمن في قاعدة البيانات.")

# نموذج الإدخال
with st.form("instant_ads_form", clear_on_submit=True):
    content = st.text_input("محتوى الإعلان (Content)")
    message = st.text_area("الرسالة النهائية (Message)")
    source = st.text_input("المصدر", value="streamlit-admin")
    
    submitted = st.form_submit_button("حفظ وإرسال الإعلان")
    
    if submitted:
        if not content or not message:
            st.error("الرجاء ملء حقل المحتوى والرسالة على الأقل.")
        else:
            success, result = insert_instant_ad(content, message, source)
            if success:
                st.success("تم حفظ الإعلان الفوري بنجاح في قاعدة البيانات!")
            else:
                st.error(f"حدث خطأ أثناء حفظ الإعلان: {result}")

st.divider()

# عرض البيانات الحالية
st.subheader("📋 الإعلانات الفورية الحالية في النظام")

success, ads_data = fetch_instant_ads()

if success:
    if ads_data:
        for ad in ads_data:
            with st.expander(f"إعلان: {ad.get('content')} (المصدر: {ad.get('source')})"):
                st.write(f"**الرسالة:** {ad.get('message')}")
                st.caption(f"تاريخ الإنشاء: {ad.get('created_at')}")
    else:
        st.info("لا توجد إعلانات حالياً.")
else:
    st.error(f"تعذر جلب الإعلانات: {ads_data}")
