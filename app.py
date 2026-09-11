import os
import requests
import streamlit as st


# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="Tassaout Omega AI - Multi-Domain",
    page_icon="👑",
    layout="wide",
)


# =========================
# الإعدادات
# =========================

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-20b"


def get_secret(key, default=None):
    """قراءة القيمة من Streamlit Secrets أو متغيرات البيئة."""
    try:
        value = st.secrets.get(key)
    except Exception:
        value = None

    return value or os.getenv(key, default)


# =========================
# الاتصال بـ Groq
# =========================

def call_ai_engine(prompt, agent_role, domain_field):
    """توليد جواب باستعمال Groq."""

    api_key = get_secret("GROQ_API_KEY")
    model = get_secret("GROQ_MODEL", DEFAULT_MODEL)

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في Secrets."

    if not prompt or not prompt.strip():
        return "❌ المرجو إدخال تفاصيل المهمة."

    system_prompt = f"""
أنت {agent_role}، خبير محترف في مجال {domain_field}.

حلل طلب المستخدم وقدم جواباً عملياً ومنظماً.
استعمل الدارجة المغربية مع العربية الفصحى المهنية.
نظم الجواب بعناوين واضحة ونقاط مختصرة.
لا تخترع أي معلومات غير موجودة.
إذا كانت المعطيات ناقصة، وضح ما يجب توفيره.

اعرض الجواب وفق الشكل التالي:

📌 الخلاصة التنفيذية
🔍 التحليل
🛠️ الخطة العملية
⚠️ المخاطر والنقاط المهمة
✅ الخطوات التالية
"""

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt.strip(),
            },
            {
                "role": "user",
                "content": prompt.strip(),
            },
        ],
        "temperature": 0.7,
        "max_tokens": 1800,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=90,
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        if response.ok:
            choices = data.get("choices", [])

            if not choices:
                return "❌ الخادم أرجع نتيجة فارغة."

            content = choices[0].get("messa
