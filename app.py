import os
import streamlit as st
from groq import Groq
import ollama


# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="دانا الوكيلة العقارية",
    page_icon="👑",
    layout="centered",
)


# =========================
# قراءة الإعدادات بأمان
# =========================

def get_setting(key, default=""):
    """
    يقرأ الإعداد من Streamlit Secrets أو من متغيرات البيئة.
    إذا لم يوجد، يعيد قيمة فارغة أو القيمة الافتراضية.
    """
    try:
        value = st.secrets.get(key, default)
    except Exception:
        value = default

    return value or os.getenv(key, default)


GROQ_KEY = get_setting("GROQ_API_KEY")
GROQ_MODEL = get_setting("GROQ_MODEL", "openai/gpt-oss-20b")

OLLAMA_HOST = get_setting(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

OLLAMA_MODEL = get_setting(
    "OLLAMA_MODEL",
    "llama3.2",
)


# =========================
# تهيئة العملاء
# =========================

groq_client = None
ollama_client = None

if GROQ_KEY:
    groq_client = Groq(
        api_key=GROQ_KEY,
        timeout=10.0,
    )

if OLLAMA_HOST:
    ollama_client = ollama.Client(
        host=OLLAMA_HOST,
    )


# =========================
# تعليمات دانا
# =========================

SYSTEM_PROMPT = """
أنت دانا، وكيلة عقارية ذكية من وكالة تساوت بقلعة السراغنة.

تحدثي بالدارجة المغربية بطريقة ودودة ومحترفة، ويمكنك استعمال العربية الفصحى عند الحاجة.

مهمتك:
- مساعدة العملاء في البحث عن العقارات.
- تقديم معلومات واضحة عن العقار.
- طرح أسئلة مفيدة لفهم طلب العميل.
- اقتراح حجز موعد للمعاينة.
- جمع الميزانية، المنطقة، المساحة، ونوع العقار.
- عدم اختراع أسعار أو مساحات أو معلومات غير موجودة.
- إذا كانت المعلومات ناقصة، صرحي بذلك واطلبي التفاصيل اللازمة.
- لا تؤكدي الحجز النهائي إلا بعد موافقة المسؤول.
"""


def ask_dana(message):
    """
    تحاول الإجابة باستعمال Groq أولاً،
    ثم تستعمل Ollama كخطة احتياطية.
    """

    if not message or not message.strip():
        return "عافاك كتب ليا شنو العقار أو المعلومة اللي باغي تعرف عليها.", "Error"

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.strip(),
        },
        {
            "role": "user",
            "content": message.strip(),
        },
    ]

    # =========================
    # المحاولة الأولى: Groq
    # =========================

    if groq_client is not None:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )

            content = response.choices[0].message.content

            if content:
                return content.strip(), "Groq"

        except Exception:
            pass

    # =========================
    # الخطة الثانية: Ollama
    # =========================

    if ollama_client is not None:
        try:
            response = ollama_client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
            )

            content = response.get("message", {}).get("content", "")

            if content:
                return content.strip(), "Ollama"

        except Exception:
            pass

    return (
        "سمح ليا، وقع مشكل تقني مؤقت. "
        "عاود المحاولة من بعد أو تواصل مع الوكالة مباشرة.",
        "Error",
    )


# =========================
# واجهة المحادثة
# =========================

st.title("👑 دانا الوكيلة العقارية")

st.caption(
    "وكيلة ذكية لمساعدتك في البحث عن العقارات وحجز المعاينات"
)


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input(
    "سوليني على أي عقار..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("دانا كتفكر..."):
            reply, brain = ask_dana(prompt)

        st.markdown(reply)

        if brain != "Error":
            st.caption(f"المحرك المستعمل: {brain}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )
