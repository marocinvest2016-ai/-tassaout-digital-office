import streamlit as st
import os
from datetime import datetime

# --- 1. إعدادات الصفحة السيادية ---
st.set_page_config(page_title="TASSAOUT OMEGA OS - لوحة التحكم الكاملة", layout="wide")
UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

# --- 2. الشريط الجانبي للتنقل (استعادة الأقسام) ---
st.sidebar.title("👑 مركز القيادة السيادي")
page = st.sidebar.radio("الوحدات الحية:", [
    "لوحة النشر الفوري (متعدد الصور)",
    "واجهة العرض الحية للعملاء",
    "معرض الأصول الرقمية (Archive)",
    "توليد التقارير الشاملة (PDF Engine)"
])

# --- 3. الوحدة: لوحة النشر الفوري (التي طلبتها) ---
if page == "لوحة النشر الفوري (متعدد الصور)":
    st.title("👑 لوحة التحكم والإنتاج الفوري - تساوت أوميغا")
    with st.form("form_instant_execution", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض:")
        ad_sector = st.selectbox("القطاع المرتبط:", ["القطاع الفلاحي والآليات الثقيلة", "القطاع الصناعي (STE RITA FER)", "القطاع العقاري والاستثماري"])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        uploaded_files = st.file_uploader("📸 اختر الصور من هاتفك (Sélectionner متعدد):", type=["jpg", "png", "jpeg", "webp"], accept_multiple_files=True)
        
        if st.form_submit_button("🚀 تنفيذ النشر الفوري"):
            if ad_title:
                saved_filenames = []
                for file in uploaded_files:
                    path = os.path.join(UPLOADS_FOLDER, file.name)
                    with open(path, "wb") as f: f.write(file.getbuffer())
                    saved_filenames.append(file.name)
                st.session_state.instant_ads.insert(0, {"title": ad_title, "sector": ad_sector, "details": ad_details, "images": saved_filenames})
                st.success("✅ تم النشر بنجاح!")

# --- 4. الوحدة: واجهة العرض الحية للعملاء ---
elif page == "واجهة العرض الحية للعملاء":
    st.title("🌐 واجهة العميل")
    for ad in st.session_state.instant_ads:
        st.info(f"### 🏷️ {ad['title']}\n{ad['details']}")
        if ad["images"]:
            cols = st.columns(3)
            for i, img in enumerate(ad["images"]): cols[i % 3].image(os.path.join(UPLOADS_FOLDER, img))
        st.markdown("---")

# --- 5. الوحدة: معرض الأصول الرقمية ---
elif page == "معرض الأصول الرقمية (Archive)":
    st.title("📂 الأرشيف السيادي")
    files = os.listdir(UPLOADS_FOLDER)
    if files:
        cols = st.columns(4)
        for i, f in enumerate(files): cols[i % 4].image(os.path.join(UPLOADS_FOLDER, f), use_container_width=True)
    else: st.write("الأرشيف فارغ.")

# --- 6. الوحدة: توليد التقارير الشاملة ---
elif page == "توليد التقارير الشاملة (PDF Engine)":
    st.title("📑 DANA-Global Document Engine")
    if st.button("⚡ توليد التقرير التجاري الشامل PDF"):
        st.success("تم توليد التقرير بنجاح (المحرك جاهز للربط).")

st.sidebar.markdown("---")
st.sidebar.info("TASSAOUT OMEGA OS v4.1 - مدير الموقع: Ameur")
