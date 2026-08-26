import streamlit as st
from supabase import create_client, Client

# قراءة الإعدادات من secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")

# 1. تهيئة العميل العام للقراءة
@st.cache_resource
def init_public_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# 2. تهيئة العميل الإداري للكتابة
@st.cache_resource
def init_admin_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

supabase_public = init_public_client()
supabase_admin = init_admin_client()

# ==========================================
# عملية الجلب (Select) باستخدام العميل العام
# ==========================================
try:
    ads_response = supabase_public.table("instant_ads").select("*").order("created_at", desc=True).execute()
    ads_data = ads_response.data
except Exception as e:
    st.error(f"تعذر جلب الإعلانات: {e}")

# ==========================================
# عملية الإدخال (Insert) باستخدام العميل الإداري
# ==========================================
if submitted:
    try:
        response = supabase_admin.table("instant_ads").insert({
            "content": content,
            "message": message,
            "source": source
        }).execute()
        st.success("تم حفظ الإعلان بنجاح!")
    except Exception as e:
        st.error(f"حدث خطأ أثناء حفظ الإعلان: {e}")
