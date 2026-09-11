import os
import requests
import streamlit as st


# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="Tassaout Omega AI - Multi-Domain",
    page_icon="👑",
    layout="wide"
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
                "content": system_prompt.strip()
            },
            {
                "role": "user",
                "content": prompt.strip()
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1800
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=90
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        if response.ok:
            choices = data.get("choices", [])

            if not choices:
                return "❌ الخادم أرجع نتيجة فارغة."

            content = choices[0].get("message", {}).get("content", "")

            if not content:
                return "❌ لم يتم العثور على نص في نتيجة النموذج."

            return content.strip()

        error_message = (
            data.get("error", {}).get("message")
            or response.text
            or "خطأ غير معروف"
        )

        if response.status_code == 401:
            return "❌ مفتاح GROQ_API_KEY غير صحيح أو منتهي."

        if response.status_code == 429:
            return "❌ تم تجاوز الحد المسموح للطلبات. حاول لاحقاً."

        if response.status_code == 400:
            return f"❌ طلب غير صالح من Groq: {error_message}"

        return f"❌ خطأ من Groq ({response.status_code}): {error_message}"

    except requests.exceptions.Timeout:
        return "❌ انتهت مهلة الاتصال بـ Groq."

    except requests.exceptions.ConnectionError:
        return "❌ تعذر الاتصال بخادم Groq."

    except requests.exceptions.RequestException as error:
        return f"❌ خطأ في طلب Groq: {error}"

    except Exception as error:
        return f"❌ خطأ غير متوقع: {error}"


# =========================
# تقسيم رسائل واتساب
# =========================

def split_message(message, max_length=4096):
    """
    تقسيم النص إلى أجزاء لا تتجاوز 4096 حرفاً.
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
# إرسال واتساب
# =========================

def push_to_whatsapp(message_text):
    """إرسال النتيجة إلى WhatsApp Cloud API."""

    phone_id = get_secret("WHATSAPP_PHONE_NUMBER_ID")
    access_token = get_secret("WHATSAPP_ACCESS_TOKEN")
    target_number = get_secret("WHATSAPP_BUSINESS_NUMBER")
    version = get_secret("WHATSAPP_API_VERSION", "v20.0")

    missing = []

    if not phone_id:
        missing.append("WHATSAPP_PHONE_NUMBER_ID")

    if not access_token:
        missing.append("WHATSAPP_ACCESS_TOKEN")

    if not target_number:
        missing.append("WHATSAPP_BUSINESS_NUMBER")

    if missing:
        return False, "إعدادات واتساب ناقصة: " + ", ".join(missing)

    target_number = (
        str(target_number)
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
    )

    url = f"https://graph.facebook.com/{version}/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    parts = split_message(message_text, 4096)

    try:
        for index, part in enumerate(parts, start=1):
            if len(parts) > 1:
                part = (
                    f"👑 Tassaout Omega - الجزء {index}/{len(parts)}

"
                    f"{part}"
                )

            payload = {
                "messaging_product": "whatsapp",
                "to": target_number,
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": part
                }
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            try:
                data = response.json()
            except ValueError:
                data = {}

            if not response.ok:
                error_message = (
                    data.get("error", {}).get("message")
                    or response.text
                    or "خطأ غير معروف من واتساب"
                )

                return (
                    False,
                    f"فشل إرسال الجزء {index}: "
                    f"{response.status_code} - {error_message}"
                )

        return True, f"تم إرسال {len(parts)} رسالة بنجاح."

    except requests.exceptions.Timeout:
        return False, "انتهت مهلة الاتصال بواجهة واتساب."

    except requests.exceptions.ConnectionError:
        return False, "تعذر الاتصال بواجهة واتساب."

    except requests.exceptions.RequestException as error:
        return False, f"خطأ في طلب واتساب: {error}"

    except Exception as error:
        return False, f"خطأ غير متوقع: {error}"


# =========================
# واجهة المستخدم
# =========================

st.title("👑 Tassaout Omega - Multi-Domain Agentic System")

st.caption(
    "نظام ذكي متكامل لإدارة المشاريع، العقار، التجارة "
    "وإرسال التقارير إلى واتساب"
)

if "last_result" not in st.session_state:
    st.session_state["last_result"] = ""

if "last_domain" not in st.session_state:
    st.session_state["last_domain"] = ""


col1, col2 = st.columns(2)

with col1:
    domain = st.text_input(
        "مجال النشاط / القطاع",
        value="العقار وتجزئة الأراضي بقلعة السراغنة"
    )

with col2:
    agent_type = st.selectbox(
        "اختر الوكيل الذكي",
        [
            "CEO (الاستراتيجية والتخطيط الشامل)",
            "CTO (البنية التقنية والحلول الرقمية)",
            "COO (إدارة العمليات والجدولة)",
            "Copywriter & Closer (صياغة الإعلانات والمبيعات)"
        ]
    )

task_input = st.text_area(
    "أدخل تفاصيل المهمة أو المشروع:",
    height=180,
    placeholder=(
        "مثال: تسويق بقع أرضية تجارية "
        "واستقطاب المستثمرين في قلعة السراغنة..."
    )
)


if st.button("🚀 تنفيذ المهمة وتوليد الاستراتيجية", type="primary"):

    if not domain.strip():
        st.warning("المرجو إدخال مجال النشاط.")

    elif not task_input.strip():
        st.warning("المرجو إدخال وصف المهمة أولاً.")

    else:
        role_name = agent_type.split(" (", 1)[0]

        with st.spinner("جاري معالجة المهمة بالذكاء الاصطناعي..."):
            result = call_ai_engine(
                prompt=task_input,
                agent_role=role_name,
                domain_field=domain
            )

        st.session_state["last_result"] = result
        st.session_state["last_domain"] = domain

        if result.startswith("❌"):
            st.error(result)
        else:
            st.success("تم توليد النتيجة بنجاح!")
            st.markdown(result)


# =========================
# عرض وإرسال آخر نتيجة
# =========================

if st.session_state.get("last_result"):

    st.markdown("---")
    st.subheader("📄 آخر تقرير مولد")

    st.markdown(st.session_state["last_result"])

    if st.button("📱 إرسال هذه النتيجة إلى واتساب الأعمال"):

        whatsapp_message = (
            "👑 *Tassaout Omega Report*
"
            f"*المجال:* {st.session_state['last_domain']}

"
            f"{st.session_state['last_result']}"
        )

        with st.spinner("جاري الإرسال عبر WhatsApp Cloud API..."):
            success, info = push_to_whatsapp(whatsapp_message)

        if success:
            st.success(info)
        else:
            st.error(f"فشل الإرسال: {info}")
