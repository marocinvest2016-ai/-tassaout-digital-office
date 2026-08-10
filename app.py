import streamlit as st
import os
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import supabase

# --- إعدادات النظام السيادي الفائق v5.1 ---
st.set_page_config(page_title="TASSAOUT OMEGA OS - Super Agentic AI v5.1", layout="wide")

# تهيئة اتصال Supabase للأرشيف الدائم
try:
    supabase_client = supabase.create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.sidebar.error("⚠️ خطأ في اتصال Supabase (تأكد من إعداد Secrets)")

# تهيئة عقل Gemini الذكي
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
except:
    pass

UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = [
        {"role": "assistant", "content": "👑 أهلاً بك سيدي الرئيس AMEUR. أنا نظامك الذكي الخارق v5.1 (Super Multi-Domaine Agentic AI). العقل المدبر والأرشيف الدائم مفعلان بالكامل."}
    ]

# --- الشريط الجانبي السيادي ---
st.sidebar.title("👑 قيادة Super Agentic v5.1")
page = st.sidebar.radio("الوحدات السيادية:", [
    "لوحة النشر الفوري والرفع الدائم",
    "واجهة العميل والمعرض المباشر",
    "الواجهة السحابية الشاملة (Cloud Vault)",
    "واجهة خرائط Google (Maps Integration)",
    "محرك الوكيل الخارق (Super Agentic Core)"
])

# --- 1. وحدة النشر الفوري مع الرفع الدائم Supabase ---
if page == "لوحة النشر الفوري والرفع الدائم":
    st.title("⚡ لوحة الإنتاج والنشر الفوري (تخزين دائم)")
    st.markdown("ارفع الأصول (صور وفيديوهات)، يتم حفظها في Supabase للأبد مع النشر اللحظي.")
    
    with st.form("form_instant_execution", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض:")
        ad_sector = st.selectbox("القطاع السيادي:", [
            "القطاع الفلاحي والآليات الثقيلة", 
            "القطاع الصناعي (STE RITA FER)", 
            "القطاع العقاري والاستثماري"
        ])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        
        uploaded_files = st.file_uploader(
            "📸 رفع الأصول (صور / فيديو mp4):", 
            type=["jpg", "png", "jpeg", "webp", "mp4"], 
            accept_multiple_files=True
        )
        
        submit_button = st.form_submit_button("🚀 تنفيذ الإنتاج والنشر الدائم")
        
        if submit_button:
            if ad_title:
                saved_filenames = []
                if uploaded_files:
                    for file in uploaded_files:
                        try:
                            file_path = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
                            supabase_client.storage.from_("assets").upload(file_path, file.getbuffer())
                            saved_filenames.append(file_path)
                        except Exception as ex:
                            local_path = os.path.join(UPLOADS_FOLDER, file.name)
                            with open(local_path, "wb") as f:
                                f.write(file.getbuffer())
                            saved_filenames.append(file.name)
                
                new_entry = {
                    "title": ad_title,
                    "sector": ad_sector,
                    "details": ad_details,
                    "images": saved_filenames,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.instant_ads.insert(0, new_entry)
                st.success(f"✅ تم الإنتاج والنشر بنجاح للإعلان: '{ad_title}' مع تأمين الأصول للأبد.")
            else:
                st.warning("⚠️ يجب إدخال عنوان الإعلان لتنفيذ العملية.")

    st.markdown("---")
    st.subheader("📢 الإدارة والتحكم في المنشورات:")
    if st.session_state.instant_ads:
        for idx, ad in enumerate(st.session_state.instant_ads):
            st.info(f"### 🏷️ {ad['title']}\n* **القطاع:** {ad['sector']} | 🕒 {ad['time']}\n\n{ad['details']}")
            if ad["images"]:
                cols = st.columns(min(len(ad["images"]), 3))
                for i, img_name in enumerate(ad["images"]):
                    try:
                        public_url = supabase_client.storage.from_("assets").get_public_url(img_name)
                        cols[i % 3].image(public_url, caption=img_name, use_container_width=True)
                    except:
                        local_p = os.path.join(UPLOADS_FOLDER, img_name)
                        if os.path.exists(local_p):
                            cols[i % 3].image(local_p, caption=img_name, use_container_width=True)
            if st.button(f"🗑️ حذف الإعلان #{idx+1}", key=f"del_ad_{idx}"):
                st.session_state.instant_ads.pop(idx)
                st.rerun()
            st.markdown("---")
    else:
        st.info("لا توجد إعلانات منشورة حالياً.")

# --- 2. واجهة العميل والمعرض المباشر ---
elif page == "واجهة العميل والمعرض المباشر":
    st.title("🌐 واجهة العميل - العروض الحية والصفقات")
    st.markdown("استعراض كافة العروض والمنتجات المنشورة لحظياً:")
    
    if st.session_state.instant_ads:
        for idx_ad, ad in enumerate(st.session_state.instant_ads):
            st.markdown(f"### 🌟 {ad['title']}")
            st.caption(f"القطاع: {ad['sector']} | تاريخ النشر: {ad['time']}")
            st.write(ad['details'])
            
            if ad["images"]:
                cols = st.columns(min(len(ad["images"]), 3))
                for i, img_name in enumerate(ad["images"]):
                    try:
                        public_url = supabase_client.storage.from_("assets").get_public_url(img_name)
                        cols[i % 3].image(public_url, caption=img_name, use_container_width=True)
                    except:
                        local_p = os.path.join(UPLOADS_FOLDER, img_name)
                        if os.path.exists(local_p):
                            cols[i % 3].image(local_p, caption=img_name, use_container_width=True)
            
            st.markdown(f"[💬 اطلب هذا العرض عبر واتساب](https://wa.me/212691897126?text=مرحباً، أهتم بعرض: {ad['title']})")
            st.markdown("---")
    else:
        st.info("🌐 لا توجد عروض منشورة في واجهة العميل حالياً.")

# --- 3. الواجهة السحابية الشاملة (Cloud Vault) ---
elif page == "الواجهة السحابية الشاملة (Cloud Vault)":
    st.title("☁️ الواجهة السحابية الشاملة (Supabase Storage Vault)")
    st.markdown("إدارة الأرشيف الدائم في السحابة:")
    
    try:
        files_list = supabase_client.storage.from_("assets").list()
        if files_list:
            st.success(f"إجمالي الأصول المؤمنة للأبد في سحابة Supabase: {len(files_list)} ملف.")
            cols_cloud = st.columns(4)
            for i, file_obj in enumerate(files_list):
                f_name = file_obj['name']
                if f_name != ".emptyFolderPlaceholder":
                    public_url = supabase_client.storage.from_("assets").get_public_url(f_name)
                    cols_cloud[i % 4].image(public_url, caption=f_name, use_container_width=True)
                    cols_cloud[i % 4].markdown(f"[📥 تحميل دائم]({public_url})")
        else:
            st.info("السحابة فارغة حالياً.")
    except Exception as ex:
        st.error(f"تعذر جلب قائمة الملفات من Supabase: {ex}")

# --- 4. واجهة خرائط Google (Maps Integration) ---
elif page == "واجهة خرائط Google (Maps Integration)":
    st.title("🗺️ واجهة خرائط النطاق الجغرافي (قلعة السراغنة ومراكش)")
    st.markdown("النطاق الاستراتيجي لعمليات الاستثمار العقاري والفلاحي:")
    
    map_data = pd.DataFrame({
        'latitude': [32.0494, 31.6295],
        'longitude': [-7.4083, -7.9811],
        'location': ['قلعة السراغنة (المركز الرئيسي)', 'مراكش (محور الاستثمار)']
    })
    st.map(map_data, zoom=8)
    st.success("📍 الخريطة مفعلة ضمن النطاق الجغرافي المعتمد.")

# --- 5. محرك الوكيل الخارق (Super Agentic Core مع Gemini API) ---
elif page == "محرك الوكيل الخارق (Super Agentic Core)":
    st.title("🧠 محرك الوكيل الخارق (Gemini 1.5 Flash Enabled)")
    st.markdown("الوكيل يفكر، يولد، ويكتب الإعلانات والتقارير تلقائياً بناءً على أوامرك.")
    
    for msg in st.session_state.gemini_logs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("اكتب الأمر السيادي: 'ولد إعلان فلاحي لجرارات Massey Ferguson'"):
        st.session_state.gemini_logs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.spinner("🧠 الوكيل السيادي يحلل ويكتب الآن..."):
            try:
                system_prompt = f"""أنت الوكيل السيادي TASSAOUT OMEGA OS v5.1 لشركة Ameur Boukhaddada. 
                القطاعات: فلاحي، صناعي STE RITA FER، عقاري تجزئة الهدى.
                مهمتك: توليد إعلان احترافي جاهز للواتساب بالعربية الفصحى مع تضمين رابط التواصل: https://wa.me/212691897126"""
                
                response = gemini_model.generate_content(system_prompt + "\n\nالأمر: " + prompt)
                execution_output = response.text
            except Exception as e:
                execution_output = f"⚠️ حدث خطأ في اتصال Gemini API (تأكد من إدخال المفتاح الصحيح في Secrets): {e}"
        
        st.session_state.gemini_logs.append({"role": "assistant", "content": execution_output})
        with st.chat_message("assistant"):
            st.markdown(execution_output)
            st.download_button(
                label="📥 تحميل مخرجات الإنتاج الذكي",
                data=execution_output,
                file_name=f"Agentic_Production_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

st.sidebar.markdown("---")
st.sidebar.caption("TASSAOUT OMEGA OS - Super Agentic AI v5.1 Active ⚡")
