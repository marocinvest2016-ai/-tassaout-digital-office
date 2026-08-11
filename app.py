import streamlit as st
import os
import google.generativeai as genai

# --- إعدادات الصفحة السيادية ---
st.set_page_config(
    page_title="SRAGHNA IMMOBILIÈRE - التوأم الذكي السيادي",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- إعداد مفتاح الـ API لـ Gemini ---
API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = None

# --- تهيئة الحالة (Session State) ---
if "gemini_logs" not in st.session_state:
    st.session_state.gemini_logs = [
        {"role": "assistant", "content": "👑 أهلاً بك سيدي الرئيس عامر بوخدادة. أنا التوأم الذكي الحقيقي المدعوم بالذكاء الاصطناعي، جاهز تماماً لتلقي أوامرك وإدارتك في Sraghna Immobilière."}
    ]

if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = []

# --- تصميم واجهة مستقلة مقسومة لعمودين (التوأم الذكي الحقيقي + النشر الفوري) ---
col_ai, col_publish = st.columns(2, gap="large")

# ==========================================
# القسم الأول: واجهة التوأم الذكي (Gemini الحقيقي)
# ==========================================
with col_ai:
    st.subheader("🧠 التوأم الذكي السيادي (Gemini AI)")
    st.markdown("---")
    
    chat_container = st.container(height=450)
    
    with chat_container:
        for msg in st.session_state.gemini_logs:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_query = st.chat_input("اطرح أمرك أو استفسارك على التوأم الذكي...", key="real_gemini_input")

    if user_query:
        st.session_state.gemini_logs.append({"role": "user", "content": user_query})
        
        ai_reply = ""
        if model and API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            try:
                system_prompt = "أنت التوأم الذكي والوكيل السيادي لـ عامر بوخدادة، مدير Sraghna Immobilière بقلعة السراغنة ومراكش. أجب باحترافية وبصيغة تليق بالرئيس."
                response = model.generate_content(f"{system_prompt}\n\nالسؤال/الأمر: {user_query}")
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"👑 سيدي الرئيس، حدث خطأ في الاتصال بالسحابة الذكية تأكد من مفتاح الـ API. (الخطأ: {str(e)})"
        else:
            ai_reply = f"👑 سيدي الرئيس عامر بوخدادة، بصفتي وكيلك الذكي، أؤكد لك استلام الأمر ('{user_query}'). يرجى إدخال مفتاح Google Gemini API الفعلي في الـ Secrets لتفعيل الذكاء الاصطناعي الحقيقي."

        st.session_state.gemini_logs.append({"role": "assistant", "content": ai_reply})
        st.rerun()

# ==========================================
# القسم الثاني: واجهة النشر الفوري
# ==========================================
with col_publish:
    st.subheader("⚡ واجهة النشر الفوري")
    st.markdown("---")
    
    with st.form("real_publish_form", clear_on_submit=True):
        ad_title = st.text_input("عنوان الإعلان أو العقار:")
        ad_sector = st.selectbox("القطاع:", ["عقار (Sraghna Immobilière)", "نقل ولوجستيك (Sraghna Media Trans)", "خدمات رقمية"])
        ad_profit = st.text_input("الفائدة المطلوبة / السعر:")
        ad_details = st.text_area("تفاصيل العرض والمواصفات:")
        
        submit_btn = st.form_submit_button("🚀 نشر العرض فوراً")
        
        if submit_btn:
            if ad_title:
                new_ad = {
                    "title": ad_title,
                    "sector": ad_sector,
                    "profit": ad_profit,
                    "details": ad_details + "\n\n**للتواصل:** 0691897126\n© **Sraghna Immobilière**"
                }
                st.session_state.instant_ads.insert(0, new_ad)
                st.success(f"✅ تم نشر العرض بنجاح: {ad_title}")
                st.rerun()
            else:
                st.warning("⚠️ يرجى إدخال عنوان الإعلان على الأقل.")

    st.markdown("### 📋 العروض والخدمات المنشورة:")
    ads_container = st.container(height=250)
    with ads_container:
        if st.session_state.instant_ads:
            for idx, ad in enumerate(st.session_state.instant_ads):
                st.info(f"**{ad['title']}** | القطاع: {ad['sector']} | الفائدة: {ad['profit']}\n\n{ad['details']}")
        else:
            st.info("لا توجد عروض منشورة حتى الآن.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© <strong>Sraghna Immobilière - إنتاج عامر بوخدادة - جميع الحقوق محفوظة</strong></p>", unsafe_allow_html=True)
