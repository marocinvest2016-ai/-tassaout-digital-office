import streamlit as st
import requests
import json

# إعداد واجهة الصفحة بتصميم واسع وأيقونة ملكية
st.set_page_config(
    page_title="OMEGA Super Agentic AI", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم وتنسيق CSS إضافي لجعل الواجهة أكثر أناقة واحترافية
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    .uploaded-img-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق متعدد المجالات - Groq مع نظام النماذج الاحتياطية"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

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
            res = requests.post(url, headers=headers, json=payload, timeout=90)
            res.raise_for_status()
            return res.json()['choices'][0]['message']['content']
        except Exception as e:
            last_error = str(e)
            continue

    return f"❌ خطأ في الاتصال بجميع النماذج: {last_error}"

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

    def ceo(self, task, images_info=""):
        prompt = f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}. {images_info} عطيني SWOT + الميزة التنافسية + خطة 90 يوم"
        return call_super_ai(prompt, "Super CEO Agent", self.domain)

    def cto(self, task, images_info=""):
        prompt = f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}. {images_info}"
        return call_super_ai(prompt, "Super CTO Agent", self.domain)

    def coo(self, task, images_info=""):
        prompt = f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}. {images_info}"
        return call_super_ai(prompt, "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى مع أيقونات، كلمات مفتاحية، هاشتاقات، ودعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.1\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال FOMO + ضمان + شهادات لزيادة المبيعات: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== تصميم واجهة المستخدم التفاعلية =====
st.title("👑 OMEGA Super Agentic AI - نظام الإدارة والوكلاء الأذكياء")
st.markdown("---")

# الشريط الجانبي للإعدادات والمعلومات
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.header("إعدادات العمل")
    domain = st.selectbox("🎯 اختر المجال المستهدف", ["العقار", "التجارة الإلكترونية", "المطاعم", "التعليم", "الصحة", "التسويق الرقمي"])
    
    st.info("💡 **نصيحة:** قم بكتابة تفاصيل دقيقة للمشروع وارفاق الصور التوضيحية للحصول على استراتيجيات دقيقة ومخصصة.")
    st.markdown("---")
    st.caption("مدعوم بواسطة Groq & Meta Llama 🚀")

# منطقة العمل الرئيسية (قسم المدخلات والصور)
col_input, col_media = st.columns([2, 1], gap="medium")

with col_input:
    st.subheader("📝 تفاصيل المشروع أو المهمة")
    task = st.text_area(
        "اكتب تفاصيل طلبك هنا...", 
        placeholder="مثال: تسويق وبيع بقع أرضية سكنية في تجزئة الهدى بقلعة السراغنة مع إبراز المميزات القريبة...",
        height=160
    )

with col_media:
    st.subheader("🖼️ مرفقات الصور (اختياري)")
    uploaded_files = st.file_uploader(
        "اختر صور المشروع (عقارات، منتجات، تصاميم...)", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )

# معاينة الصور المرفوعة بطريقة أنيقة
images_info = ""
if uploaded_files:
    st.markdown("**📸 الصور المرفوعة للمشروع:**")
    img_cols = st.columns(min(len(uploaded_files), 4))
    for idx, uploaded_file in enumerate(uploaded_files):
        with img_cols[idx % 4]:
            st.image(uploaded_file, caption=f"صورة {idx+1}", use_container_width=True)
    images_info = f"[ملاحظة: قام المستخدم بإرفاق {len(uploaded_files)} صور توضيحية للمشروع يجب أخذها بعين الاعتبار]."

st.markdown("---")

# إنشاء كائن الوكيل بناءً على المجال المختار
agent = SuperOmegaAgent(domain)

# أزرار التشغيل والتحكم الإداري
st.subheader("⚡ لوحة التحكم وتحفيذ الوكلاء")
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
    ceo_btn = st.button("🧠 استشارة CEO")
with btn_col2:
    cto_btn = st.button("💻 استشارة CTO")
with btn_col3:
    coo_btn = st.button("📊 استشارة COO")
with btn_col4:
    campaign_btn = st.button("✍️ إعلان + واتساب 📱")

# التعامل مع الأزرار وعرض المخرجات
if ceo_btn:
    if task.strip():
        with st.spinner("⏳ المدير التنفيذي (CEO) يدرس المشروع ويضع الاستراتيجية..."):
            result = agent.ceo(task, images_info)
            st.markdown("### 🧠 تقرير المدير التنفيذي (CEO)")
            st.markdown(result)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")

if cto_btn:
    if task.strip():
        with st.spinner("⏳ المدير التقني (CTO) يجهز البنية التقنية والحلول الرقمية..."):
            result = agent.cto(task, images_info)
            st.markdown("### 💻 تقرير المدير التقني (CTO)")
            st.markdown(result)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")

if coo_btn:
    if task.strip():
        with st.spinner("⏳ مدير العمليات (COO) يضع الجدول الزمني وخطة التنفيذ..."):
            result = agent.coo(task, images_info)
            st.markdown("### 📊 تقرير مدير العمليات (COO)")
            st.markdown(result)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")

if campaign_btn:
    if task.strip():
        with st.spinner("🚀 جاري كتابة الحملة الإعلانية، إرسال تنبيه الواتساب، وتفعيل مهارات الإغلاق..."):
            plan = agent.ceo(task, images_info)
            ad = agent.copywriter(plan)
            final_ad = agent.closer(ad)
            st.success("✨ تم إنشاء الحملة الإعلانية وإرسالها بنجاح إلى الواتساب!")
            st.markdown("### ✍️ الحملة الإعلانية المطورة والمحسنة للمبيعات:")
            st.markdown(final_ad)
    else:
        st.warning("⚠️ يرجى كتابة وصف المهمة أو المشروع أولاً.")
