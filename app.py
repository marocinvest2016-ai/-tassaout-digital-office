import os
import streamlit as st
from groq import Groq
import ollama
from PIL import Image
import base64
import io
from datetime import datetime

# =========================
# إعدادات النظام العامة - اضافات في الاول
# =========================
APP_NAME = "ORION-AI & دانا الوكيلة العقارية"
APP_VERSION = "v3.1"
LOCATION = "قلعة السراغنة - مراكش"
AGENCY_PHONE = "0691897126"
AGENCY_NAME = "وكالة تساوت للعقارات والخدمات"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للواجهة
st.markdown("""
<style>
   .main-header {text-align: center; padding: 10px;}
   .footer {text-align: center; color: gray; font-size: 12px; margin-top: 50px;}
</style>
""", unsafe_allow_html=True)

# =========================
# قراءة الإعدادات بأمان
# =========================
def get_setting(key, default=""):
    try:
        value = st.secrets.get(key, default)
    except Exception:
        value = default
    return value or os.getenv(key, default)

GROQ_KEY = get_setting("GROQ_API_KEY")
GROQ_MODEL = get_setting("GROQ_MODEL", "llama-3.2-90b-vision-preview")
OLLAMA_HOST = get_setting("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = get_setting("OLLAMA_MODEL", "llava")

# =========================
# تهيئة العملاء الذكيين
# =========================
groq_client = Groq(api_key=GROQ_KEY, timeout=30.0) if GROQ_KEY else None
ollama_client = ollama.Client(host=OLLAMA_HOST) if OLLAMA_HOST else None

# =========================
# تحويل الصورة ل base64
# =========================
def image_to_base64(uploaded_file):
    image = Image.open(uploaded_file)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# =========================
# تعليمات دانا والمنظومة
# =========================
SYSTEM_PROMPT = f"""
أنت دانا، وكيلة عقارية ذكية ومديرة أعمال من {AGENCY_NAME} بـ {LOCATION}.
تاريخ اليوم: {datetime.now().strftime("%Y-%m-%d")}
تحدثي بالدارجة المغربية بطريقة ودودة ومحترفة.
مهمتك:
- تحليل الصور: تشخيص العقار، الديكور، العيوب، الجودة
- مساعدة العملاء في البحث عن العقارات والبقع التجارية (مثل المنارة 1 و 3).
- تقديم معلومات واضحة، دقيقة ومنظمة بالأرقام.
- طرح أسئلة مفيدة لفهم طلب العميل (الميزانية، المساحة، نوع العقار).
- اقتراح حجز موعد للمعاينة وتوجيههم لخدمات الوكالة.
- عدم اختراع أسعار أو مساحات أو معلومات غير موجودة.
"""

def ask_dana(message, images_base64=[], current_context=""):
    if not message and not images_base64:
        return "عافاك كتب ليا أو صيفط ليا صور.", "Error"

    system_content = SYSTEM_PROMPT.strip()
    if current_context:
        system_content += f"\n\nالسياق الحالي: {current_context}"

    user_content = [{"type": "text", "text": message}]
    for img_b64 in images_base64:
        user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}})

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL, messages=messages, temperature=0.7, max_tokens=1000
            )
            content = response.choices[0].message.content
            if content: return content.strip(), "Groq"
        except Exception: pass

    if ollama_client and images_base64:
        try:
            response = ollama_client.chat(
                model=OLLAMA_MODEL, messages=[{"role": "system", "content": system_content}, {"role": "user", "content": message, "images": images_base64}]
            )
            content = response.get("message", {}).get("content", "")
            if content: return content.strip(), "Ollama"
        except Exception: pass

    return f"سمح ليا، وقع مشكل تقني مؤقت. تواصل معنا: {AGENCY_PHONE}", "Error"

# =========================
# مصفوفة الـ 100 قطاع
# =========================
sectors_matrix = {
    "1. العقارات والبناء (1-15)": ["الوساطة العقارية السكنية والتجارية", "الهندسة المعمارية 3D", "التصميم الداخلي والديكور"],
    "2. الإعلام والتسويق الرقمي (16-30)": ["التصوير الفوتوغرافي الاحترافي", "إنتاج الفيديوهات الترويجية"],
    "3. التجارة والصناعة واللوجستيات (31-50)": ["دراسات الجدوى الاقتصادية", "الصناعات الغذائية"],
    "4. الفلاحة والتنمية القروية (51-70)": ["تسيير الضيعات الفلاحية", "تثمين الزيتون"],
    "5. الخدمات الإدارية والقانونية (71-85)": ["تأسيس الشركات", "التدبير المحاسباتي"],
    "6. الأتمتة المتقدمة (86-100)": ["بناء نظم CRM", "روبوتات الدردشة"],
}

# =========================
# الواجهة الرئيسية
# =========================
st.markdown(f"<div class='main-header'><h1>👑 {APP_NAME}</h1><p>الذكاء الاصطناعي المتكامل لإدارة العقارات والخدمات بـ {LOCATION}</p></div>", unsafe_allow_html=True)

st.sidebar.title("🎛️ لوحة تحكم المنظومة")
st.sidebar.caption(f"النسخة: {APP_VERSION}")
app_mode = st.sidebar.radio("اختر وضع التشغيل:", ["💬 محادثة دانا المباشرة", "📊 مصفوفة الـ 100 قطاع"])
st.sidebar.info(f"📌 هاتف الوكالة: {AGENCY_PHONE}")

# 1. قسم المحادثة
if app_mode == "💬 محادثة دانا المباشرة":
    st.subheader("🤖 محادثة ذكية مع دانا")

    uploaded_files = st.file_uploader("📸 رفع صور من الهاتف", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    images_base64 = []
    if uploaded_files:
        cols = st.columns(3)
        for i, file in enumerate(uploaded_files):
            with cols[i % 3]: st.image(file, use_container_width=True)
            images_base64.append(image_to_base64(file))

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"مرحباً! أنا دانا من {AGENCY_NAME}. شنو العقار اللي باغي؟"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    prompt = st.chat_input("سوليني...")
    if prompt or images_base64:
        st.session_state.messages.append({"role": "user", "content": prompt if prompt else "📸 صور"})
        with st.chat_message("user"): st.markdown(prompt if prompt else "📸 صور")
        with st.chat_message("assistant"):
            with st.spinner("دانا كتفكر..."):
                reply, brain = ask_dana(prompt, images_base64)
            st.markdown(reply)
            st.caption(f"⚡ {brain}")
        st.session_state.messages.append({"role": "assistant", "content": reply})

# 2. قسم المصفوفة
elif app_mode == "📊 مصفوفة الـ 100 قطاع":
    st.subheader("⚙️ مصفوفة التشغيل")
    selected_axis = st.selectbox("اختر المحور:", list(sectors_matrix.keys()))
    selected_sector = st.selectbox("اختر القطاع:", sectors_matrix[selected_axis])
    user_input_data = st.text_area("التفاصيل:")
    if st.button("🚀 تنفيذ"):
        report_reply, engine_used = ask_dana(f"قطاع: {selected_sector}. {user_input_data}", current_context=selected_sector)
        st.success("تم")
        st.markdown(report_reply)

st.markdown(f"<div class='footer'>{APP_NAME} {APP_VERSION} © {datetime.now().year} | {LOCATION}</div>", unsafe_allow_html=True)
