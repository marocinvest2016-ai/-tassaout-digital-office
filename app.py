import streamlit as st
import os

# --- 1. إعدادات الصفحة السيادية ---
st.set_page_config(
    page_title="TASSAOUT OMEGA OS - لوحة التحكم السيادية",
    page_icon="👑",
    layout="wide"
)

UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# تهيئة حالة الجلسة للتخزين الفوري
if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

st.title("👑 لوحة التحكم والإنتاج الفوري - تساوت أوميغا")
st.markdown("النظام السيادي المباشر: ارفع الصور واكتب التفاصيل وانشر لحظياً في الموقع دون توقف.")

# --- 2. واجهة النشر الفوري (نصوص + رفع متعدد للصور) ---
with st.container():
    st.subheader("📢 نشر إعلان أو عرض جديد (متعدد الصور)")
    
    with st.form("form_instant_execution", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض:")
        ad_sector = st.selectbox("القطاع المرتبط:", [
            "القطاع الفلاحي والآليات الثقيلة", 
            "القطاع الصناعي (STE RITA FER)", 
            "القطاع العقاري والاستثماري"
        ])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        
        # زر الرفع المتعدد من الهاتف (Sélectionner)
        uploaded_files = st.file_uploader(
            "📸 اختر الصور من هاتفك (يمكنك تحديد عدة صور دفعة واحدة):", 
            type=["jpg", "png", "jpeg", "webp"], 
            accept_multiple_files=True
        )
        
        submit_button = st.form_submit_button("🚀 تنفيذ النشر الفوري في الموقع")
        
        if submit_button:
            if ad_title:
                saved_filenames = []
                if uploaded_files:
                    for file in uploaded_files:
                        file_path = os.path.join(UPLOADS_FOLDER, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        saved_filenames.append(file.name)
                
                # حفظ الإعلان في الذاكرة الحية
                new_entry = {
                    "title": ad_title,
                    "sector": ad_sector,
                    "details": ad_details,
                    "images": saved_filenames
                }
                st.session_state.instant_ads.insert(0, new_entry)
                st.success(f"✅ تم تنفيذ النشر بنجاح! الإعنوان '{ad_title}' متوفر الآن مع {len(saved_filenames)} صورة.")
            else:
                st.warning("⚠️ يجيب إدخال عنوان الإعلان على الأقل لتنفيذ العملية.")

# --- 3. عرض العروض والمنشورات الحية مع صورها ---
st.markdown("---")
st.subheader("🌐 العروض والإعلانات المنشورة في واجهة الموقع:")

if st.session_state.instant_ads:
    for idx, ad in enumerate(st.session_state.instant_ads):
        with st.container():
            st.info(f"### 🏷️ {ad['title']}\n* **القطاع:** {ad['sector']}\n\n{ad['details']}")
            
            # عرض الصور المرتبطة بالإعلان بشكل أفقي منظم
            if ad["images"]:
                cols = st.columns(min(len(ad["images"]), 3))
                for i, img_name in enumerate(ad["images"]):
                    img_path = os.path.join(UPLOADS_FOLDER, img_name)
                    if os.path.exists(img_path):
                        cols[i % 3].image(img_path, caption=img_name, use_container_width=True)
            
            if st.button(f"🗑️ حذف الإعلان #{idx+1}", key=f"del_ad_{idx}"):
                st.session_state.instant_ads.pop(idx)
                st.rerun()
        st.markdown("---")
else:
    st.write("لا توجد إعلانات منشورة حالياً. استخدم النموذج أعلاه للنشر الفوري.")

# --- 4. الأرشيف العام للأصول الرقمية ---
st.subheader("📂 معرض الأرشيف السحابي والمحلي")
if os.path.exists(UPLOADS_FOLDER):
    all_files = os.listdir(UPLOADS_FOLDER)
    if all_files:
        archive_cols = st.columns(4)
        for i, filename in enumerate(all_files):
            file_path = os.path.join(UPLOADS_FOLDER, filename)
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                archive_cols[i % 4].image(file_path, caption=filename, use_container_width=True)
    else:
        st.write("الأرشيف فارغ حالياً.")
