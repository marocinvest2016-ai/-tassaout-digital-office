import streamlit as st
import requests
import json
from PIL import Image

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide")

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق مع نظام الحماية التلقائية للموديلات"""
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

    # قائمة الموديلات المرتبة كبدائل آمنة لضمان عدم السقوط نهائياً
    fallback_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]

    last_error = ""

    for model_name in fallback_models:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.75,
            "max_tokens": 2000
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=60)
            if res.status_code == 200:
                return res.json()['choices'][0]['message']['content']
            else:
                last_error = f"Model {model_name} failed with status {res.status_code}"
        except Exception as e:
            last_error = str(e)
            continue

    return f"❌ خطأ نهائي في الاتصال بالذكاء الاصطناعي: {last_error}"

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

    def cto(self, task):
        return call_super_ai(f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}", "Super CTO Agent", self.domain)

    def coo(self, task):
        return call_super_ai(f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}", "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة Streamlit الأنيقة =====
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption("CEO + CTO + COO + Copywriter + Closer مدعوم بنظام الحماية التلقائية عبر Groq")

domain = st.selectbox("اختر المجال الأساسي للمشروع", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق الرقمي"])
task = st.text_area("وصف المهمة / المشروع بحرية تامة", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة...")

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

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧠 استراتيجية CEO", use_container_width=True):
        if task.strip():
            with st.spinner("المدير التنفيذي يضع الخطة..."):
                st.markdown(agent.ceo(task))
        else:
            st.warning("⚠️ يرجى كتابة وصف المهمة أولاً.")

with col2:
    if st.button("💻 الاستراتيجية التقنية CTO", use_container_width=True):
        if task.strip():
            with st.spinner("المدير التقني يحلل المشروع..."):
                st.markdown(agent.cto(task))
        else:
            st.warning("⚠️ يرجى كتابة وصف المهمة أولاً.")

with col3:
    if st.button("📊 خطة العمليات COO", use_container_width=True):
        if task.strip():
            with st.spinner("مدير العمليات يجهز الجدول الزمني..."):
                st.markdown(agent.coo(task))
        else:
            st.warning("⚠️ يرجى كتابة وصف المهمة أولاً.")

st.markdown("---")

if st.button("✍️ توليد الإعلان التسويقي الاحترافي + إرسال واتساب", use_container_width=True):
    if task.strip():
        with st.spinner("جارٍ صياغة الإعلان وإرسال التنبيه عبر واتساب..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("✨ تم إنشاء الإعلان وإرساله بنجاح!")
            st.markdown(final_ad)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أولاً.")
