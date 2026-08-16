import streamlit as st
import json
import os
import glob

st.set_page_config(page_title="Tassaout Immo & Media", page_icon="🏢", layout="wide")

# التصميم الموحد
st.markdown("""
    <style>
    .main { background-color: #062314; color: #f8fafc; }
    .prop-card { padding: 20px; border-radius: 12px; border: 1px solid #14532d; margin-bottom: 20px; background-color: #0f3d24; }
    .badge-cat { background-color: #166534; color: #4ade80; padding: 4px 10px; border-radius: 6px; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# التأكد من وجود مجلد listings وإنشاء ملف تجريبي تلقائياً لمنع ظهور الخطأ
if not os.path.exists("listings"):
    os.makedirs("listings")
    sample_data = {
        "title": "أرض فلاحية أو محل تجاري تجريبي",
        "category": "العقاري الفلاحي",
        "description": "هذا عقار تجريبي تم إنشاؤه تلقائياً لعمل التطبيق بنجاح.",
        "price": "1,200,000 درهم"
    }
    with open("listings/sample_prop.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=4)

# دالة تحميل الخدمات
def load_services():
    try:
        with open("services_tassaout_sraghna.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"services": []}

# التبديل بين الصفحات
if 'nav_mode' not in st.session_state: 
    st.session_state.nav_mode = "عقارات"

col1, col2, col3 = st.columns(3)
if col1.button("العقارات", use_container_width=True): 
    st.session_state.nav_mode = "عقارات"
if col2.button("الخدمات", use_container_width=True): 
    st.session_state.nav_mode = "خدمات"
if col3.button("اتصل بنا", use_container_width=True): 
    st.session_state.nav_mode = "اتصال"

# محتوى الصفحات
if st.session_state.nav_mode == "عقارات":
    st.title("المحفظة العقارية")
    st.write("استعراض العقارات المتاحة:")
    
    listing_files = glob.glob("listings/*.json")
    if listing_files:
        for file_path in listing_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    prop = json.load(f)
                    st.markdown(f"""
                    <div class="prop-card">
                        <h3>{prop.get('title', 'عقار')}</h3>
                        <span class="badge-cat">{prop.get('category', 'عام')}</span>
                        <p>{prop.get('description', '')}</p>
                        <p><b>السعر:</b> {prop.get('price', 'غير محدد')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                pass
    else:
        st.info("لا توجد ملفات عقارات حالياً.")

elif st.session_state.nav_mode == "خدمات":
    st.title("خدماتنا الرقمية والهندسية")
    data = load_services()
    for s in data.get("services", []):
        with st.expander(f"{s.get('الخدمة', 'خدمة')}"):
            st.write(s.get('الوصف', ''))

elif st.session_state.nav_mode == "اتصال":
    st.title("تواصل مع عامر بوخدادة")
    st.success("الهاتف/واتساب: 0691897126")
    st.markdown("[اضغط هنا للمحادثة المباشرة](https://wa.me/212691897126)")
