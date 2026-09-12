import os
import streamlit as st
import ollama
from PIL import Image
import base64, io
from datetime import datetime
import PyPDF2

# =====================================================================
# الرابط المرجعي للكبسولة المعلوماتية والتكنولوجية (Awesome LLM Apps):
# https://github.com/Shubhamsaboo/awesome-llm-apps
# 
# حقوق الملكية والإنتاج:
# - المنتج والمالك: السيد عامر بوخدادة
# - الجهة: مراكش آسفي - قلعة السراغنة، المملكة المغربية
# - الهاتف: +212691897126
# - البريد الإلكتروني: marocinvest2012@gmail.com
# =====================================================================

APP_NAME = "ORION-AI Interactive Screen"
APP_VERSION = "v9.4 - Capsule Agent + RAG"
LOCATION = "قلعة السراغنة - مراكش آسفي"
OWNER_NAME = "السيد عامر بوخدادة"
AGENCY_PHONE = "+212691897126"
AGENCY_EMAIL = "marocinvest2012@gmail.com"
AGENCY_NAME = "وكالة تساوت للعقارات والخدمات"
CAPSULE_REPO = "https://github.com/Shubhamsaboo/awesome-llm-apps"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيقات CSS احترافية
st.markdown("""
<style>
    .main-header { text-align: center; padding: 15px; background: linear-gradient(135deg, #1e1e2f, #2d2b42); border-radius: 10px; color: white; margin-bottom: 20px; }
    .footer { text-align: center; color: gray; font-size: 12px; margin-top: 50px; }
    .stChatMessage { border-radius: 12px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# =========================
# 1. الدماغ + النماذج المفتوحة المستوحاة من الكبسولة
# =========================
class OrionNeuralCore:
    def __init__(self):
        self.client_ollama = ollama.Client(host="http://localhost:11434")
        # النماذج المستخرجة والمعتمدة من الكبسولة الهندسية
        self.open_models = {
            "text": ["qwen3:8b", "qwen3:1.7b", "gemma3:4b", "gemma3:1b", "deepseek-r1:1.5b", "llama3.2"],
            "vision": ["llava:7b", "llava:13b", "qwen2.5vl:7b"],
            "embedding": ["snowflake-arctic-embed"]
        }
        self.tools = {
            "RAG PDF": "حلل PDF واستخرج المعلومات منه",
            "Web Search": "بحث فالويب إلا ما لقيتش الجواب",
            "Agent Coding": "كتب كود أو حل مشكل برمجي",
            "Real Estate": "وكيل عقاري - حلل الصور والأسعار بالدارجة"
        }
        self.rag_context = "" # الذاكرة الخاصة بملفات PDF

    def image_to_base64(self, f):
        image = Image.open(f).convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()

    def read_pdf(self, pdf_file):
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            self.rag_context = text[:8000] # اقتطاع السياق للسرعة
            return f"تم قراءة {len(reader.pages)} صفحة بنجاح. الذاكرة جاهزة للأسئلة."
        except Exception as e:
            return f"خطأ في قراءة ملف الـ PDF: {e}"

    def run_agent(self, tool, prompt, images=[], model="auto"):
        system = f"أنت دانا، وكيلة ذكية ومتخصصة في {tool} بمنظومة {AGENCY_NAME} الإدارية لـ {OWNER_NAME} بـ {LOCATION}. تحدثي بالدارجة المغربية بأسلوب احترافي وودي. أعط خطوات عملية ودقيقة بالأرقام دون اختلاق معلومات."

        current_prompt = prompt
        if self.rag_context and tool == "RAG PDF":
            current_prompt = f"السياق المستخرج من ملف الـ PDF:\n{self.rag_context}\n\nسؤال المستخدم: {prompt}"

        use_vision = len(images) > 0
        if model == "auto":
            model = self.open_models["vision"][0] if use_vision else self.open_models["text"][0]

        messages = [{"role": "system", "content": system}]
        if use_vision:
            messages.append({"role": "user", "content": current_prompt, "images": images})
        else:
            messages.append({"role": "user", "content": current_prompt})

        try:
            res = self.client_ollama.chat(model=model, messages=messages)
            content = res.get("message", {}).get("content", "")
            return content.strip(), f"Ollama Local ({model})"
        except Exception as e:
            return f"خطأ في الاتصال بنظام Ollama المحلي: {e}. تأكد من تشغيله عبر الأمر: ollama serve", "Error"

if "orion_core" not in st.session_state:
    st.session_state.orion_core = OrionNeuralCore()

core = st.session_state.orion_core

# =========================
# 2. الواجهة التفاعلية (Sidebar & Main UI)
# =========================
st.markdown(f"<div class='main-header'><h1>👑 {APP_NAME}</h1><p>{APP_VERSION} | {LOCATION}</p></div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎛️ لوحة تحكم الوكلاء")
    st.caption(f"المنتج: {OWNER_NAME}")
    st.caption(f"الوكالة: {AGENCY_NAME}")
    
    selected_tool = st.selectbox("اختر أداة التشغيل الذكي (Tool):", list(core.tools.keys()))
    st.info(f"💡 وصف الأداة: {core.tools[selected_tool]}")
    
    st.markdown("---")
    selected_model = st.selectbox("اختر النموذج المحلي:", ["auto"] + core.open_models["text"] + core.open_models["vision"])
    
    st.markdown("---")
    if selected_tool == "RAG PDF":
        st.subheader("📁 رفع وثيقة الـ RAG")
        uploaded_pdf = st.file_uploader("اختر ملف PDF للعقود أو الدفاتتر", type=["pdf"])
        if uploaded_pdf:
            if st.button("📖 قراءة وتحليل الوثيقة"):
                with st.spinner("جاري قراءة وتحليل الوثيقة واستخراج النصوص..."):
                    pdf_status = core.read_pdf(uploaded_pdf)
                    st.success(pdf_status)

    st.markdown("---")
    st.markdown(f"🔗 **الكبسولة الهندسية:** [Awesome LLM Apps]({CAPSULE_REPO})")
    st.markdown(f"📞 **الهاتف:** {AGENCY_PHONE}")
    st.markdown(f"✉️ **البريد:** {AGENCY_EMAIL}")

# =========================
# 3. قسم الدردشة والتفاعل المباشر
# =========================
st.subheader(f"🤖 محادثة تفاعلية - وضع [{selected_tool}]")

uploaded_files = st.file_uploader("📸 رفع الصور المرفقة (اختياري)", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
images_base64 = []
if uploaded_files:
    cols = st.columns(4)
    for i, file in enumerate(uploaded_files):
        with cols[i % 4]: 
            st.image(file, use_column_width=True)
        images_base64.append(core.image_to_base64(file))

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"مرحباً! أنا دانا، ممثلة لمنظومة {OWNER_NAME}. جاهزة لمساعدتك في قطاع **{selected_tool}**. كتب ليا طلبك أو صيفط صور/وثائق."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("اكتب استفسارك هنا...")

if user_prompt or images_base64:
    display_text = user_prompt if user_prompt else "📸 [تم إرفاق صور]"
    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.markdown(display_text)

    with st.chat_message("assistant"):
        with st.spinner("دانا كتفكر وكتعالج المعطيات محلياً..."):
            reply, engine_info = core.run_agent(selected_tool, user_prompt if user_prompt else "حلل الصور المرفقة", images_base64, selected_model)
        
        st.markdown(reply)
        st.caption(f"⚡ محرك التشغيل: {engine_info}")
    
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown(f"<div class='footer'>{APP_NAME} {APP_VERSION} © {datetime.now().year} | انتاج السيد {OWNER_NAME} | جهة مراكش آسفي ({LOCATION}) | جميع الحقوق محفوظة</div>", unsafe_allow_html=True)
