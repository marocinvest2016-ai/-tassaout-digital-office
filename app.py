import streamlit as st
from PIL import Image
import os

# إعداد الصفحة
st.set_page_config(page_title="خدمات السراغنة", layout="centered")

# العنوان السيادي
st.title("💐 خدمات السراغنة للتسويق الرقمي العقاري والتجاري 💐")
st.markdown("### المعرض الرقمي للسيارات والآليات الفلاحية")

# مركز التحكم
st.sidebar.header("مركز التحكم")
if st.sidebar.checkbox("نظام Active", value=True):
    st.sidebar.success("النظام في حالة تشغيل كامل")

# قسم تحليل الملفات (مع معالجة الأخطاء)
st.subheader("📂 تحليل الملفات الذكي")
uploaded_file = st.file_uploader("اختر صورة أو ملف للتحليل", type=["jpg", "png", "webp", "pdf"])

if uploaded_file is not None:
    try:
        if uploaded_file.type.startswith("image/"):
            image = Image.open(uploaded_file)
            st.image(image, caption=f"تم رفع الملف: {uploaded_file.name}", use_container_width=True)
        else:
            st.success(f"تم استقبال الملف بنجاح: {uploaded_file.name}")
    except Exception as e:
        st.error(f"خطأ في معالجة الملف: {e}")

# عرض معلومات التواصل
st.divider()
st.subheader("📞 تواصل مع الوسيط")
st.markdown("""
- **الهاتف/واتساب:** [+212691897126](https://wa.me/212691897126)
- **البريد الإلكتروني:** marocinvest2012@gmail.com
""")

# تذييل الصفحة
st.markdown("---")
st.caption("خدمات السراغنة للتسويق الرقمي العقاري والتجاري - الجودة والموثوقية")
