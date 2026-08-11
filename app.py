import streamlit as st
from supabase import create_client
import random

st.set_page_config(page_title="نظام الإعلانات العقارية السيادي 👑", layout="wide")

SUPABASE_URL = "https://xjjriuohqvhdxfgsyepl.supabase.co"
SUPABASE_KEY = "sb_publishable_xNbvcCGrqDQyU8fAtEMF7w_FqDzwSVg"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

st.title("👑 لوحة تحكم ونظام إعلانات العقارات")

def load_ads_from_db():
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data if res.data else []
    except Exception as e:
        st.error(f"خطأ في الاتصال بالقاعدة: {e}")
        return []

# المحرك الذكي المحلي (بدون مفتاح Gemini)
def generate_pro_ad(details):
    templates = [
        f"""
🏠 **عرض عقاري مميز بقلعة السراغنة** 🏠

✨ {details}

🎯 **لماذا هذا العقار؟**
✅ تصميم عصري وتشطيبات عالية الجودة.
✅ موقع استراتيجي في قلب قلعة السراغنة.
✅ بالقرب من جميع الخدمات والمرافق الحيوية.
✅ فرصة استثمارية وسكنية لا تعوض.

🔑 **للمزيد من المعلومات أو حجز موعد للمعاينة:**
📞 اتصل بنا على: 0691897126
📧 البريد الإلكتروني: marocinvest2012@gmail.com

---
#عقارات #قلعة_السراغنة #شقق_للبيع #استثمار_عقاري #المغرب #MarocInvest
""",
        f"""
🌟 **فرصة استثمارية عقارية كبرى** 🌟

✨ {details}

🎯 **مميزات العقار:**
✅ مساحة ممتازة وتوزيع داخلي ذكي ومريح.
✅ متواجد بمنطقة هادئة وآمنة بقلعة السراغنة.
✅ قرب تام من الطرق الرئيسية والمحاور الحيوية.

🔑 **للتواصل والاستفادة من العرض:**
📞 اتصل بنا على: 0691897126
📧 البريد الإلكتروني: marocinvest2012@gmail.com

---
#عقارات #قلعة_السراغنة #شقق_للبيع #استثمار_عقاري #المغرب #MarocInvest
"""
    ]
    return random.choice(templates).strip()

col_input, col_view = st.columns(2, gap="large")

with col_input:
    st.subheader("🤖 صياغة ونشر إعلان منظم")
    user_input = st.text_area("أدخل تفاصيل العقار (مثال: شقة 120م²، 3 غرف وصالون):", key="ad_input_area")
    
    if st.button("توليد ونشر فوري", type="primary"):
        if user_input.strip() != "":
            with st.spinner("جاري المعالجة والصياغة السيادية..."):
                ad_content = generate_pro_ad(user_input)
                ad_title = f"إعلان: {user_input[:30]}..."
                
                insert_res = supabase.table("instant_ads").insert({
                    "title": ad_title, 
                    "content": ad_content
                }).execute()
                
                if insert_res:
                    st.success("تم النشر بنجاح بالتنسيق الاحترافي!")
                    st.rerun()
                else:
                    st.error("فشل الحفظ في قاعدة البيانات.")
        else:
            st.warning("يرجى كتابة تفاصيل العقار أولاً.")

with col_view:
    st.subheader("📋 لوحة الإعلانات الحية")
    ads = load_ads_from_db()
    
    if not ads:
        st.info("لا توجد إعلانات مسجلة حالياً.")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title')} — {str(ad.get('created_at'))[:10]}"):
                st.markdown(ad.get('content'))
