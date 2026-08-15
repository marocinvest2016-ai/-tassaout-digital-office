import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="Bureau Tassaout - إدارة الإعلانات", page_icon="👑", layout="wide")

# الاتصال بـ Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("👑 Bureau Tassaout Digital - الإدارة السيادية")

# نموذج إدخال سريع ونظيف
with st.form("simple_form", clear_on_submit=True):
    st.subheader("📝 إضافة إعلان أو عقار جديد")
    
    col1, col2 = st.columns(2)
    with col1:
        titre = st.text_input("عنوان الإعلان / العقار")
        ville = st.text_input("المدينة / المنطقة", "قلعة السراغنة")
    
    with col2:
        montant = st.number_input("المبلغ (DH)", min_value=0, value=50000)
        secteur = st.selectbox("القطاع", ["أراضي فلاحية", "عقارات سكنية", "تجاري", "خدمات"])

    contenu = st.text_area("تفاصيل الإعلان", height=100)
    
    submit_button = st.form_submit_button("🚀 حفظ الإعلان في القاعدة")

if submit_button:
    if titre and contenu:
        try:
            data = {
                "message": f"{titre}: {contenu}",
                "content": contenu,
                "ville": ville,
                "montant": montant,
                "region": secteur,
                "created_at": datetime.now().isoformat()
            }
            supabase.table("instant_ads").insert(data).execute()
            st.success("✅ تم حفظ الإعلان بنجاح في قاعدة البيانات!")
        except Exception as e:
            st.error(f"خطأ أثناء الحفظ: {e}")
    else:
        st.error("المرجو ملء العنوان والتفاصيل على الأقل.")

st.markdown("---")

# عرض الأرشيف
st.subheader("📂 آخر الإعلانات المسجلة")
try:
    res = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(5).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        st.dataframe(df[['ville', 'message', 'montant', 'created_at']])
    else:
        st.info("لا توجد إعلانات مسجلة حالياً.")
except Exception as e:
    st.error(f"خطأ في جلب البيانات: {e}")
