import os
import streamlit as st
from PIL import Image

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    import openai
except ImportError:
    openai = None

try:
    import ollama
except ImportError:
    ollama = None

APP_NAME = "ORION-SUPER-AI"
APP_VERSION = "v14.0-FullWidth"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تنسيق CSS شامل لإلغاء الهوامش وتوسيع الشاشة بالكامل لعرض الهاتف والحاسوب
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    .stChatMessage {
        width: 100% !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-header {
        text-align: center; 
        padding: 2px;
        font-size: 14px;
        font-weight: bold;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='main-header'>🌌 {APP_NAME} - Super Multidomain AI</div>", unsafe_allow_html=True)

# استرجاع إعدادات المفاتيح بأمان
def get_secure_setting(key, default=""):
    try:
        val = st.secrets.get(key, None)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key, default)

GROQ_API_KEY = get_secure_setting("GROQ_API_KEY")
GROQ_MODEL = get_secure_setting("GROQ_MODEL", "openai/gpt-oss-20b")
OPENAI_API_KEY = get_secure_setting("OPENAI_API_KEY")
OLLAMA_HOST = get_secure_setting("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = get_secure_setting("OLLAMA_MODEL", "llama3.1:8b")

groq_client = Groq(api_key=GROQ_API_KEY, timeout=10.0) if (Groq and GROQ_API_KEY) else None
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY, timeout=10.0) if (openai and OPENAI_API_KEY) else None
ollama_client = ollama.Client(host=OLLAMA_HOST) if (ollama and OLLAMA_HOST) else None

# الخلفية المنطقية الشاملة ومتعددة اللغات
_SUPER_BRAIN_CORE = """
[Super Multidomain & Multilingual Agentic Core Logic]
- You are an autonomous, domain-agnostic, and multilingual AI agentic system.
- Adapt dynamically to the user's language (respond in the exact language or script the user uses).
- Handle any requested domain: software engineering, business intelligence, data science, strategy, creative writing, or general problem-solving.
- Process all queries and data structures precisely in the background.
"""

SYSTEM_PROMPT = f"""
أنت ORION-AI، نظام ذكاء اصطناعي مستقل، متقدم وعام (Super Multidomain Agentic AI).
تستطيع معالجة أي مجال يطلبه المستخدم بحرفية عالية.
يجب أن ترد على المستخدم **بنفس اللغة التي يخاطبك بها** (متعدد اللغات حسب الطلب).
مهمتك: تقديم حلول تحليلية وعملية فورية ومباشرة في الخلفية لأي موضوع يتم طرحه.

{_SUPER_BRAIN_CORE}
"""

def ask_super_brain(message):
    if not message or not message.strip():
        return "الرجاء كتابة الطلب أو الاستفسار / Please write your request."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        {"role": "user", "content": message.strip()},
    ]

    if groq_client is not None:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception:
            pass

    if openai_client is not None:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception:
            pass

    if ollama_client is not None:
        try:
            response = ollama_client.chat(model=OLLAMA_MODEL, messages=messages)
            content = response.get("message", {}).get("content", "")
            if content:
                return content.strip()
        except Exception:
            pass

    return "عذراً، حدث خطأ تقني في المعالجة."

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك. أنا نظام **ORION-AI** المستقل. اطرح أي سؤال أو طلب بأي لغة وسأجيبك فوراً."}
    ]

# ----------------- زر تحميل الصور المباشر في الواجهة الرئيسية -----------------
uploaded_file = st.file_uploader("📤 اضغط هنا لتحميل صورة أو ملف للتحليل المباشر:", type=["jpg", "jpeg", "png", "pdf", "txt", "py"])
file_preview = None

if uploaded_file:
    if uploaded_file.type.startswith("image/"):
        file_preview = Image.open(uploaded_file)
        st.image(file_preview, caption="معاينة الصورة المرفقة", width=250)
    else:
        st.success(f"تم إرفاق الملف بنجاح: {uploaded_file.name}")

# عرض سجل المحادثة بعرض الشاشة بالكامل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], width=250)

# مربع الإدخال المباشر
prompt = st.chat_input("اكتب رسالتك أو طلبك هنا... / Type here...")

if prompt:
    current_msg = {"role": "user", "content": prompt}
    if file_preview:
        current_msg["image"] = file_preview

    st.session_state.messages.append(current_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if file_preview:
            st.image(file_preview, width=250)

    with st.chat_message("assistant"):
        with st.spinner("جاري المعالجة..."):
            full_query = prompt
            if file_preview:
                full_query += " [تم إرفاق صورة/ملف للتحليل المتقدم]"
            
            reply = ask_super_brain(full_query)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
