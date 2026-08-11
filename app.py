import streamlit as st
from google import genai
from supabase import create_client

# 1. إعدادات الصفحة السيادية
st.set_page_config(page_title="نظام الإعلانات السيادي 👑", layout="wide")

# 2. تحميل المفاتيح والتهيئة السيادية
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"خطأ في التهيئة أو المفاتيح: {e}")
    st.stop()

st.title("👑 مولد إعلانات العقارات السيادي")

# 3. دالة جلب الإعلانات من قاعدة البيانات
def load_ads_from_db():
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        return []

# 4. دالة التوليد والحفظ الفوري
def create_and_save_ad(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=f"قم بصياغة إعلان عقاري جذاب وقصير بناءً على: {prompt}. العنوان في السطر الأول، والتفاصيل بعده."
        )
        ai_text = response.text
        lines = ai_text.strip().split('\n')
        title = lines[0].replace("#", "").strip() if lines else "إعلان جديد"
        content = "\n".join(lines[1:]).strip()

        supabase.table("instant_ads").insert({"title": title, "content": content}).execute()
        return True
    except Exception as e:
        st.error(f"تفاصيل خطأ التوليد: {e}")
        return False

# 5. واجهة التطبيق
col_ai, col_display = st.columns(2, gap="large")

with col_ai:
    st.subheader("🤖 توليد إعلان فوري")
    user_input = st.text_area("أدخل تفاصيل العقار (مثال: شقة للبيع في قلعة السراغنة 100م²):")
    if st.button("توليد ونشر الإعلان فوراً"):
        if user_input:
            with st.spinner("جاري المعالجة السيادية والنشر..."):
                if create_and_save_ad(user_input):
                    st.success("تم النشر بنجاح!")
                    st.rerun()
        else:
            st.warning("يرجى إدخال تفاصيل العقار.")

with col_display:
    st.subheader("📋 لوحة الإعلانات")
    ads = load_ads_from_db()
    if not ads:
        st.info("لا توجد إعلانات حالياً في قاعدة البيانات.")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title')} - {str(ad.get('created_at'))[:10]}"):
                st.write(ad.get('content'))
