import streamlit as st
import requests
import json
import os
import tempfile
from groq import Groq

st.set_page_config(page_title="OMEGA Super Agentic Suite", page_icon="👑", layout="wide")

# دالة فحص النماذج المتاحة في Groq
def get_available_groq_model(api_key):
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
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
            for model in preferred_models:
                if model in available_ids:
                    return model
            if available_ids:
                return available_ids[0]
    except Exception:
        pass
    return "llama-3.1-8b-instant"

def call_super_ai(prompt, agent_name, domain):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets أو البيئة."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

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
        if res.status_code == 404 and active_model != "llama-3.1-8b-instant":
            payload["model"] = "llama-3.1-8b-instant"
            res = requests.post(url, headers=headers, json=payload, timeout=90)

        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def send_whatsapp_alert(message):
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

# ===== واجهة التبويبات (Tabs) لتنظيم التطبيقين =====
tab1, tab2 = st.tabs(["👑 OMEGA Super Agentic AI", "🎙️ تفريغ صوتي - Whisper V3"])

with tab1:
    st.title("👑 OMEGA Super Agentic AI - متعدد المجالات")
    st.caption("CEO + CTO + COO + Copywriter + Closer في وكيل واحد يخدم على Groq")

    domain = st.selectbox("اختر المجال", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق"], key="d_select")
    task = st.text_area("وصف المهمة / المشروع", placeholder="مثال: بيع بقع أرضية في تجزئة الهدى بقلعة السراغنة", key="t_area")

    agent = SuperOmegaAgent(domain)

    api_key_val = st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")
    if api_key_val:
        active_model_name = get_available_groq_model(api_key_val)
        st.info(f"🤖 **النموذج النشط المكتشف تلقائياً:** `{active_model_name}`")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🧠 خطة CEO", key="btn_ceo"):
            with st.spinner("المدير التنفيذي كيخدم..."):
                st.markdown(agent.ceo(task))
    with col2:
        if st.button("💻 خطة CTO", key="btn_cto"):
            with st.spinner("المدير التقني كيخدم..."):
                st.markdown(agent.cto(task))
    with col3:
        if st.button("📊 خطة COO", key="btn_coo"):
            with st.spinner("مدير العمليات كيخدم..."):
                st.markdown(agent.coo(task))

    if st.button("✍️ إنشاء إعلان + إرسال واتساب", key="btn_ad"):
        with st.spinner("الكاتب كيكتب الإعلان..."):
            plan = agent.ceo(task)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("تم!")
            st.markdown(final_ad)

with tab2:
    st.title("🎙️ تفريغ صوتي باستخدام Groq Whisper V3")
    st.markdown("حمّل ملف صوتي أو فيديو للحصول على تفريغ نصي فوري")

    api_key_whisper = st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")
    if not api_key_whisper:
        api_key_whisper = st.sidebar.text_input("أدخل مفتاح Groq API للتفريغ", type="password")

    if api_key_whisper:
        client = Groq(api_key=api_key_whisper)
        
        uploaded_file = st.file_uploader(
            "اختر ملف صوتي أو فيديو",
            type=["wav", "mp3", "mp4", "m4a", "ogg", "flac", "webm", "mpeg", "mpga"],
            help="الملفات المدعومة: WAV, MP3, MP4, M4A, OGG, FLAC, WEBM"
        )
        
        if uploaded_file is not None:
            st.info(f"📁 الملف: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
            
            if uploaded_file.type.startswith("audio"):
                st.audio(uploaded_file)
            elif uploaded_file.type.startswith("video"):
                st.video(uploaded_file)
            
            if st.button("🚀 ابدأ التفريغ", type="primary", key="btn_transcribe"):
                try:
                    with st.spinner("جاري التفريغ..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                    
                        with open(tmp_path, "rb") as f:
                            transcription = client.audio.transcriptions.create(
                                file=(uploaded_file.name, f),
                                model="whisper-large-v3",
                                response_format="text",
                                language="ar",
                                temperature=0.0
                            )
                        
                        os.unlink(tmp_path)
                        
                        st.success("✅ تم التفريغ بنجاح!")
                        st.subheader("📝 النص المفرّغ:")
                        st.write(transcription)
                        
                        st.download_button(
                            label="📥 تحميل النص",
                            data=transcription,
                            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcript.txt",
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    else:
        st.warning("⚠️ يرجى إدخال مفتاح Groq API للبدء في التفريغ الصوتي.")
