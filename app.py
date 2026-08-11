import streamlit as st
from supabase import create_client
from google import genai
import os

# 1. إعدادات الصفحة والاتصال
st.set_page_config(page_title="نظام الإعلانات السيادي 👑", layout="wide")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# إعداد العميل لـ Google GenAI
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

st.title("نظام الإعلانات السيادي 👑")

# 2. وظيفة جلب البيانات من قاعدة البيانات
def load_ads_from_db():
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return []

# 3. وظيفة توليد الإعلان عبر الذكاء الاصطناعي وحفظه
def create_and_save_ad(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"قم بصياغة إعلان عقاري أو تجاري جذاب وقصير بناءً على: {prompt}. أعطني العنوان في السطر الأول، وباقي التفاصيل في المحتوى."
    )
    
    ai_text = response.text
    lines = ai_text.strip().split('\n')
    title = lines[0].replace("#", "").strip() if lines else "إعلان جديد"
    content = "\n".join(lines[1:]).strip() if len(lines) > 1 else ai_text

    # الحفظ في جدول instant_ads
    data = {"title": title, "content": content}
    supabase.table("instant_ads").insert(data).execute()

# 4. عرض الواجهة وجلب الإعلانات
ads = load_ads_from_db()

col_ai, col_display = st.columns(2, gap="large")

with col_ai:
    st.subheader("🤖 توليد إعلان فوري")
    user_input = st.text_input("أدخل تفاصيل أو فكرة الإعلان:")
    if st.button("توليد ونشر الإعلان فوراً"):
        if user_input:
            with st.spinner("جاري التوليد والنشر عبر الذكاء الاصطناعي..."):
                create_and_save_ad(user_input)
                st.success("تم نشر الإعلان بنجاح في قاعدة البيانات!")
                st.rerun()
        else:
            st.warning("المرجو إدخال تفاصيل الإعلان أولاً.")

with col_display:
    st.subheader("📋 لوحة الإعلانات الحالية")
    if not ads:
        st.info("لا توجد إعلانات حالياً. استخدم الذكاء الاصطناعي لإنشاء أول إعلان!")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title', 'بدون عنوان')} ({str(ad.get('created_at', ''))[:10]})"):
                st.write(ad.get('content', ''))
