import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")

# تعريف عميل عام للقراءة
@st.cache_resource
def get_public_client():
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# تعريف عميل إداري للكتابة (Service Role)
@st.cache_resource
def get_admin_client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

supabase_public = get_public_client()
supabase_admin = get_admin_client()

st.title("📢 إدارة نظام الإعلانات الفورية (Instant Ads)")

with st.form("instant_ads_form"):
    content = st.text_input("محتوى الإعلان (Content)")
    message = st.text_area("الرسالة النهائية (Message)")
    source = st.text_input("المصدر", value="streamlit-agent")
    
    submitted = st.form_submit_button("حفظ وإرسال الإعلان")
    
    if submitted:
        if not content or not message:
            st.error("الرجاء ملء الحقول المطلوبة.")
        else:
            try:
                # استخدام supabase_admin حصرياً لتجاوز RLS وتجنب خطأ 401
                response = supabase_admin.table("instant_ads").insert({
                    "content": content,
                    "message": message,
                    "source": source
                }).execute()
                
                st.success("تم حفظ الإعلان الفوري بنجاح!")
                st.json(response.data)
            except Exception as e:
                st.error(f"خطأ في الإدخال: {e}")
