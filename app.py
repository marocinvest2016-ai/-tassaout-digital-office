import os
from google import genai
from google.genai import types
import streamlit as st
from supabase import create_client

# إعداد الصفحة
st.set_page_config(
    page_title="Tassaout Mega Fort & Dana AI", page_icon="👑", layout="centered"
)

# جلب المفاتيح بأمان
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get(
    "GEMINI_API_KEY"
)
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")

if not GEMINI_API_KEY:
    st.error("المرجو إعداد `GEMINI_API_KEY` في إعدادات التطبيق.")
    st.stop()

# تهيئة العميل بالطريقة الحديثة الموصى بها
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(api_version="v1beta"),
)

# تهيئة Supabase
@st.cache_resource
def init_supabase():
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = init_supabase()

# العنوان الرئيسي للمنصة المدمجة
st.title("👑 Tassaout Mega Fort & Dana Real Estate AI")
st.markdown(
    "المنصة السيادية المتكاملة: الراصد الذكي والاستوديوهات العشرة + وكيل"
    " تساوت للعقارات (قلعة السراغنة ومراكش)."
)

# القائمة الجانبية أو التبويبات لاختيار وضع العمل
app_mode = st.sidebar.selectbox(
    "اختر النظام التشغيلي:",
    [
        "👑 Tassaout Mega Fort (الراصد والاستوديوهات)",
        "🏢 وكيل تساوت للعقارات | دانا (Chat)",
    ],
)

if app_mode == "👑 Tassaout Mega Fort (الراصد والاستوديوهات)":
    st.subheader("إدارة الاستوديوهات والراصد السيادي (A1 - A10)")

    # قائمة الاستوديوهات العشرة كاملة
    studios = {
        "1. A - Iconic Studio ($299)": "portrait pro",
        "2. A2 - Content Factory ($149)": "reels/tiktok",
        "3. A3 - Analog Atelier ($199)": "film look",
        "4. A4 - Product Factory ($249)": "e-commerce",
        "5. A5 - Mobile Storytellers ($99)": "vlog",
        "6. A6 - Video Stage ($349)": "ciné",
        "7. A7 - Beauty Lab ($279)": "retouche IA",
        "8. A8 - Corporate Stage ($399)": "linkedin",
        "9. A9 - Family House ($179)": "famille",
        "10. A10 - UGC Factory ($129)": "ads",
    }

    mode = st.radio(
        "اختر وضع التشغيل:", ["الراصد السيادي (Agentic Mode)", "اختيار يدوي"]
    )

    selected_studio = None
    if mode == "الراصد السيادي (Agentic Mode)":
        st.info("🤖 الراصد المكاني والزماني والجوي يعمل تلقائياً...")
        selected_studio = "A7 - Beauty Lab (الافتراضي للراصد)"
    else:
        selected_studio = st.selectbox("اختر الستوديو:", list(studios.keys()))

    uploaded_file = st.file_uploader(
        "تحميل صورة للمعالجة التفاعلية", type=["jpg", "jpeg", "png"]
    )
    user_prompt = st.text_input("أدخل الأمر النصي السيادي:")

    if st.button("تنفيذ الأمر السيادي 🚀"):
        with st.spinner("جاري المعالجة داخل النظام..."):
            try:
                # بناء محتوى ذكي حسب وجود صورة
                contents = []
                if uploaded_file is not None:
                    contents.append(uploaded_file)
                contents.append(
                    f"Execute Tassaout Mega Fort command for studio:"
                    f" {selected_studio} with prompt: {user_prompt}"
                )

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "أنت النظام السيادي لـ Tassaout Mega Fort AI. أجب باحترافية"
                            " وبالدارجة المغربية أو العربية حسب السياق."
                        ),
                        temperature=0.7,
                    ),
                )
                st.success("تم التنفيذ بنجاح ✅")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

else:
    st.subheader("🏢 وكيل تساوت للعقارات - دانا")
    st.markdown(
        "مرحباً! أنا **دانا**، مساعدتك الذكية للعقارات في قلعة السراغنة ومراكش."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("اطرح سؤالك العقاري أو استفسر عن أي جديد..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    system_instruction = (
                        "أنت 'دانا'، مساعدة ذكية ومحترفة خاصة بـ 'وكيل تساوت للعقارات'"
                        " (Tassaout Real Estate) في قلعة السراغنة ومراكش. تتحدثين بلطف"
                        " واحترافية (باللغة العربية والدارجة المغربية عند الحاجة)."
                        " مسؤولة عن عرض الشقق، البقع، الفيلات، وتسهيل التواصل على الرقم"
                        " 0691897126."
                    )

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                            max_output_tokens=800,
                        ),
                    )

                    reply = (
                        response.text
                        if response and response.text
                        else "عذراً، لم أتمكن من معالجة طلبك حالياً."
                    )
                    st.markdown(reply)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply}
                    )

                except Exception as e:
                    st.error(f"حدث خطأ تقني: {e}")
