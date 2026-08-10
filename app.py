import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- إعدادات النظام السيادي v6.13 (تفعيل تحميل وحفظ الأصول) ---
st.set_page_config(
    page_title="TASSAOUT DIGITAL SERVICES - Sovereign OS v6.13", 
    layout="wide",
    initial_sidebar_state="expanded"
)

UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = [
        {"role": "assistant", "content": "👑 أهلاً بك سيدي الرئيس AMEUR. النظام جاهز الآن للتحميل الفعلي وإدارة الأصول بكفاءة تامة."}
    ]

# --- الشريط الجانبي السيادي ---
st.sidebar.title("👑 Tassaout Digital Services")
st.sidebar.markdown("**Status:** Online & Active")
st.sidebar.markdown("---")
page = st.sidebar.radio("الوحدات السيادية:", [
    "🧠 محادثة التوأم الذكي",
    "⚡ النشر الفوري",
    "🌐 واجهة العميل (المعرض)",
    "📁 إدارة الأصول والتحميل",
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
        
        sim_response = f"👑 **[النظام السيادي]** سيدي الرئيس AMEUR، تم تنفيذ الأمر: '{user_query}' بنجاح."
        st.session_state.gemini_logs.append({"role": "assistant", "content": sim_response})
        with st.chat_message("assistant"):
            st.markdown(sim_response)

# ==========================================
# 2. لوحة النشر الفوري
# ==========================================
elif page == "⚡ النشر الفوري":
    st.title("⚡ لوحة الإنتاج والنشر الفوري")
    with st.form("form_instant_exec", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض السيادي:")
        ad_sector = st.selectbox("القطاع:", ["عقار", "تجارة", "خدمات", "نقل", "أعمال", "أخرى"])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        uploaded_files = st.file_uploader("📸 رفع صور أو فيديوهات للإعلان:", accept_multiple_files=True)
        
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
            if st.button(f"🗑️ حذف الإعلان #{idx+1}", key=f"del_ad_{idx}"):
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
# 4. إدارة الأصول والتحميل الفعلي
# ==========================================
elif page == "📁 إدارة الأصول والتحميل":
    st.title("📁 وحدة إدارة الأصول والتحميل الفعلي")
    st.markdown("قم برفع أي ملف أو أصل جديد ليتم تخزينه في النظام السحابي، أو تحميل الملفات المحفوظة:")

    # رفع ملفات جديدة حقيقية
    uploaded_asset = st.file_uploader("📤 رفع أصل جديد (ملف، صورة، مستند):", accept_multiple_files=False)
    if uploaded_asset:
        file_path = os.path.join(UPLOADS_FOLDER, uploaded_asset.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_asset.getbuffer())
        st.success(f"✅ تم رفع وحفظ الملف '{uploaded_asset.name}' بنجاح في النظام!")

    st.markdown("---")
    st.subheader("📂 الأصول والمستندات المخزنة حالياً:")
    
    if os.path.exists(UPLOADS_FOLDER):
        files_in_folder = os.listdir(UPLOADS_FOLDER)
        if files_in_folder:
            for file_name in files_in_folder:
                f_path = os.path.join(UPLOADS_FOLDER, file_name)
                f_size = os.path.getsize(f_path) / 1024 # بالحكيلوبايت
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📄 **{file_name}** ({f_size:.1f} KB)")
                with col2:
                    with open(f_path, "rb") as fp:
                        st.download_button(
                            label="📥 تحميل",
                            data=fp,
                            file_name=file_name,
                            key=f"down_{file_name}"
                        )
                with col3:
                    if st.button("🗑️ حذف", key=f"del_{file_name}"):
                        os.remove(f_path)
                        st.rerun()
        else:
            info_msg = "لا توجد أصول مرفوعة حالياً. استخدم زر الرفع أعلاه."
            st.info(info_msg)

# ==========================================
# 5. إدارة البيانات
# ==========================================
elif page == "📊 إدارة البيانات":
    st.title("📊 إدارة قواعد البيانات")
    st.markdown("### 📊 سجل العمليات السيادية:")
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
