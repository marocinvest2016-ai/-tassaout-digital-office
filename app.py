import streamlit as st
import requests
import json
import base64
from fpdf import FPDF
import datetime

st.set_page_config(page_title="OMEGA Super Agentic AI", page_icon="👑", layout="wide", initial_sidebar_state="expanded")

# تصميم وتنسيق CSS أنيق واحترافي
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def call_super_ai(prompt, agent_name, domain, use_vision=False, uploaded_files=None):
    """محرك الذكاء الاصطناعي الفائق - مع دعم الرؤية (صور) ونظام Groq"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # اختيار الموديل تلقائياً حسب وجود صور أو طلب استراتيجية
    model = "qwen/qwen3.6-27b" if (use_vision and uploaded_files) else "groq/compound"

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Groq. "
        f"Think step by step. Use web search and advanced capabilities if needed. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    messages = [{"role": "system", "content": system_prompt}]

    # معالجة الصور المرسلة إن وجدت
    if use_vision and uploaded_files:
        content = [{"type": "text", "text": prompt}]
        for file in uploaded_files:
            img_b64 = base64.b64encode(file.read()).decode()
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}})
        messages.append({"role": "user", "content": content})
    else:
        messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 3000
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=120)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def generate_audio(text):
    """توليد صوت احترافي للإعلان (Text-to-Speech)"""
    url = "https://api.groq.com/openai/v1/audio/speech"
    api_key = st.secrets.get("GROQ_API_KEY", "")
    payload = {
        "model": "canopylabs/orpheus-arabic-saudi",
        "input": text[:3000],
        "voice": "saadi" # صوت رجولي احترافي
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        return res.content
    except Exception as e:
        st.warning(f"تعذر توليد الصوت: {e}")
        return None

def export_pdf(title, content):
    """تصدير التقارير والإعلانات إلى ملف PDF"""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'OMEGA Super Agentic AI - Report', 0, 1, 'C')
            self.ln(5)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    
    # تنظيف النصوص لضمان توافق الطباعة
    safe_title = title.encode('latin-1', 'ignore').decode('latin-1')
    safe_content = content.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.cell(0, 10, txt=safe_title, ln=True, align='C')
    pdf.ln(5)
    pdf.multi_cell(0, 8, txt=safe_content)
    
    filename = f"OMEGA_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def save_campaign(domain, task, ad):
    """حفظ الحملات الإعلانية في ملف محلي"""
    data = {"date": str(datetime.datetime.now()), "domain": domain, "task": task, "ad": ad}
    try:
        with open("campaigns.json", "r", encoding="utf-8") as f:
            campaigns = json.load(f)
    except:
        campaigns = []
    campaigns.append(data)
    with open("campaigns.json", "w", encoding="utf-8") as f:
        json.dump(campaigns, f, ensure_ascii=False, indent=2)

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
    def __init__(self, domain, uploaded_files):
        self.domain = domain
        self.uploaded_files = uploaded_files

    def ceo(self, task, use_vision=False):
        return call_super_ai(f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}. عطيني SWOT + الميزة التنافسية + خطة 90 يوم", "Super CEO Agent", self.domain, use_vision, self.uploaded_files)

    def cto(self, task, use_vision=False):
        return call_super_ai(f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}", "Super CTO Agent", self.domain, use_vision, self.uploaded_files)

    def coo(self, task, use_vision=False):
        return call_super_ai(f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}", "Super COO Agent", self.domain, use_vision, self.uploaded_files)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.4\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة Streamlit الأنيقة =====
st.title("👑 OMEGA Super Agentic AI - نظام الإدارة والوكلاء الأذكياء")
st.markdown("---")

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.header("إعدادات العمل")
    domain = st.selectbox("🎯 اختر المجال المستهدف", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق الرقمي"])
    st.info("💡 **نصيحة:** اكتب تفاصيل دقيقة للمشروع وقم برفع الصور التوضيحية للحصول على تحليل بصري واستراتيجي متكامل.")
    st.markdown("---")
    st.caption("مدعوم بواسطة Groq Compound & Qwen Vision 🚀")

# تقسيم الشاشة (مكان الكتابة + رفع الصور)
col_input, col_media = st.columns([2, 1], gap="medium")

with col_input:
    st.subheader("📝 تفاصيل المشروع أو المهمة")
    task = st.text_area(
        "اكتب تفاصيل طلبك هنا...", 
        placeholder="مثال: بيع 50 بقعة أرضية في تجزئة الهدى بقلعة السراغنة، المساحة من 120م إلى 300م...",
        height=160
    )

with col_media:
    st.subheader("🖼️ مرفقات الصور (اختياري)")
    uploaded_files = st.file_uploader(
        "اختر صور المشروع (عقارات، منتجات، تصاميم...)", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )

if uploaded_files:
    st.markdown("**📸 الصور المرفوعة للمشروع:**")
    img_cols = st.columns(min(len(uploaded_files), 4))
    for idx, uploaded_file in enumerate(uploaded_files):
        with img_cols[idx % 4]:
            st.image(uploaded_file, caption=f"صورة {idx+1}", use_container_width=True)

st.markdown("---")

agent = SuperOmegaAgent(domain, uploaded_files)

st.subheader("⚡ لوحة التحكم وتحفيز الوكلاء")
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
    ceo_btn = st.button("🧠 استشارة CEO")
with btn_col2:
    cto_btn = st.button("💻 استشارة CTO")
with btn_col3:
    coo_btn = st.button("📊 استشارة COO")
with btn_col4:
    campaign_btn = st.button("✍️ إعلان + واتساب 📱")

if ceo_btn:
    if task.strip():
        with st.spinner("⏳ المدير التنفيذي (CEO) يدرس المشروع و يحلل الصور..."):
            result = agent.ceo(task, use_vision=True if uploaded_files else False)
            st.markdown("### 🧠 تقرير المدير التنفيذي (CEO)")
            st.markdown(result)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")

if cto_btn:
    if task.strip():
        with st.spinner("⏳ المدير التقني (CTO) يجهز الحلول التقنية..."):
            result = agent.cto(task, use_vision=True if uploaded_files else False)
            st.markdown("### 💻 تقرير المدير التقني (CTO)")
            st.markdown(result)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")

if coo_btn:
    if task.strip():
        with st.spinner("⏳ مدير العمليات (COO) يضع الجدول الزمني وخطة التنفيذ..."):
            result = agent.coo(task, use_vision=True if uploaded_files else False)
            st.markdown("### 📊 تقرير مدير العمليات (COO)")
            st.markdown(result)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")

if campaign_btn:
    if task.strip():
        with st.spinner("🚀 جاري إنشاء الحملة الإعلانية، الإرسال للواتساب، والحفظ..."):
            plan = agent.ceo(task, use_vision=True if uploaded_files else False)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            
            # حفظ الحملة تلقائياً
            save_campaign(domain, task, final_ad)
            
            st.success("✨ تم إنشاء الحملة الإعلانية وإرسالها بنجاح إلى الواتساب وحفظها!")
            st.markdown("### ✍️ الحملة الإعلانية المطورة والمحسنة للمبيعات:")
            st.markdown(final_ad)
            
            # أزرار تفاعلية إضافية (صوت + PDF)
            st.markdown("---")
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🎙️ توليد صوت للإعلان بالدارجة"):
                    with st.spinner("جاري تسجيل الصوت..."):
                        audio_bytes = generate_audio(final_ad)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                            st.success("✅ تم توليد التسجيل الصوتي بنجاح!")
            
            with col_b:
                if st.button("📄 تحميل التقرير بصيغة PDF"):
                    pdf_file = export_pdf(f"OMEGA Campaign - {domain}", final_ad)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="📥 اضغط هنا لتحميل ملف PDF",
                            data=f,
                            file_name=pdf_file,
                            mime="application/pdf"
                        )
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")
