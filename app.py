import streamlit as st
import requests
import json

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide")

def get_available_groq_model(api_key):
    """فحص النماذج المتاحة فعلياً في حساب Groq واختيار المتاح بتدرج آمن"""
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # قائمة النماذج المفضلة مرتبة حسب الأولوية
    preferred_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json().get("data", [])
            available_ids = [m["id"] for m in data]
            
            # اختيار أول نموذج متوفر من القائمة المفضلة
            for model in preferred_models:
                if model in available_ids:
                    return model
            # إذا وُجد أي نموذج آخر كبديل
            if available_ids:
                return available_ids[0]
    except Exception:
        pass
        
    # قيمة افتراضية احتياطية كـ Fallback
    return "llama-3.1-8b-instant"

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

    # جلب النموذج المتاح ديناميكياً لتجنب مشاكل توقف النماذج
    active_model = get_available_groq_model(api_key)

    payload = {
        "model": active_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.75,
        "max_completion_tokens": 2000
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        
        # نظام Fallback فوري في حال أعطى الخادم خطأ عدم توفر النموذج
        if res.status_code == 404 and active_model != "llama-3.1-8b-instant":
            payload["model"] = "llama-3.1-8b-instant"
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

    def cto(self, task):
        return call_super_ai(f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}", "Super CTO Agent", self.domain)

    def coo(self, task):
        return call_super_ai(f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}", "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.2\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة Streamlit =====
st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
st.caption("CEO + CTO + COO + Copywriter + Closer في وكيل واحد يخدم على Groq مع فحص تلقائي للنماذج المتاحة")

domain = st.selectbox("اختر المجال", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"])
task = st.text_area("وصف المهمة / المشروع", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة")

agent = SuperOmegaAgent(domain)

# عرض النموذج المكتشف حالياً في حسابك بناءً على فحص الـ API
api_key_val = st.secrets.get("GROQ_API_KEY", "")
if api_key_val:
    active_model_name = get_available_groq_model(api_key_val)
    st.info(f"🤖 **النموذج النشط المكتشف تلقائياً:** `{active_model_name}`")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧠 خطة CEO"):
        with st.spinner("المدير التنفيذي كيخدم..."):
            st.markdown(agent.ceo(task))
with col2:
    if st.button("💻 خطة CTO"):
        with st.spinner("المدير التقني كيخدم..."):
            st.markdown(agent.cto(task))
with col3:
    if st.button("📊 خطة COO"):
        with st.spinner("مدير العمليات كيخدم..."):
            st.markdown(agent.coo(task))

if st.button("✍️ إنشاء إعلان + إرسال واتساب"):
    with st.spinner("الكاتب كيكتب الإعلان..."):
        plan = agent.ceo(task)
        ad = agent.copywriter(plan)
        final_ad = agent.closer(ad)
        st.success("تم!")
        st.markdown(final_ad)
