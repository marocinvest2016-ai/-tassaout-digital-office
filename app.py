import streamlit as st
import google.generativeai as genai
from supabase import create_client

# 1. إعدادات الصفحة والاتصال
st.set_page_config(page_title="نظام الإعلانات السيادي 👑", layout="wide")

# 2. تهيئة المفاتيح من Secrets
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في تحميل المفاتيح: {e}")
    st.stop()

st.title("👑 مولد إعلانات العقارات السيادي")

# 3. وظيفة الجلب من قاعدة البيانات
def load_ads_from_db():
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return []

# 4. وظيفة التوليد والحفظ
def create_and_save_ad(prompt):
    response = model.generate_content(f"قم بصياغة إعلان عقاري جذاب وقصير بناءً على: {prompt}. العنوان في السطر الأول، والتفاصيل بعده.")
    ai_text = response.text
    lines = ai_text.strip().split('\n')
    title = lines[0].replace("#", "").strip() if lines else "إعلان جديد"
    content = "\n".join(lines[1:]).strip()

    supabase.table("instant_ads").insert({"title": title, "content": content}).execute()
    return title, content

# 5. الواجهة
col_ai, col_display = st.columns(2, gap="large")

with col_ai:
    st.subheader("🤖 توليد إعلان فوري")
    user_input = st.text_area("أدخل تفاصيل العقار:")
    if st.button("توليد ونشر الإعلان فوراً"):
        if user_input:
            with st.spinner("جاري التوليد والنشر..."):
                create_and_save_ad(user_input)
                st.success("تم نشر الإعلان بنجاح!")
                st.rerun()
        else:
            st.warning("يرجى إدخال تفاصيل العقار.")

with col_display:
    st.subheader("📋 لوحة الإعلانات")
    ads = load_ads_from_db()
    if not ads:
        st.info("لا توجد إعلانات حالياً.")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title')} - {str(ad.get('created_at'))[:10]}"):
                st.write(ad.get('content'))
