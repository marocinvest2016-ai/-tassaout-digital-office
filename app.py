import streamlit as st
import requests
import json
import io

st.set_page_config(page_title="OMEGA Super Agentic AI - Voice v2.1", page_icon="👑", layout="wide")

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق - Groq + Llama 3.3"""
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

def transcribe_audio_with_whisper(audio_bytes):
    """تحويل التسجيل الصوتي إلى نص باستخدام Whisper API على Groq"""
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    api_key = st.secrets.get("GROQ_API_KEY", "")
    
    if not api_key:
        return ""

    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    files = {
        "file": ("audio.wav", audio_bytes, "audio/wav")
    }
    data = {
        "model": "whisper-large-v3",
        "language": "ar" # يدعم العربية واللهجة المغربية بشكل ممتاز
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        if response.status_code == 200:
            return response.json().get("text", "")
        else:
            return ""
    except Exception:
        return ""

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
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v2.1 (Voice)\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة Streamlit مع تفعيل الصوت (Voice Mode) =====
st.title("👑 OMEGA Super Agentic AI - Voice v2.1")
st.caption("النظام الذكي المتكامل المدعوم بالتحليل الصوتي المباشر عبر Whisper و Llama 3.3")

domain = st.text_input("أدخل مجال المشروع أو النشاط", placeholder="مثال: العقار، السيارات، التجارة، الزراعة...")

# قسم الادخال الصوتي (Voice Input)
st.markdown("🎙️ **أو تحدث مباشرة لتسجيل المهمة صوتياً:**")
audio_value = st.audio_input("اضغط للتسجيل الصوتي")

task_input_method = st.text_area("وصف المهمة / المشروع (يتم تعبئته تلقائياً من الصوت أو يدوياً)", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة")

# إذا قام المستخدم بالتسجيل الصوتي، نقوم بتحويله إلى نص عبر Whisper API
if audio_value is not None:
    with st.spinner("🎧 جاري تحويل صوتك إلى نص عبر Whisper..."):
        audio_bytes = audio_value.read()
        transcribed_text = transcribe_audio_with_whisper(audio_bytes)
        if transcribed_text:
            task = transcribed_text
            st.success(تم التعرف على الصوت بنجاح: "{task}")
        else:
            task = task_input_method
            st.warning("تعذر استخراج النص من الصوت، يرجى إعادة المحاولة أو الكتابة يدوياً.")
else:
    task = task_input_method

if domain and task:
    agent = SuperOmegaAgent(domain)

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

    st.markdown("---")

    if st.button("✍️ إنشاء إعلان + إرسال واتساب"):
        with st.spinner("جاري إعداد الإعلان النهائي وإرساله..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("تم بنجاح!")
            st.markdown("### 📋 الإعلان النهائي:")
            st.markdown(final_ad)
else:
    st.info("الرجاء إدخال المجال ووصف المهمة (سواء كتابة أو عبر التسجيل الصوتي) للبدء.")
