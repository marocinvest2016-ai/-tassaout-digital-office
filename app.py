import os
from google import genai
from google.genai import types
import streamlit as st
from supabase import create_client

# إعداد الصفحة
st.set_page_config(
    page_title="وكيل تساوت للعقارات | Dana", page_icon="🏢", layout="centered"
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

# تهيئة العميل بالطريقة الحديثة
client = genai.Client(
    api_key=GEMINI_API_KEY, http_options=types.HttpOptions(api_version="v1")
)


# تهيئة Supabase
@st.cache_resource
def init_supabase():
  if SUPABASE_URL and SUPABASE_KEY:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
  return None


supabase = init_supabase()

# واجهة المستخدم
st.title("🏢 وكيل تساوت للعقارات - دانا")
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

        # توليد المحتوى بالطريقة المستقرة بدون أخطاء إضافية في الـ tools
        response = client.models.generate_content(
            model="gemini-2.5-flash",
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
        st.session_state.messages.append({"role": "assistant", "content": reply})

      except Exception as e:
        st.error(f"حدث خطأ تقني: {e}")
