import os
import requests
import streamlit as st


# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="Tassaout Super Omega Agent",
    page_icon="👑",
    layout="wide",
)


# =========================
# إعدادات عامة
# =========================

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

DEFAULT_GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
]


# =========================
# قراءة الإعدادات بأمان
# =========================

def get_setting(key, default=""):
    """
    قراءة القيمة من Streamlit Secrets أو متغيرات البيئة.
    """
    try:
        value = st.secrets.get(key, default)
    except Exception:
        value = default

    return value or os.getenv(key, default)


def get_groq_models():
    """
    قراءة قائمة النماذج من Secrets.
    إذا لم توجد، استعمال القائمة الافتراضية.
    """

    models_value = get_setting("GROQ_MODELS", "")

    if not models_value:
        return DEFAULT_GROQ_MODELS

    if isinstance(models_value, list):
        return models_value

    return [
        model.strip()
        for model in str(models_value).split(",")
        if model.strip()
    ]


# =========================
# توليد الجواب من Groq
# =========================

def call_super_ai(prompt, agent_name, domain):
    """
    إرسال الطلب إلى Groq مع تجربة عدة نماذج بالترتيب.
    """

    api_key = get_setting("GROQ_API_KEY")
    models = get_groq_models()

    if not api_key:
        return (
            "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في Streamlit Secrets.",
            "Error",
        )

    if not prompt or not prompt.strip():
        return (
            "❌ المرجو إدخال تفاصيل المهمة.",
            "Error",
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = f"""
أنت {agent_name}، وكيل ذكي محترف ومتخصص في مجال {domain}.

حلل الطلب بعمق، لكن لا تعرض التفكير الداخلي التفصيلي.
قدم جواباً عملياً ومنظماً وقابلاً للتنفيذ.
استعمل الدارجة المغربية مع العربية الفصحى المهنية.
لا تخترع أرقاماً أو معلومات غير موجودة.
إذا كانت المعطيات ناقصة، اذكر ما يجب توفيره.

نظم الجواب بعناوين واضحة ونقاط عملية.
"""

    last_error = "لم يتم الحصول على تفاصيل الخطأ."

    for model in models:
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
            "max_completion_tokens": 2000,
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
                    last_error = f"{model}: النتيجة فارغة."
                    continue

                content = (
                    choices[0]
                    .get("message", {})
                    .get("content", "")
                )

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

            last_error = (
                f"{model} ({response.status_code}): "
                f"{error_message}"
            )

            if response.status_code == 401:
                st.session_state["last_model_status"] = "❌ مفتاح غير صالح"
                return (
                    "❌ مفتاح GROQ_API_KEY غير صحيح أو منتهي.",
                    "Error",
                )

            if response.status_code == 429:
                continue

            if response.status_code in (400, 404):
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

    return (
        "❌ تعذر الاتصال بنماذج Groq.

"
        f"تفاصيل تقنية: {last_error}",
        "Error",
    )


# =========================
# تقسيم رسائل واتساب
# =========================

def split_message(message, max_length=4096):
    """
    تقسيم النص إلى أجزاء مناسبة لواتساب.
    """

    message = message or ""
    parts = []

    while len(message) > max_length:
        split_at = message.rfind("
", 0, max_length)

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
    """
    إرسال التقرير إلى WhatsApp Cloud API.
    """

    phone_id = get_setting("WHATSAPP_PHONE_NUMBER_ID")
    access_token = get_setting("WHATSAPP_ACCESS_TOKEN")
    target_number = get_setting("WHATSAPP_BUSINESS_NUMBER")
    version = get_setting("WHATSAPP_API_VERSION", "v20.0")

    if not phone_id or not access_token or not target_number:
        return (
            False,
            "إعدادات WhatsApp ناقصة في Streamlit Secrets.",
        )

    target_number = (
        str(target_number)
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
    )

    url = f"https://graph.facebook.com/{version}/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    parts = split_message(message, 4096)

    try:
        for index, part in enumerate(parts, start=1):

            if len(parts) > 1:
                part = (
                    f"👑 Tassaout Omega - الجزء "
                    f"{index}/{len(parts)}

"
                    f"{part}"
                )

            payload = {
                "messaging_product": "whatsapp",
                "to": target_number,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": part,
                },
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=20,
            )

            if not response.ok:
                try:
                    data = response.json()
                except ValueError:
                    data = {}

                error_message = (
                    data.get("error", {}).get("message")
                    or response.text
                    or "خطأ غير معروف"
                )

                return (
                    False,
                    f"فشل إرسال الجزء {index}: "
                    f"{response.status_code} - "
                    f"{error_message}",
                )

        return True, f"تم إرسال {len(parts)} رسالة بنجاح."

    except requests.exceptions.Timeout:
        return False, "انتهت مهلة الاتصال بواجهة WhatsApp."

    except requests.exceptions.ConnectionError:
        return False, "تعذر الاتصال بواجهة WhatsApp."

    except requests.exceptions.RequestException as error:
        return False, f"خطأ في طلب WhatsApp: {error}"

    except Exception as error:
        return False, f"خطأ غير متوقع: {error}"


# =========================
# الوكيل الذكي
# =========================

class SuperOmegaAgent:

    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        prompt = f"""
بصفتك CEO محترفاً، ضع خطة استراتيجية عملية في مجال {self.domain}.

المهمة:
{task}

المطلوب:
1. الخلاصة التنفيذية.
2. تحليل SWOT.
3. الميزة التنافسية.
4. خطة عملية لمدة 90 يوماً.
5. مؤشرات الأداء KPIs.
6. المخاطر والحلول.
"""

        return call_super_ai(
            prompt,
            "CEO",
            self.domain,
        )

    def cto(self, task):
        prompt = f"""
بصفتك CTO محترفاً، اقترح حلولاً تقنية وهندسية في مجال {self.domain}.

المهمة:
{task}

المطلوب:
1. البنية التقنية المناسبة.
2. الأدوات والبرمجيات.
3. الأتمتة الرقمية.
4. تكامل الذكاء الاصطناعي.
5. حماية البيانات والمفاتيح.
6. خطة تنفيذ تدريجية.
"""

        return call_super_ai(
            prompt,
            "CTO",
            self.domain,
        )

    def coo(self, task):
        prompt = f"""
بصفتك COO محترفاً، ضع خطة تشغيلية في مجال {self.domain}.

المهمة:
{task}

المطلوب:
1. خطة التشغيل اليومية.
2. توزيع المسؤوليات.
3. إدارة الموارد.
4. سير العمل.
5. معايير الجودة.
6. مؤشرات الكفاءة.
7. المخاطر التشغيلية والحلول.
"""

        return call_super_ai(
            prompt,
            "COO",
            self.domain,
        )


# =========================
# واجهة Streamlit
# =========================

st.title("👑 Tassaout Super Omega Agent")

st.caption(
    "وكيل ذكي للاستراتيجية والتقنية والتشغيل والتسويق"
)


if "last_model_used" not in st.session_state:
    st.session_state["last_model_used"] = ""

if "last_model_status" not in st.session_state:
    st.session_state["last_model_status"] = ""


domain = st.text_input(
    "مجال النشاط",
    value="العقار وتجزئة الأراضي بقلعة السراغنة",
)

agent_type = st.selectbox(
    "اختر نوع الوكيل",
    [
        "CEO",
        "CTO",
        "COO",
    ],
)

task = st.text_area(
    "اكتب المهمة",
    height=180,
    placeholder=(
        "مثال: أريد خطة لتسويق بقع أرضية تجارية "
        "واستقطاب المستثمرين..."
    ),
)


if st.button("🚀 تنفيذ المهمة", type="primary"):

    if not domain.strip():
        st.warning("المرجو إدخال مجال النشاط.")

    elif not task.strip():
        st.warning("المرجو إدخال المهمة.")

    else:
        agent = SuperOmegaAgent(domain)

        with st.spinner("جاري تحليل المهمة..."):

            if agent_type == "CEO":
                result, brain = agent.ceo(task)

            elif agent_type == "CTO":
                result, brain = agent.cto(task)

            else:
                result, brain = agent.coo(task)

        if brain == "Error":
            st.error(result)
        else:
            st.success(
                f"تم توليد النتيجة باستعمال النموذج: {brain}"
            )
            st.markdown(result)

            st.session_state["last_result"] = result
            st.session_state["last_domain"] = domain


if st.session_state.get("last_result"):

    st.markdown("---")
    st.subheader("📄 آخر تقرير")

    st.markdown(
        st.session_state["last_result"]
    )

    if st.button("📱 إرسال التقرير إلى WhatsApp"):

        whatsapp_message = (
            "👑 *Tassaout Super Omega Report*
"
            f"*المجال:* "
            f"{st.session_state.get('last_domain', '')}

"
            f"{st.session_state['last_result']}"
        )

        with st.spinner("جاري الإرسال إلى WhatsApp..."):
            success, info = send_whatsapp_alert(
                whatsapp_message
            )

        if success:
            st.success(info)
        else:
            st.error(info)


with st.sidebar:
    st.subheader("📊 حالة النظام")

    if st.session_state.get("last_model_used"):
        st.write(
            f"النموذج: "
            f"{st.session_state['last_model_used']}"
        )

    if st.session_state.get("last_model_status"):
        st.write(
            st.session_state["last_model_status"]
        )
