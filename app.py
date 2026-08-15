import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="Meta Tassaout - المكتب السيادي", page_icon="👑", layout="wide")

# الاتصال بـ Supabase من أسرار Streamlit Secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("👑 المكتب السيادي - إدارة المحتوى والعقارات")
st.markdown("### 🟢 متصل بـ GitHub و Streamlit وقاعدة بيانات Supabase")

# --- واجهة إدخال البيانات ورفع الصور ---
with st.form("tassaout_form", clear_on_submit=True):
    st.subheader("📝 إضافة إعلان أو عقار جديد مع الصورة")
    
    col1, col2 = st.columns(2)
    with col1:
        titre = st.text_input("عنوان الإعلان / العقار")
        ville = st.text_input("المدينة / المنطقة", "قلعة السراغنة")
        montant = st.number_input("المبلغ التقديري (DH)", min_value=0, value=50000)
    
    with col2:
        secteur = st.selectbox("القطاع", ["أراضي فلاحية", "عقارات سكنية", "تجاري", "خدمات"])
        image_file = st.file_uploader("رفع صورة الإعلان (JPG / PNG)", type=['jpg', 'png', 'jpeg'])

    contenu = st.text_area("نص الإعلان الترويجي التفصيلي", height=120)
    
    submit_button = st.form_submit_button("🚀 حفظ ونشر في المكتب السيادي")

if submit_button:
    if titre and contenu:
        try:
            image_url = ""
            # رفع الصورة إلى Supabase Storage إذا تمت إضافتها
            if image_file is not None:
                file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}"
                file_bytes = image_file.getvalue()
                
                # رفع الملف إلى Bucket باسم 'ads-images' (تأكد من إنشائه في Supabase)
                res_storage = supabase.storage.from_("ads-images").upload(file_name, file_bytes)
                
                # الحصول على الرابط العام للصورة
                image_url = supabase.storage.from_("ads-images").get_public_url(file_name)

            # حفظ البيانات في جدول instant_ads
            data = {
                "message": f"{titre}: {contenu}",
                "content": contenu,
                "ville": ville,
                "montant": montant,
                "region": secteur,
                "lien": image_url, # تخزين رابط الصورة في حقل الـ lien أو مخصص
                "created_at": datetime.now().isoformat()
            }
            
            supabase.table("instant_ads").insert(data).execute()
            st.success("✅ تم حفظ الإعلان والصورة بنجاح في Supabase!")
        except Exception as e:
            st.error(f"⚠️ خطأ أثناء الحفظ أو رفع الصورة (تأكد من إنشاء Storage Bucket باسم 'ads-images'): {e}")
    else:
        st.error("المرجو ملء العنوان ومحتوى الإعلان على الأقل.")

st.markdown("---")

# --- عرض الأرشيف والبيانات المخزنة ---
st.subheader("📂 آخر الإعلانات المسجلة في النظام السيادي")
try:
    res = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(5).execute()
    if res.data:
        for ad in res.data:
            with st.expander(f"📍 {ad.get('ville', 'قلعة السراغنة')} - {ad.get('montant', 0)} DH"):
                st.write(f"**التفاصيل:** {ad.get('message')}")
                if ad.get('lien') and ad.get('lien').startswith('http'):
                    st.image(ad.get('lien'), width=300, caption="صورة الإعلان المرفوعة")
                st.caption(تاريخ: {ad.get('created_at')})
    else:
        st.info("لا توجد إعلانات مسجلة حالياً.")
except Exception as e:
    st.error(f"خطأ في جلب البيانات: {e}")
