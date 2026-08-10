import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- إعدادات النظام السيادي v6.12 (وضع المحاكاة الآمنة) ---
st.set_page_config(
    page_title="TASSAOUT DIGITAL SERVICES - Sovereign OS v6.12", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def simulate_gemini_response(prompt_text):
    return f"👑 **[وضع المحاكاة السيادية]** سيدي الرئيس AMEUR، لقد استلمتُ الأمر التحليلي التالي داخلياً: '{prompt_text[:150]}...'. النظام يعمل بكامل طاقته التشغيلية محلياً."

UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = [
        {"role": "assistant", "content": "👑 أهلاً بك سيدي الرئيس AMEUR في منصة Tassaout Digital Services. النظام يعمل بكفاءة تامة في الذاكرة المحلية السيادية."}
    ]

# --- الشريط الجانبي السيادي ---
st.sidebar.title("👑 Tassaout Digital Services")
st.sidebar.markdown("**Status:** Online (Active)")
st.sidebar.markdown("---")
page = st.sidebar.radio("الوحدات السيادية:", [
    "🧠 محادثة التوأم الذكي",
    "⚡ النشر الفوري",
    "🌐 واجهة العميل (المعرض)",
    "📁 إدارة الأصول",
    "📊 إدارة البيانات",
    "🗺️ خرائط النطاق"
])

st.sidebar.markdown("---")
st.sidebar.markdown("© **إنتاج عامر بوخدادة - كل الحقوق محفوظة**")

# ==========================================
# 1. محادثة التوأم الذكي
# ==========================================
if page == "🧠 محادثة التوأم الذكي":
    st.title("🧠 محادثة التوأم الذكي - Tassaout Digital Services")
    
    for msg in st.session_state.gemini_logs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("اكتب أمرك هنا...")

    if user_query:
        st.session_state.gemini_logs.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        sim_response = simulate_gemini_response(user_query)
        st.session_state.gemini_logs.append({"role": "assistant", "content": sim_response})
        with st.chat_message("assistant"):
            st.markdown(sim_response)

# ==========================================
# 2. لوحة النشر الفوري
# ==========================================
elif page == "⚡ النشر الفوري":
    st.title("⚡ لوحة الإنتاج والنشر الفوري")
    with st.form("form_instant_exec_sim", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض السيادي:")
        ad_sector = st.selectbox("القطاع:", ["عقار", "تجارة", "خدمات", "نقل", "أعمال", "أخرى"])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        uploaded_files = st.file_uploader("📸 رفع صور أو فيديوهات:", accept_multiple_files=True)
        
        submit_button = st.form_submit_button("🚀 تنفيذ الإنتاج والنشر")
        
        if submit_button:
            if ad_title:
                saved_files_paths = []
                if uploaded_files:
                    for file in uploaded_files:
                        local_path = os.path.join(UPLOADS_FOLDER, file.name)
                        with open(local_path, "wb") as f:
                            f.write(file.getbuffer())
                        saved_files_paths.append(local_path)
                
                new_entry = {
                    "title": ad_title,
                    "sector": ad_sector,
                    "details": ad_details + "\n\n© **إنتاج عامر بوخدادة - كل الحقوق محفوظة**",
                    "images": saved_files_paths,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.instant_ads.insert(0, new_entry)
                st.success(f"✅ تم النشر بنجاح للإعلان: '{ad_title}'!")
            else:
                st.warning("⚠️ يجب إدخال عنوان الإعلان.")

    st.markdown("---")
    if st.session_state.instant_ads:
        for idx, ad in enumerate(st.session_state.instant_ads):
            st.info(f"### 🏷️ **{ad['title']}**\n* **القطاع:** {ad['sector']} | 🕒 {ad['time']}\n\n{ad['details']}")
            if ad['images']:
                cols = st.columns(len(ad['images']) if len(ad['images']) <= 3 else 3)
                for i, img_path in enumerate(ad['images']):
                    if os.path.exists(img_path):
                        with cols[i % len(cols)]:
                            st.image(img_path, width=200)
            if st.button(f"🗑️ حذف الإعلان #{idx+1}", key=f"del_ad_sim_{idx}"):
                st.session_state.instant_ads.pop(idx)
                st.rerun()

# ==========================================
# 3. واجهة العميل (المعرض)
# ==========================================
elif page == "🌐 واجهة العميل (المعرض)":
    st.title("🌐 واجهة العميل - المعرض المرئي المباشر")
    if st.session_state.instant_ads:
        for ad in st.session_state.instant_ads:
            st.markdown(f"### 🌟 **{ad['title']}**")
            st.caption(f"القطاع: {ad['sector']} | تاريخ النشر: {ad['time']}")
            
            if ad['images']:
                cols = st.columns(len(ad['images']) if len(ad['images']) <= 3 else 3)
                for i, img_path in enumerate(ad['images']):
                    if os.path.exists(img_path):
                        with cols[i % len(cols)]:
                            st.image(img_path, use_container_width=True)
                            
            st.write(ad['details'])
            st.markdown(f"[💬 اطلب هذا العرض عبر واتساب](https://wa.me/212691897126?text=مرحباً، أهتم بعرض: {ad['title']})")
            st.markdown("---")
    else:
        st.info("🌐 واجهة العميل فارغة حالياً. قم بنشر إعلان من لوحة '⚡ النشر الفوري'.")

# ==========================================
# 4. إدارة الأصول
# ==========================================
elif page == "📁 إدارة الأصول":
    st.title("📁 وحدة إدارة الأصول السيادية")
    st.markdown("### 📂 الملفات المتاحة في الذاكرة المحلية:")
    fake_files = [
        {"name": "Tassaout_Assets_v3.zip", "type": "zip", "size": "150 MB"},
        {"name": "Presentation_Nexus_Alpha.pdf", "type": "pdf", "size": "18 MB"},
        {"name": "Client_Database_Oct.csv", "type": "csv", "size": "5 MB"}
    ]
    for file in fake_files:
        col_f1, col_f2 = st.columns([3, 1])
        with col_f1:
            st.write(f"📄 **{file['name']}** (نوع الملف: {file['type']}) | الحجم: {file['size']}")
        with col_f2:
            st.button(f"📥 تحميل", key=f"sim_drive_{file['name']}")

# ==========================================
# 5. إدارة البيانات
# ==========================================
elif page == "📊 إدارة البيانات":
    st.title("📊 إدارة قواعد البيانات")
    st.markdown("### 📊 سجل العمليات:")
    fake_data = {
        "العنوان": ["مشروع سكني - قلعة السراغنة", "محل تجاري - مراكش", "شراكة لوجستيك"],
        "القطاع": ["عقار", "تجارة", "نقل"],
        "الحالة": ["نشط", "متميز", "قيد التنفيذ"],
        "التاريخ": ["2026-08-01", "2026-08-05", "2026-08-10"]
    }
    df_sim_data = pd.DataFrame(fake_data)
    st.dataframe(df_sim_data, use_container_width=True)

# ==========================================
# 6. واجهة خرائط النطاق
# ==========================================
elif page == "🗺️ خرائط النطاق":
    st.title("🗺️ واجهة خرائط النطاق الجغرافي")
    map_data = pd.DataFrame({
        'latitude': [32.0494, 31.6295],
        'longitude': [-7.4083, -7.9811],
        'location': ['قلعة السراغنة (المركز الرئيسي)', 'مراكش (محور الاستثمار)']
    })
    st.map(map_data, zoom=8)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© <strong>إنتاج عامر بوخدادة - كل الحقوق محفوظة</strong></p>", unsafe_allow_html=True)
