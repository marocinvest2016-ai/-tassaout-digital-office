import streamlit as st
import requests
import json

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide")

def call_super_ai(prompt, agent_name, domain, selected_model):
    """محرك الذكاء الاصطناعي الفائق متعدد المجالات - Groq مع دعم النماذج المفتوحة المتعددة"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Open Source models on Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    payload = {
        "model": selected_model, # النموذج المختار من طرف المستخدم عبر الواجهة
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
    def __init__(self, domain, selected_model):
        self.domain = domain
        self.selected_model = selected_model

    def ceo(self, task):
        return call_super_ai(f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم", "Super CEO Agent", self.domain, self.selected_model)

    def cto(self, task):
        return call_super_ai(f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}", "Super CTO Agent", self.domain, self.selected_model)

    def coo(self, task):
        return call_super_ai(f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}", "Super COO Agent", self.domain, self.selected_model)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain, self.selected_model)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.2\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain, self.selected_model)

# ===== واجهة Streamlit =====
st.title("👑 OMEGA Super Agentic AI - متعدد النماذج والمجالات")
st.caption("النظام الذكي المتكامل المدعوم بنماذج الذكاء الاصطناعي المفتوحة على منصة Groq")

# شريط جانبي أو إعدادات لاختيار النموذج والمجال
col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    domain = st.selectbox("اختر المجال الاستراتيجي", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"])

with col_opt2:
    selected_model = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي (Open Source Models)",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32k",
            "gemma2-9b-it",
            "llama-3.1-8b-instant"
        ]
    )

task = st.text_area("وصف المهمة / المشروع", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة")

agent = SuperOmegaAgent(domain, selected_model)

# خيارات الأزرار: خطط مفردة (اختياري) أو التوليد التلقائي الشامل المتكامل
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("🧠 تشغيل استراتيجية CEO"):
        with st.spinner(f"المدير التنفيذي يعمل عبر نموذج {selected_model}..."):
            st.markdown(agent.ceo(task))
with col_btn2:
    if st.button("💻 تشغيل استراتيجية CTO"):
        with st.spinner(f"المدير التقني يعمل عبر نموذج {selected_model}..."):
            st.markdown(agent.cto(task))
with col_btn3:
    if st.button("📊 تشغيل استراتيجية COO"):
        with st.spinner(f"مدير العمليات يعمل عبر نموذج {selected_model}..."):
            st.markdown(agent.coo(task))

st.markdown("---")

if st.button("✍️ تنفيذ النظام الشامل (إنشاء الإعلان الاحترافي + إرسال واتساب تلقائي)"):
    if task.strip():
        with st.spinner("🔄 جاري تفعيل الوكلاء في الخلفية وتحليل المعطيات..."):
            # الخطوات تعمل بسلاسة في الخلفية
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            
            st.success("تم التنفيذ بنجاح! تم إنشاء الإعلان وإرساله عبر الواتساب.")
            st.markdown("### 📋 الإعلان النهائي الجاهز للنشر:")
            st.markdown(final_ad)
    else:
        st.warning("الرجاء إدخال وصف المهمة أو المشروع أولاً.")
