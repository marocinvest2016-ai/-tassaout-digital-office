import streamlit as st
import requests
import json
from PIL import Image

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide")

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق متعدد المجالات - Groq + Llama"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Meta Llama on Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.75,
        "max_tokens": 2000
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def send_whatsapp_alert(message):
    """إرسال إشعار مباشر عبر واتساب API"""
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

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
    except Exception as e:
        st.warning(f"تعذر إرسال إشعار الواتساب: {e}")

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        return call_super_ai(f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم", "Super CEO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.1\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة Streamlit =====
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption("CEO + Copywriter + Closer في وكيل واحد يخدم على Groq")

domain = st.selectbox("اختر المجال", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"])
task = st.text_area("وصف المهمة / المشروع", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة")

# قسم رفع الصور المتعددة والمعاينة البصرية
st.markdown("---")
st.subheader("🖼️ مرفقات الصور (اختياري)")
uploaded_files = st.file_uploader("اختر الصور المتعلقة بالمشروع (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"📁 تم إرفاق {len(uploaded_files)} صورة بنجاح:")
    cols = st.columns(min(len(uploaded_files), 4))
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        with cols[i % 4]:
            st.image(img, caption=file.name, use_container_width=True)

st.markdown("---")

agent = SuperOmegaAgent(domain)

if st.button("✍️ إنشاء الخطة والإعلان + إرسال واتساب", use_container_width=True):
    if task.strip():
        with st.spinner("الوكيل الذكي كيخدم على المشروع..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("تم بنجاح!")
            st.markdown(final_ad)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أولاً.")
