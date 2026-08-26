import streamlit as st
from supabase import create_client, Client

# ==========================================
# Supabase Configuration & Initialization
# ==========================================
# يتم استخدام مفتاح service_role لضمان صلاحيات الكتابة الكاملة المتوافقة مع قواعد RLS
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "YOUR_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "YOUR_SUPABASE_SERVICE_ROLE_KEY")

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

supabase = init_supabase()

# ==========================================
# Streamlit UI: إدارة نظام الإعلانات الفورية
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
                # تنفيذ عملية الإدخال باستخدام مفتاح الخدمة عبر الباك إند
                response = supabase.table("instant_ads").insert({
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
    ads_response = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
    ads_data = ads_ads = ads_response.data
    
    if ads_data:
        for ad in ads_data:
            with st.expander(f"إعلان: {ad.get('content')} (المصدر: {ad.get('source')})"):
                st.write(f"**الرسالة:** {ad.get('message')}")
                st.caption(f"تاريخ الإنشاء: {ad.get('created_at')}")
    else:
        st.info("لا توجد إعلانات حالياً.")
except Exception as e:
    st.error(f"تعذر جلب الإعلانات: {e}")
