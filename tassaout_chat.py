
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="تساوت | الوكيل الذكي",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="expanded",
)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

DEFAULT_GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
]

SPECIALTIES = {
    "العقار والأعمال": "خبير عقاري واستشاري أعمال محترف في قلعة السراغنة ومراكش.",
    "القانون": "مستشار قانوني متخصص في القانون المغربي (عقاري، تجاري، شغل).",
    "الهندسة المدنية والمعمارية": "مهندس مدني ومعماري استشاري.",
    "الهندسة الصناعية والميكانيكية": "مهندس صناعي وميكانيكي للمصانع والشركات.",
    "الهندسة الفلاحية": "مهندس فلاحي استشاري.",
    "الديكور والتصميم": "مصمم ديكور داخلي ومصمم عام محترف.",
    "التصوير الفوتوغرافي": "مصور فوتوغرافي احترافي.",
    "الثقافة العالمية": "خبير في الثقافة العالمية والتواصل بين الثقافات.",
    "عام / منسق": "منسق ذكي متعدد التخصصات.",
}

def get_setting(key, default=""):
    try:
        value = st.secrets.get(key, default)
    except Exception:
        value = default
    return value or os.getenv(key, default)

def get_groq_models():
    models_value = get_setting("GROQ_MODELS", "")
    if not models_value:
        return DEFAULT_GROQ_MODELS
    if isinstance(models_value, list):
        return models_value
    return [m.strip() for m in str(models_value).split(",") if m.strip()]

def call_groq(messages, system_prompt):
    api_key = get_setting("GROQ_API_KEY")
    models = get_groq_models()

    if not api_key:
        return "❌ مفتاح GROQ_API_KEY غير موجود.", "Error"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = "خطأ غير معروف"

    for model in models:
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "temperature": 0.6,
            "max_completion_tokens": 2500,
        }

        try:
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=90)
            data = response.json() if response.content else {}

            if response.ok:
                choices = data.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    if content:
                        st.session_state["last_model"] = model
                        return content.strip(), model

            error_msg = data.get("error", {}).get("message") or response.text
            last_error = f"{model}: {error_msg}"

            if response.status_code == 401:
                return "❌ مفتاح GROQ_API_KEY غير صحيح.", "Error"
            if response.status_code in (429, 400, 404):
                continue

        except Exception as e:
            last_error = f"{model}: {str(e)}"
            continue

    return f"❌ تعذر الاتصال بنماذج Groq.\n{last_error}", "Error"

def build_system_prompt(specialty, custom_instructions):
    base = SPECIALTIES.get(specialty, SPECIALTIES["عام / منسق"])
    prompt = f"""أنت وكيل ذكي محترف تابع لـ «مكتب تساوت الرقمي» في قلعة السراغنة.

التخصص الحالي: {specialty}
{base}

قواعد:
- استخدم العربية الفصحى مع الدارجة المغربية عند الحاجة.
- كن عملياً ومنظماً.
- لا تخترع معلومات.
- إذا نقصت معلومات، اطلبها.
"""
    if custom_instructions and custom_instructions.strip():
        prompt += f"\n\nتعليمات إضافية:\n{custom_instructions.strip()}"
    return prompt.strip()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "custom_instructions" not in st.session_state:
    st.session_state.custom_instructions = ""
if "selected_specialty" not in st.session_state:
    st.session_state.selected_specialty = "عام / منسق"
if "last_model" not in st.session_state:
    st.session_state.last_model = ""

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 👑 تساوت الذكي")
    specialty = st.selectbox(
        "التخصص",
        options=list(SPECIALTIES.keys()),
        index=list(SPECIALTIES.keys()).index(st.session_state.selected_specialty),
    )
    st.session_state.selected_specialty = specialty

    custom_inst = st.text_area(
        "تعليمات إضافية",
        value=st.session_state.custom_instructions,
        height=100,
        placeholder="مثال: ركز على الجانب القانوني...",
    )
    st.session_state.custom_instructions = custom_inst

    if st.button("🗑️ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.last_model:
        st.success(f"النموذج: {st.session_state.last_model}")

# الواجهة الرئيسية
st.markdown(f"### 👑 تساوت | الوكيل الذكي")
st.caption(f"التخصص الحالي: **{specialty}**")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("أكتب سؤالك أو تعليماتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]]
    system_prompt = build_system_prompt(st.session_state.selected_specialty, st.session_state.custom_instructions)

    with st.chat_message("assistant"):
        with st.spinner("كيفكر..."):
            reply, model = call_groq(history, system_prompt)

        if model == "Error":
            st.error(reply)
        else:
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
