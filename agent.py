import streamlit as st
import requests

GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.2-11b-vision-preview",
    "llama-3.3-70b-versatile",
]

def call_super_ai(prompt, agent_name, domain):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' "
        "powered by Meta Llama on Groq. Think step by step. "
        "Respond in Moroccan Arabic Darija + العربية الفصحى."
    )

    last_error = None
    for model in GROQ_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.75,
            "max_completion_tokens": 2000
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=90)

            if res.status_code in (404, 400, 429):
                last_error = f"⚠️ {model} غير متاح ({res.status_code}). جاري البديل..."
                continue

            res.raise_for_status()
            st.session_state.last_model_used = model
            st.session_state.last_model_status = "✅ نجح"
            return res.json()["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            last_error = f"⏱️ {model} timeout."
            continue
        except Exception as e:
            last_error = f"❌ {model}: {e}"
            continue

    st.session_state.last_model_status = "❌ فشل"
    return "❌ تعذر الاتصال بالنماذج. " + str(last_error)

def send_whatsapp_alert(message):
    try:
        phone_id = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
        access_token = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
        target_number = st.secrets.get("WHATSAPP_BUSINESS_NUMBER")
        version = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

        if not all([phone_id, access_token, target_number]):
            return

        url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": message[:4096]}
        }
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        prompt = f"""بصفتك CEO فائق، ضع خطة استراتيجية لـ {self.domain}: {task}.

المطلوب:
1. SWOT
2. الميزة التنافسية
3. خطة 90 يوم
4. KPIs

جاوب بالدارجة + الفصحى."""
        return call_super_ai(prompt, "CEO", self.domain)

    def cto(self, task):
        prompt = f"""بصفتك CTO فائق، اقترح Tech Stack لـ {task} في {self.domain}.

المطلوب:
1. البنية التقنية
2. الأتمتة
3. استهداف رقمي
4. أمان

جاوب بالدارجة + الفصحى."""
        return call
