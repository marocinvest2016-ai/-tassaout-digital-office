import streamlit as st
import os
from supabase import create_client, Client

# قراءة المتغيرات بالشكل الصحيح المطابق تماماً لملف الأسرار
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# التحقق من وجود المفاتيح لمنع توقف التطبيق
if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_SERVICE_ROLE_KEY:
    st.error("⚠️ يرجى التأكد من إضافة جميع مفاتيح Supabase (URL, ANON_KEY, SERVICE_ROLE_KEY) في إعدادات Secrets.")
    st.stop()

# 1. العميل العام (للقراءة العامة)
@st.cache_resource
def get_public_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# 2. العميل الإداري (للكتابة والإدخال)
@st.cache_resource
def get_admin_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

supabase_public = get_public_client()
supabase_admin = get_admin_client()

# ==========================================
# واجهة Streamlit: إدارة نظام الإعلانات الفورية
# ==========================================
st.title("📢 إدارة نظام الإعلانات الفورية (Instant Ads)")
st.markdown("أدخل تفاصيل الإعلان الجديد ليتم حفظه بشكل آمن في قاعدة البيانات.")

with st.form("instant_ads_form"):
    content = st.text_input("محتوى الإعلان (Content)")
    message = st.text_area("الرسالة النهائية (Message)")
    source = st.text_input("المصدر", value="streamlit-agent")
    
    submitted = st.form_submit_button("حفظ وإرسال الإعلان")
    
    if submitted:
        if not content or not message:
            st.error("الرجاء ملء حقل المحتوى والرسالة على الأقل.")
        else:
            try:
                # استخدام عميل الإدارة (service_role) للإدخال
                response = supabase_admin.table("instant_ads").insert({
                    "content": content,
                    "message": message,
                    "source": source
                }).execute()
                
                st.success("تم حفظ الإعلان الفوري بنجاح في قاعدة البيانات!")
                st.json(response.data)
            except Exception as e:
                st.error(f"حدث خطأ أثناء حفظ الإعلان: {e}")

# ==========================================
# عرض الإعلانات الفورية الحالية (Public Read)
# ==========================================
st.divider()
st.subheader("📋 الإعلانات الفورية الحالية في النظام")

try:
    ads_response = supabase_public.table("instant_ads").select("*").order("created_at", desc=True).execute()
    ads_data = ads_response.data
    
    if ads_data:
        for ad in ads_data:
            with st.expander(f"إعلان: {ad.get('content')} (المصدر: {ad.get('source')})"):
                st.write(f"**الرسالة:** {ad.get('message')}")
                st.caption(f"تاريخ الإنشاء: {ad.get('created_at')}")
    else:
        st.info("لا توجد إعلانات حالياً.")
except Exception as e:
    st.error(f"تعذر جلب الإعلانات: {e}")
