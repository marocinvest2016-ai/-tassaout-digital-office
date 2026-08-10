import streamlit as st
import os
import pandas as pd
from datetime import datetime
from PIL import Image

# محاولة استيراد مكتبة الذكاء الاصطناعي بأمان تام
gemini_available = False
try:
    import google.generativeai as genai
    gemini_available = True
except ImportError:
    pass

# --- إعدادات النظام السيادي v6.10 (Multi-Image Vision Support) ---
st.set_page_config(
    page_title="TASSAOUT OMEGA OS - Sovereign Vision v6.10", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة عقل Gemini الذكي
gemini_model = None
if gemini_available:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        pass

# تهيئة Google Drive / Sheets بأمان
google_sheets_client = None
drive_service = None
try:
    import gspread
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    
    if "GCP_SERVICE_ACCOUNT" in st.secrets:
        scope = [
            "https://spreadsheets.google.com/feeds", 
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        creds_dict = dict(st.secrets["GCP_SERVICE_ACCOUNT"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        google_sheets_client = gspread.authorize(creds)
        drive_service = build('drive', 'v3', credentials=creds)
except Exception:
    pass

UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = [
        {"role": "assistant", "content": "👑 أهلاً بك سيدي الرئيس AMEUR. تم تفعيل نظام رفع وتحليل الصور المتعددة دفعة واحدة في الإصدار v6.10."}
    ]

# --- الشريط الجانبي السيادي ---
st.sidebar.title("👑 قيادة Super Agent v6.10")
st.sidebar.markdown("---")
page = st.sidebar.radio("الوحدات السيادية:", [
    "🧠 محادثة التوأم الذكي (Gemini Core)",
    "⚡ النشر الفوري مع الصور",
    "🌐 واجهة العميل (المعرض المرئي)",
    "📁 Google Drive (التحميل المباشر)",
    "📊 Google Sheets",
    "🗺️ خرائط النطاق"
])

st.sidebar.markdown("---")
st.sidebar.markdown("© **إنتاج عامر بوخدادة - كل الحقوق محفوظة**")

# ==========================================
# 1. محادثة التوأم الذكي (دعم صور متعددة)
# ==========================================
if page == "🧠 محادثة التوأم الذكي (Gemini Core)":
    st.title("🧠 محادثة التوأم الذكي - تحليل الصور المتعددة والذكاء الفائق")
    st.markdown("تحدث معي بحرية، وارفع **عدة صور معاً** لتحليلها واستخراج البيانات منها دفعة واحدة:")

    # عرض سجل المحادثة
    for msg in st.session_state.gemini_logs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "image_paths" in msg and msg["image_paths"]:
                cols = st.columns(len(msg["image_paths"]) if len(msg["image_paths"]) <= 3 else 3)
                for i, img_path in enumerate(msg["image_paths"]):
                    if os.path.exists(img_path):
                        with cols[i % len(cols)]:
                            st.image(img_path, width=200)

    user_query = st.chat_input("اكتب أمرك أو استفسارك هنا...")
    uploaded_chat_images = st.file_uploader(
        "📸 ارفع صوراً متعددة لتحليلها مع الرسالة:", 
        type=["jpg", "png", "jpeg", "webp"], 
        accept_multiple_files=True
    )

    if user_query or uploaded_chat_images:
        if not user_query:
            user_query = "تحليل الصور المرفقة واستخراج كافة التفاصيل بدقة."
            
        user_msg_dict = {"role": "user", "content": user_query}
        saved_img_paths = []
        
        if uploaded_chat_images:
            for img_file in uploaded_chat_images:
                saved_img_path = os.path.join(UPLOADS_FOLDER, img_file.name)
                with open(saved_img_path, "wb") as f:
                    f.write(img_file.getbuffer())
                saved_img_paths.append(saved_img_path)
            user_msg_dict["image_paths"] = saved_img_paths

        st.session_state.gemini_logs.append(user_msg_dict)
        with st.chat_message("user"):
            st.markdown(user_query)
            if saved_img_paths:
                cols = st.columns(len(saved_img_paths) if len(saved_img_paths) <= 3 else 3)
                for i, img_path in enumerate(saved_img_paths):
                    with cols[i % len(cols)]:
                        st.image(img_path, width=200)

        with st.spinner("🧠 جاري معالجة النص والصور المتعددة بدقة فائقة..."):
            ai_response_text = ""
            if gemini_model:
                try:
                    system_prompt = """أنت الوكيل السيادي الرقمي الذكي للمستخدم عامر بوخدادة.
                    تعمل في قطاعات العقار، التجارة، الخدمات، النقل، والهندسة.
                    أجب بدقة بالغة، وبأسلوب ذكي ومهني باللغة العربية.
                    أي عناوين أو نقاط أساسية يجب أن تكون مكتوبة **بخط عريض (Bold)** حصراً.
                    اختم الإجابة دائماً برابط الواتساب: https://wa.me/212691897126
                    والعبارة الرسمية: © إنتاج عامر بوخدادة - كل الحقوق محفوظة."""
                    
                    content_payload = [system_prompt]
                    if saved_img_paths:
                        for img_p in saved_img_paths:
                            content_payload.append(Image.open(img_p))
                    content_payload.append(user_query)
                    
                    response = gemini_model.generate_content(content_payload)
                    ai_response_text = response.text
                except Exception as e:
                    ai_response_text = f"عذراً سيدي الرئيس، حدث خطأ أثناء المعالجة الذكية: {e}"
            else:
                ai_response_text = f"**رد النظام:** تم استلام طلبك والصور بنجاح.\n\nللتواصل والاستفادة فوراً عبر الواتساب:\nhttps://wa.me/212691897126\n\n© **إنتاج عامر بوخدادة - كل الحقوق محفوظة**"

        st.session_state.gemini_logs.append({"role": "assistant", "content": ai_response_text})
        with st.chat_message("assistant"):
            st.markdown(ai_response_text)
            st.download_button(
                label="📥 تحميل المخرجات الذكية",
                data=ai_response_text,
                file_name=f"Smart_Output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# ==========================================
# 2. لوحة النشر الفوري مع الصور
# ==========================================
elif page == "⚡ النشر الفوري مع الصور":
    st.title("⚡ لوحة الإنتاج والنشر الفوري مع الصور")
    with st.form("form_instant_execution", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العرض الاستثماري:")
        ad_sector = st.selectbox("القطاع السيادي:", [
            "أسفار حج وعمرة", "هندسة رقمية وديكور 3D", "صناعة", "تجارة", "خدمات", "أعمال", "نقل ولوجستيك", "شراكة", "عقار", "متفرقات"
        ])
        ad_details = st.text_area("تفاصيل العرض النصية:")
        
        uploaded_files = st.file_uploader(
            "📸 رفع الصور أو الفيديوهات المرفقة للإعلان:", 
            type=["jpg", "png", "jpeg", "webp", "mp4"], 
            accept_multiple_files=True
        )
        
        submit_button = st.form_submit_button("🚀 تنفيذ الإنتاج والنشر الفوري")
        
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
                
                if google_sheets_client:
                    try:
                        sheet = google_sheets_client.open("Tassaout_Omega_DB").sheet1
                        sheet.append_row([ad_title, ad_sector, ad_details, new_entry["time"]])
                    except:
                        pass

                st.success(f"✅ تم النشر بنجاح للإعلان: '{ad_title}'!")
            else:
                st.warning("⚠️ يجب إدخال عنوان الإعلان على الأقل.")

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
# 3. واجهة العميل (المعرض المرئي)
# ==========================================
elif page == "🌐 واجهة العميل (المعرض المرئي)":
    st.title("🌐 واجهة العميل - المعرض المرئي المباشر للعروض")
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
            st.markdown(f"[💬 اطلب هذا العرض فوراً عبر واتساب](https://wa.me/212691897126?text=مرحباً، أهتم بعرض: {ad['title']})")
            st.markdown("---")
    else:
        st.info("🌐 واجهة العميل فارغة حالياً. قم بنشر إعلان مع صور من لوحة '⚡ النشر الفوري مع الصور' ليظهر هنا فوراً.")

# ==========================================
# 4. إدارة Google Drive
# ==========================================
elif page == "📁 Google Drive (التحميل المباشر)":
    st.title("📁 وحدة Google Drive - التحميل المباشر للأصول والملفات")
    if drive_service:
        st.success("🟢 الاتصال بـ Google Drive مفعل بنجاح!")
        try:
            results = drive_service.files().list(
                pageSize=15, 
                fields="files(id, name, mimeType, webViewLink, size)"
            ).execute()
            items = results.get('files', [])
            
            if items:
                st.markdown("### 📂 الملفات المتاحة في سحابة Google Drive:")
                for item in items:
                    col_f1, col_f2 = st.columns([3, 1])
                    with col_f1:
                        st.write(f"📄 **{item['name']}** (نوع الملف: {item['mimeType'].split('/')[-1]})")
                    with col_f2:
                        st.markdown(f"[📥 تحميل / عرض مباشر]({item.get('webViewLink', '#')})")
                st.markdown("---")
            else:
                st.info("📂 لم يتم العثور على ملفات في حساب Google Drive المرتبط.")
        except Exception as e:
            st.error(f"خطأ أثناء جلب الملفات من Drive: {e}")
    else:
        st.warning("⚠️ يرجى تفعيل مفاتيح حساب الخدمة في أسرار Streamlit لتفعيل التحميل المباشر من Google Drive.")

# ==========================================
# 5. إدارة Google Sheets
# ==========================================
elif page == "📊 Google Sheets":
    st.title("📊 إدارة قواعد البيانات عبر Google Sheets")
    if google_sheets_client:
        st.success("🟢 الاتصال بـ Google Sheets مفعل بنجاح!")
        try:
            sheet = google_sheets_client.open("Tassaout_Omega_DB").sheet1
            data = sheet.get_all_records()
            if data:
                df_sheets = pd.DataFrame(data)
                st.dataframe(df_sheets, use_container_width=True)
            else:
                st.info("📊 الجدول الإلكتروني فارغ حالياً.")
        except Exception as e:
            st.error(f"خطأ في قراءة الجدول: {e}")
    else:
        st.warning("⚠️ ربط Google Sheets يتطلب إعداد مفاتيح حساب الخدمة في الـ Secrets.")

# ==========================================
# 6. واجهة خرائط Google الاستراتيجية
# ==========================================
elif page == "🗺️ خرائط النطاق":
    st.title("🗺️ واجهة خرائط النطاق الجغرافي (قلعة السراغنة ومراكش)")
    map_data = pd.DataFrame({
        'latitude': [32.0494, 31.6295],
        'longitude': [-7.4083, -7.9811],
        'location': ['قلعة السراغنة (المركز الرئيسي)', 'مراكش (محور الاستثمار)']
    })
    st.map(map_data, zoom=8)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© <strong>إنتاج عامر بوخدادة - كل الحقوق محفوظة</strong></p>", unsafe_allow_html=True)
