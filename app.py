import streamlit as st
import os
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# --- إعدادات النظام السيادي الفائق v6.1 ---
st.set_page_config(
    page_title="TASSAOUT OMEGA OS - Sovereign Command Center v6.1", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة عقل Gemini الذكي
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.sidebar.error("⚠️ خطأ في تهيئة عقل Gemini. تأكد من ضبط GEMINI_API_KEY في Secrets.")

# تهيئة مرنة لـ Supabase
supabase_client = None
try:
    from supabase import create_client
    if "SUPABASE_URL" in st.secrets:
        supabase_client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except:
    pass

UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = [
        {"role": "assistant", "content": "👑 أهلاً بك سيدي الرئيس AMEUR. أنا نظامك الذكي الخارق v6.1. حقوق الإنتاج (إنتاج عامر بوخدادة - كل الحقوق محفوظة) موثقة ومعتمدة بالكامل."}
    ]

# --- الشريط الجانبي السيادي ---
st.sidebar.title("👑 قيادة Super Agent v6.1")
st.sidebar.markdown("---")
page = st.sidebar.radio("الوحدات السيادية:", [
    "⚡ النشر الفوري",
    "🌐 واجهة العميل",
    "☁️ التخزين السحابي",
    "🗺️ خرائط النطاق",
    "🧠 عقل الوكيل الخارق"
])

st.sidebar.markdown("---")
st.sidebar.markdown("© **إنتاج عامر بوخدادة - كل الحقوق محفوظة**")

# --- دالة توليد الإعلانات الذكية حسب القطاعات ---
def generate_sector_ad(sector_name, custom_prompt=""):
    try:
        system_instructions = """أنت الوكيل السيادي الرقمي لشركة Ameur Boukhaddada. 
        تعمل في قطاعات متعددة وتشمل: أسفار الحج والعمرة، الهندسة الرقمية والديكور والنمذجة ثلاثية الأبعاد (Modélisation 3D)، الصناعة (STE RITA FER)، التجارة، الخدمات، الأعمال، النقل واللوجستيك، الشراكات الاستثمارية، العقار (تجزئة الهدى بقلعة السراغنة ومراكش)، والمتفرقات.
        مهمتك: صياغة إعلانات تسويقية واحترافية للغاية باللغة العربية الفصحى مع لمسة تجارية ودولية جذابة للجمهور.
        تعليمات صارمة للتنسيق: يجب أن يكون عنوان الإعلان وكل النقاط الأساسية مكتوبة **بخط عريض (Bold)** لجذب انتباه العملاء فوراً.
        يجب أن ينتهي كل إعلان بعبارة واضحة للتواصل مع رقم الواتساب المعتمد: https://wa.me/212691897126
        ويجب أن يُختتم الإعلان بعبارة رسمية: © إنتاج عامر بوخدادة - كل الحقوق محفوظة."""
        
        target = custom_prompt if custom_prompt else f"قطاع أو خدمة: {sector_name}"
        full_prompt = f"{system_instructions}\n\nالطلب المطلوب تنفيذه: {target}"
        response = gemini_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ تعذر توليد الإعلان عبر عقل Gemini حالياً: {e}"

# ==========================================
# 1. لوحة النشر الفوري والرفع
# ==========================================
if page == "⚡ النشر الفوري":
    st.title("⚡ لوحة الإنتاج والنشر الفوري")
    with st.form("form_instant_execution", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض الاستثماري:")
        ad_sector = st.selectbox("القطاع السيادي:", [
            "أسفار حج وعمرة", "هندسة رقمية وديكور 3D", "صناعة", "تجارة", "خدمات", "أعمال", "نقل ولوجستيك", "شراكة", "عقار", "متفرقات"
        ])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        
        uploaded_files = st.file_uploader(
            "📸 رفع الأصول (صور أو فيديوهات mp4):", 
            type=["jpg", "png", "jpeg", "webp", "mp4"], 
            accept_multiple_files=True
        )
        
        submit_button = st.form_submit_button("🚀 تنفيذ الإنتاج والنشر الفوري")
        
        if submit_button:
            if ad_title:
                saved_filenames = []
                if uploaded_files:
                    for file in uploaded_files:
                        try:
                            file_path = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
                            if supabase_client:
                                supabase_client.storage.from_("assets").upload(file_path, file.getbuffer())
                            saved_filenames.append(file_path)
                        except:
                            local_path = os.path.join(UPLOADS_FOLDER, file.name)
                            with open(local_path, "wb") as f:
                                f.write(file.getbuffer())
                            saved_filenames.append(file.name)
                
                new_entry = {
                    "title": ad_title,
                    "sector": ad_sector,
                    "details": ad_details + "\n\n© **إنتاج عامر بوخدادة - كل الحقوق محفوظة**",
                    "images": saved_filenames,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.instant_ads.insert(0, new_entry)
                st.success(f"✅ تم الإنتاج والنشر بنجاح للإعلان: '{ad_title}'!")
            else:
                st.warning("⚠️ يجب إدخال عنوان الإعلان على الأقل.")

    st.markdown("---")
    if st.session_state.instant_ads:
        for idx, ad in enumerate(st.session_state.instant_ads):
            st.info(f"### 🏷️ **{ad['title']}**\n* **القطاع:** {ad['sector']} | 🕒 {ad['time']}\n\n{ad['details']}")
            if st.button(f"🗑️ حذف الإعلان #{idx+1}", key=f"del_ad_{idx}"):
                st.session_state.instant_ads.pop(idx)
                st.rerun()

# ==========================================
# 2. واجهة العميل والمعرض المباشر
# ==========================================
elif page == "🌐 واجهة العميل":
    st.title("🌐 واجهة العميل - العروض الحية والصفقات")
    if st.session_state.instant_ads:
        for ad in st.session_state.instant_ads:
            st.markdown(f"### 🌟 **{ad['title']}**")
            st.caption(f"القطاع: {ad['sector']} | تاريخ النشر: {ad['time']}")
            st.write(ad['details'])
            st.markdown(f"[💬 اطلب هذا العرض فوراً عبر واتساب](https://wa.me/212691897126?text=مرحباً، أهتم بعرض: {ad['title']})")
            st.markdown("---")
    else:
        st.info("🌐 واجهة العميل فارغة حالياً.")

# ==========================================
# 3. الواجهة السحابية الشاملة (Cloud Vault)
# ==========================================
elif page == "☁️ التخزين السحابي":
    st.title("☁️ الواجهة السحابية الشاملة (Cloud Storage Vault)")
    if supabase_client:
        try:
            files_list = supabase_client.storage.from_("assets").list()
            if files_list:
                st.success(f"إجمالي الملفات في سحابة Supabase: {len(files_list)}")
            else:
                st.info("سحابة Supabase فارغة.")
        except Exception as ex:
            st.error(f"خطأ في الاتصال: {ex}")
    else:
        st.warning("⚠️ التخزين السحابي غير مفعل، يتم استخدام التخزين المحلي.")

# ==========================================
# 4. واجهة خرائط Google الاستراتيجية
# ==========================================
elif page == "🗺️ خرائط النطاق":
    st.title("🗺️ واجهة خرائط النطاق الجغرافي (قلعة السراغنة ومراكش)")
    map_data = pd.DataFrame({
        'latitude': [32.0494, 31.6295],
        'longitude': [-7.4083, -7.9811],
        'location': ['قلعة السراغنة (المركز الرئيسي)', 'مراكش (محور الاستثمار)']
    })
    st.map(map_data, zoom=8)

# ==========================================
# 5. محرك الوكيل الخارق (Super Agentic Core)
# ==========================================
elif page == "🧠 عقل الوكيل الخارق":
    st.title("🧠 محرك الوكيل الخارق (Gemini 1.5 Flash Enabled)")
    st.markdown("اختر قطاع العمل لتوليد إعلان فوري بصياغة بارزة **بخط عريض (Bold)**، أو اكتب أمرك المفتوح:")
    
    # شبكة أزرار القطاعات الشاملة
    st.markdown("### ⚡ أزرار القطاعات الاستراتيجية:")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        if st.button("🕋 أسفار حج وعمرة"):
            res = generate_sector_ad("رحلات أسفار الحج والعمرة المتميزة، تنظيم الحملات، الخدمات المتكاملة والإقامة الفاخرة لضيوف الرحمن")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: أسفار حج وعمرة]**\n\n{res}"})
            st.rerun()
    with col_c2:
        if st.button("🏛️ هندسة وديكور 3D"):
            res = generate_sector_ad("هندسة رقمية وديكور وتصميم داخلي وخارجي ونمذجة ثلاثية الأبعاد Modélisation 3D")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: هندسة وديكور 3D]**\n\n{res}"})
            st.rerun()
    with col_c3:
        if st.button("🏠 عقار"):
            res = generate_sector_ad("العقار والبقع الأرضية (تجزئة الهدى بقلعة السراغنة ومراكش)")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: عقار]**\n\n{res}"})
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏭 صناعة"):
            res = generate_sector_ad("الصناعة (مثل مواد البناء والحديد STE RITA FER)")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: صناعة]**\n\n{res}"})
            st.rerun()
    with col2:
        if st.button("🛒 تجارة"):
            res = generate_sector_ad("التجارة والبيع بالجملة والتجزئة")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: تجارة]**\n\n{res}"})
            st.rerun()
    with col3:
        if st.button("🛠️ خدمات"):
            res = generate_sector_ad("الخدمات المهنية والرقمية والاستشارية")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: خدمات]**\n\n{res}"})
            st.rerun()
    with col4:
        if st.button("💼 أعمال"):
            res = generate_sector_ad("الأعمال والمشاريع الاستثمارية الكبرى")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: أعمال]**\n\n{res}"})
            st.rerun()

    col5, col6, col7 = st.columns(3)
    with col5:
        if st.button("🚚 نقل ولوجستيك"):
            res = generate_sector_ad("النقل ولوجستيك ونقل البضائع والآليات")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: نقل ولوجستيك]**\n\n{res}"})
            st.rerun()
    with col6:
        if st.button("🤝 شراكة"):
            res = generate_sector_ad("الشراكة الاستثمارية وتوسيع الأنشطة التجارية والعقارية")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: شراكة]**\n\n{res}"})
            st.rerun()
    with col7:
        if st.button("📌 متفرقات"):
            res = generate_sector_ad("متفرقات وعروض متنوعة")
            st.session_state.gemini_logs.insert(1, {"role": "assistant", "content": f"**[قطاع: متفرقات]**\n\n{res}"})
            st.rerun()

    st.markdown("---")
    
    # سجل الأوامر
    for msg in st.session_state.gemini_logs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # صندوق الإدخال المفتوح
    if prompt := st.chat_input("اكتب تفاصيل إضافية أو طلباً مخصصاً لأي قطاع..."):
        st.session_state.gemini_logs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.spinner("🧠 الوكيل السيادي يكتب الصياغة الاحترافية بخط عريض..."):
            execution_output = generate_sector_ad(prompt, custom_prompt=f"طلب خاص: {prompt}")
        
        st.session_state.gemini_logs.append({"role": "assistant", "content": execution_output})
        with st.chat_message("assistant"):
            st.markdown(execution_output)
            st.download_button(
                label="📥 تحميل مخرجات الإنتاج الذكي",
                data=execution_output,
                file_name=f"Agentic_Production_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© <strong>إنتاج عامر بوخدادة - كل الحقوق محفوظة</strong></p>", unsafe_allow_html=True)
