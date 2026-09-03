import streamlit as st
import requests
import json
from supabase import create_client

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide")

# إعداد اتصال Supabase (عبر Secrets)
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "") or st.secrets.get("SUPABASE_KEY", "")
    if url and key:
        return create_client(url, key)
    return None

supabase = init_supabase()

def save_report_to_supabase(project_name, domain, content):
    """حفظ التقرير أو الخطة في جدول tassaout_reports"""
    if not supabase:
        return
    try:
        payload = {
            "project_name": project_name,
            "authority_signature": domain,
            "communication_channel": "streamlit_ui",
            "report_content": content,
            "metadata": {"source": "OMEGA Super Agentic AI", "version": "4.1"}
        }
        supabase.table("tassaout_reports").insert(payload).execute()
    except Exception as e:
        print(f"Database error: {e}")

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
        "model": "llama-3.1-70b-versatile",
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
        res = call_super_ai(f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم", "Super CEO Agent", self.domain)
        save_report_to_supabase(task, f"{self.domain} - CEO", res)
        return res

    def cto(self, task):
        res = call_super_ai(f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}", "Super CTO Agent", self.domain)
        save_report_to_supabase(task, f"{self.domain} - CTO", res)
        return res

    def coo(self, task):
        res = call_super_ai(f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}", "Super COO Agent", self.domain)
        save_report_to_supabase(task, f"{self.domain} - COO", res)
        return res

    def copywriter(self, plan, task):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.1\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        save_report_to_supabase(task, f"{self.domain} - Copywriter", ad)
        return ad

    def closer(self, ad, task):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        res = call_super_ai(prompt, "Super Closer Agent", self.domain)
        save_report_to_supabase(task, f"{self.domain} - Closer", res)
        return res

# ===== واجهة Streamlit =====
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption("CEO + CTO + COO + Copywriter + Closer في وكيل واحد يخدم على Groq + Supabase")

domain = st.selectbox("اختر المجال", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"])
task = st.text_area("وصف المهمة / المشروع", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة")

agent = SuperOmegaAgent(domain)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧠 خطة CEO"):
        if task:
            with st.spinner("المدير التنفيذي كيخدم..."):
                st.markdown(agent.ceo(task))
        else:
            st.warning("المرجو إدخال وصف المهمة أولاً.")
with col2:
    if st.button("💻 خطة CTO"):
        if task:
            with st.spinner("المدير التقني كيخدم..."):
                st.markdown(agent.cto(task))
            else:
                st.warning("المرجو إدخال وصف المهمة أولاً.")
with col3:
    if st.button("📊 خطة COO"):
        if task:
            with st.spinner("مدير العمليات كيخدم..."):
                st.markdown(agent.coo(task))
            else:
                st.warning("المرجو إدخال وصف المهمة أولاً.")

if st.button("✍️ إنشاء إعلان + إرسال واتساب"):
    if task:
        with st.spinner("الكاتب والمغلق كيخدمو..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan, task)
            final_ad = agent.closer(ad, task)
            st.success("تم بنجاح حفظ النتائج وإرسال الإشعار!")
            st.markdown(final_ad)
    else:
        st.warning("المرجو إدخال وصف المهمة أولاً.")
