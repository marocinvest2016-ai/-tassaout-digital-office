import streamlit as st
from supabase import create_client
import random

# 1. إعدادات الصفحة السيادية
st.set_page_config(page_title="نظام الإعلانات العقارية السيادي 👑", layout="wide")

# 2. المفاتيح والاتصال المباشر بقاعدة البيانات
SUPABASE_URL = "https://xjjriuohqvhdxfgsyepl.supabase.co"
SUPABASE_KEY = "sb_publishable_xNbvcCGrqDQyU8fAtEMF7w_FqDzwSVg"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
    st.stop()

st.title("👑 لوحة تحكم ونظام إعلانات العقارات")

# 3. دالة جلب الإعلانات من Supabase
def load_ads_from_db():
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        return []

# 4. دالة صياغة الإعلانات الاحترافية فورياً
def generate_pro_ad(details):
    templates = [
        f"شقة فاخرة ومجهزة للبيع في موقع استراتيجي بقلعة السراغنة. المواصفات: {details}. موقع هادئ وقريب من جميع المرافق الحيوية. للمزيد من التفاصيل أو المعاينة، يرجى الاتصال بالوكالة مباشرة.",
        f"فرصة استثمارية عقارية ممتازة! عقار يتوفر على: {details}. تشطيبات عصرية وبثمن مناسب جداً. سارع بالتواصل معنا لحجز موعد للمعاينة.",
        f"عرض حصري للوكالة: {details}. تتواجد بالقرب من المحاور الرئيسية في قلعة السراغنة. تواصل معنا الآن للحصول على كافة التفاصيل والشروط."
    ]
    return random.choice(templates)

# 5. واجهة التطبيق الثنائية
col_input, col_view = st.columns(2, gap="large")

with col_input:
    st.subheader("🤖 صياغة ونشر إعلان جديد")
    user_input = st.text_area("أدخل تفاصيل العقار (مثال: شقة 120م²، 3 غرف، صالون):")
    
    if st.button("توليد ونشر فوري"):
        if user_input:
            with st.spinner("جاري المعالجة والحفظ السيادي..."):
                ad_content = generate_pro_ad(user_input)
                ad_title = f"إعلان عقاري: {user_input[:35]}..."
                
                # إدخال البيانات مباشرة إلى جدول Supabase
                supabase.table("instant_ads").insert({
                    "title": ad_title, 
                    "content": ad_content
                }).execute()
                
                st.success("تم النشر بنجاح في قاعدة البيانات!")
                st.rerun()
        else:
            st.warning("يرجى إدخال تفاصيل العقار أولاً.")

with col_view:
    st.subheader("📋 لوحة الإعلانات الحية")
    ads = load_ads_from_db()
    
    if not ads:
        st.info("لا توجد إعلانات مسجلة حالياً في القاعدة.")
    else:
        for ad in ads:
            with st.expander(f"📢 {ad.get('title')} — {str(ad.get('created_at'))[:10]}"):
                st.write(ad.get('content'))
