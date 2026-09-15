import os
import requests
import streamlit as st

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="Ferraille Super Omega Agent",
    page_icon="⚙️",
    layout="wide",
)

# =========================
# إعدادات عامة
# =========================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

DEFAULT_GROQ_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
]

# =========================
# قراءة الإعدادات بأمان
# =========================
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
    return [model.strip() for model in str(models_value).split(",") if model.strip()]

# =========================
# توليد الجواب من Groq
# =========================
def call_super_ai(prompt, agent_name, domain):
    api_key = get_setting("GROQ_API_KEY")
    models = get_groq_models()

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في Streamlit Secrets.", "Error"

    if not prompt or not prompt.strip():
        return "❌ المرجو إدخال تفاصيل المهمة.", "Error"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = f"""
أنت {agent_name}، وكيل ذكي محترف ومتخصص جداً في مجال {domain} (تجارة الفِرَاي وخردة الحديد والنحاس والألومنيوم والمعادن في المغرب).

قواعد مهمة:
- استعمل الدارجة المغربية مع العربية الفصحى المهنية.
- كن عملي وواقعي جداً (الأسعار، الهوامش، المنافسين، المخاطر، القوانين المغربية).
- لا تخترع أرقاماً أو أسعار. إذا ما كانش عندك معلومة دقيقة قول "خاص نتحقق من السوق الحالي".
- ركز على الربحية، التدفق النقدي، إدارة المخاطر (السرقة، تقلب الأسعار، الزبناء السيئين، الضرائب).
- نظم الجواب بعناوين واضحة ونقاط عملية قابلة للتنفيذ فوراً.
"""

    last_error = "لم يتم الحصول على تفاصيل الخطأ."

    for model in models:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": prompt.strip()},
            ],
            "temperature": 0.65,
            "max_completion_tokens": 2200,
        }

        try:
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=90)

            try:
                data = response.json()
            except ValueError:
                data = {}

            if response.ok:
                choices = data.get("choices", [])
                if not choices:
                    last_error = f"{model}: النتيجة فارغة."
                    continue

                content = choices[0].get("message", {}).get("content", "")
                if not content:
                    last_error = f"{model}: لا يوجد نص في النتيجة."
                    continue

                st.session_state["last_model_used"] = model
                st.session_state["last_model_status"] = "✅ نجح"
                return content.strip(), model

            error_message = (
                data.get("error", {}).get("message")
                or response.text
                or "خطأ غير معروف"
            )
            last_error = f"{model} ({response.status_code}): {error_message}"

            if response.status_code == 401:
                st.session_state["last_model_status"] = "❌ مفتاح غير صالح"
                return "❌ مفتاح GROQ_API_KEY غير صحيح أو منتهي.", "Error"

            if response.status_code in (429, 400, 404):
                continue

        except requests.exceptions.Timeout:
            last_error = f"{model}: انتهت مهلة الاتصال."
            continue
        except requests.exceptions.ConnectionError:
            last_error = f"{model}: تعذر الاتصال بخادم Groq."
            continue
        except requests.exceptions.RequestException as error:
            last_error = f"{model}: خطأ في الطلب: {error}"
            continue
        except Exception as error:
            last_error = f"{model}: خطأ غير متوقع: {error}"
            continue

    st.session_state["last_model_status"] = "❌ فشل"
    return f"❌ تعذر الاتصال بنماذج Groq.\n\nتفاصيل تقنية: {last_error}", "Error"

# =========================
# تقسيم رسائل واتساب
# =========================
def split_message(message, max_length=4096):
    message = message or ""
    parts = []

    while len(message) > max_length:
        split_at = message.rfind("\n", 0, max_length)
        if split_at < max_length // 2:
            split_at = message.rfind(" ", 0, max_length)
        if split_at <= 0:
            split_at = max_length

        parts.append(message[:split_at].strip())
        message = message[split_at:].strip()

    if message:
        parts.append(message)
    return parts

# =========================
# إرسال WhatsApp
# =========================
def send_whatsapp_alert(message):
    phone_id = get_setting("WHATSAPP_PHONE_NUMBER_ID")
    access_token = get_setting("WHATSAPP_ACCESS_TOKEN")
    target_number = get_setting("WHATSAPP_BUSINESS_NUMBER")
    version = get_setting("WHATSAPP_API_VERSION", "v20.0")

    if not phone_id or not access_token or not target_number:
        return False, "إعدادات WhatsApp ناقصة في Streamlit Secrets."

    target_number = str(target_number).replace("+", "").replace(" ", "").replace("-", "")
    url = f"https://graph.facebook.com/{version}/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    parts = split_message(message, 4096)

    try:
        for index, part in enumerate(parts, start=1):
            if len(parts) > 1:
                part = f"⚙️ Ferraille Omega - الجزء {index}/{len(parts)}\n\n{part}"

            payload = {
                "messaging_product": "whatsapp",
                "to": target_number,
                "type": "text",
                "text": {"preview_url": False, "body": part},
            }

            response = requests.post(url, headers=headers, json=payload, timeout=20)

            if not response.ok:
                try:
                    data = response.json()
                except ValueError:
                    data = {}
                error_message = data.get("error", {}).get("message") or response.text or "خطأ غير معروف"
                return False, f"فشل إرسال الجزء {index}: {response.status_code} - {error_message}"

        return True, f"تم إرسال {len(parts)} رسالة بنجاح."

    except requests.exceptions.Timeout:
        return False,
