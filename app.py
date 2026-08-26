import streamlit as st
from supabase import create_client, Client
import requests
import json
from datetime import datetime

# ==========================================
# 1. تهيئة الإعدادات (Supabase)
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_SECRET_KEY = st.secrets.get("SUPABASE_SECRET_KEY")

if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
    st.error("⚠️ خطأ في النظام: المفاتيح السرية غير موجودة.")
    st.stop()

@st.cache_resource
def init_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

supabase = init_supabase_client()

# ==========================================
# 2. الدوال البرمجية (Alpha Core Nexus Operations)
# ==========================================
def insert_instant_ad(content: str, message: str, source: str = "Alpha-Core"):
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
# 3. واجهة التحكم (Nexus UI)
# ==========================================
st.set_page_config(page_title="Alpha Core Nexus", layout="centered", page_icon="💠")

st.title("💠 Alpha Core Nexus - Instant Ads")
st.markdown("لوحة التحكم المركزية لنشر الإعلانات الفورية في قاعدة البيانات.")

with st.form("nexus_ads_form", clear_on_submit=True):
    content = st.text_input("محتوى الإعلان (Content)")
    message = st.text_area("الرسالة النهائية (Message)")
    source = st.text_input("المصدر", value="Alpha-Core-Nexus")
    
    submitted = st.form_submit_button("إرسال إلى قاعدة البيانات")
    
    if submitted:
        if not content or not message:
            st.error("الرجاء ملء حقل المحتوى والرسالة.")
        else:
            success, result = insert_instant_ad(content, message, source)
            if success:
                st.success("✅ تم تسجيل البيانات بنجاح في Alpha Core Nexus!")
            else:
                st.error(f"❌ فشل الاتصال بقاعدة البيانات: {result}")

st.divider()

st.subheader("📋 سجل الإعلانات (Nexus Database)")
success, ads_data = fetch_instant_ads()

if success:
    if ads_data:
        for ad in ads_data:
            with st.expander(f"إعلان: {ad.get('content')} | المصدر: {ad.get('source')}"):
                st.write(f"**الرسالة:** {ad.get('message')}")
                st.caption(f"تاريخ التسجيل: {ad.get('created_at')}")
    else:
        st.info("قاعدة البيانات فارغة حالياً.")
else:
    st.error(f"❌ خطأ في جلب البيانات: {ads_data}")
