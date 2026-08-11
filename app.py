import streamlit as st
import os
from google import genai
from google.genai import types
from supabase import create_client, Client

# --- إعدادات الصفحة السيادية ---
st.set_page_config(
    page_title="SRAGHNA IMMOBILIÈRE - التوأم الذكي السيادي",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- الاتصال بـ Supabase + Gemini ---
@st.cache_resource
def init_clients():
    supa: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    return supa, gemini_client

try:
    supabase, client = init_clients()
    MODEL_NAME = 'gemini-2.0-flash' # تم تحديث النموذج للمتوافق مع الإصدارات الحالية
    db_ok = True
except Exception as e:
    st.error(f"خطأ في الاتصال بالبنية التحتية: {e}")
    db_ok = False
    client = None

# --- دوال الذاكرة السياقية ---
def load_memory():
    if db_ok:
        res = supabase.table("gemini_memory").select("*").eq("user_id", "president_amr").order("created_at", desc=False).limit(20).execute()
        return res.data
    return []

def save_memory(role, content):
    if db_ok:
        supabase.table("gemini_memory").insert({"user_id": "president_amr", "role": role, "content": content}).execute()

def save_ad_to_db(ad):
    if db_ok:
        supabase.table("instant_ads").insert(ad).execute()
        return True
    return False

def load_ads_from_db():
    if db_ok:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data
    return []

# --- تهيئة الحالة الثابتة ---
if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = load_memory()
    if not st.session_state.gemini_logs:
        welcome = {"role": "assistant", "content": "👑 أهلاً بعودتك سيدي الرئيس عامر بوخدادة. النظام السيادي في حالة استقرار تام. أنا جاهز للأوامر."}
        st.session_state.gemini_logs.append(welcome)
        save_memory("assistant", welcome["content"])

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = load_ads_from_db()

# --- الواجهة ---
col_ai, col_publish = st.columns(2, gap="large")

# القسم الأول: التوأم الذكي
with col_ai:
    st.subheader("🧠 التوأم الذكي السيادي")
    st.markdown("---")
    
    chat_container = st.container(height=450)
    with chat_container:
        for msg in st.session_state.gemini_logs:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_query = st.chat_input("أصدر أمرك سيدي الرئيس...", key="real_gemini_input")

    if user_query:
        st.session_state.gemini_logs.append({"role": "user", "content": user_query})
        save_memory("user", user_query)
        
        ai_reply = ""
        if client:
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.gemini_logs[-10:]])
                system_prompt = f"""أنت التوأم الذكي والوكيل السيادي لـ عامر بوخدادة، مدير Sraghna Immobilière.
                استعمل السياق السابق للإجابة باحترافية وبصيغة تليق بالرئيس.
                السياق السابق:\n{history}"""

                response = client.models.generate_content_stream(
                    model=MODEL_NAME,
                    contents=user_query,
                    config=types.GenerateContentConfig(system_instruction=system_prompt)
                )
                
                placeholder = st.empty()
                for chunk in response:
                    ai_reply += chunk.text
                    placeholder.markdown(ai_reply + "▌")
                placeholder.markdown(ai_reply)

            except Exception as e:
                ai_reply = f"👑 سيدي الرئيس، خطأ تقني: {str(e)}"
        
        st.session_state.gemini_logs.append({"role": "assistant", "content": ai_reply})
        save_memory("assistant", ai_reply)
        st.rerun()

# القسم الثاني: النشر الفوري
with col_publish:
    st.subheader("⚡ واجهة النشر الفوري")
    st.markdown("---")
    
    with st.form("real_publish_form", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان:")
        ad_sector = st.selectbox("القطاع:", ["عقار (Sraghna Immobilière)", "نقل ولوجستيك (Sraghna Media Trans)", "خدمات رقمية"])
        ad_profit = st.text_input("الفائدة / السعر:")
        ad_details = st.text_area("التفاصيل:")
        
        if st.form_submit_button("🚀 نشر العرض فوراً"):
            if ad_title:
                new_ad = {
                    "title": ad_title,
                    "sector": ad_sector,
                    "profit": ad_profit,
                    "details": ad_details + "\n\n**للتواصل:** 0691897126\n© **Sraghna Immobilière**"
                }
                if save_ad_to_db(new_ad):
                    st.session_state.instant_ads.insert(0, new_ad)
                    st.success(f"✅ تم حفظ ونشر العرض: {ad_title}")
                    st.rerun()
            else:
                st.warning("⚠️ العنوان إجباري.")

    st.markdown("### 📋 أرشيف العروض:")
    ads_container = st.container(height=250)
    with ads_container:
        for ad in st.session_state.instant_ads:
            st.info(f"**{ad['title']}** | {ad['sector']}\n\n{ad['details']}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© <strong>Sraghna Immobilière - إنتاج عامر بوخدادة</strong></p>", unsafe_allow_html=True)
