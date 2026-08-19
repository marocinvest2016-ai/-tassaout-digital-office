import streamlit as st
from supabase import create_client
import google.generativeai as genai

# --- 1. إعدادات النظام ---
BOT_NAME = "AmarAgent v4.2"
NOM_ENTREPRISE = "شركة عامر للخدمات"
ICE = "1234567890"
RC = "987654"

# --- 2. الإعدادات السحابية ---
SUPABASE_URL = "https://rbyjjnkhdjfksyodiujs.supabase.co"
SUPABASE_KEY = "sb_publishable_Rf29NrOcmLnj0woKiYNFXw_8R5C8sP-"
GEMINI_API_KEY = "AQ.Ab8RN6Ljovi728xOU2kCuJFbk15..." 

# --- 3. تهيئة المحركات ---
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=f"أنت {BOT_NAME} خبير العقار واللوجستيك لـ {NOM_ENTREPRISE}. تساعد في إدارة العمليات العقارية والأتمتة الرقمية."
)

# --- 4. هيكلة البيانات ---
class TassaoutAgenticCore:
    def __init__(self):
        self.listings = [
            {"title": "تجزئة الهدى 1", "details": "إحداثيات جغرافية دقيقة، مساحة منظمة."},
            {"title": "تجزئة الهدى 2", "details": "تتبع دقيق للمساحات وهامش الربح."},
            {"title": "بقع البدر 1", "details": "إدارة العقود والتوثيق الرسمي."}
        ]

# --- 5. الواجهة البرمجية ---
st.set_page_config(page_title=BOT_NAME, layout="wide")
st.title(f"👑 مكتب تساوت الرقمي - {BOT_NAME}")

tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم (Dashboard)", "🗄️ إدارة المشاريع (Supabase)", "🤖 المساعد الذكي (AI)"])

with tab1:
    st.header("السجل الشامل")
    core = TassaoutAgenticCore()
    for item in core.listings:
        with st.expander(item['title']):
            st.write(item['details'])

with tab2:
    st.header("إضافة مشروع جديد")
    project_title = st.text_input("اسم المشروع")
    if st.button("حفظ في قاعدة البيانات"):
        try:
            supabase.table("projects").insert({"name": project_title}).execute()
            st.success("تم الحقن بنجاح!")
        except Exception as e:
            st.error(f"خطأ: {e}")

with tab3:
    st.header("محرك الأتمتة")
    user_prompt = st.text_area("أدخل المهمة أو الكود المراد تحسينه:")
    if st.button("تنفيذ العمليات"):
        with st.spinner("جاري المعالجة..."):
            res = model.generate_content(user_prompt)
            st.markdown("### 🤖 الرد:")
            st.write(res.text)
