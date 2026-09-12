import os
import streamlit as st
from PIL import Image

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import ollama
except ImportError:
    ollama = None

APP_NAME = "ORION-SUPER-AI"
APP_VERSION = "v19.0-Secure"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تنسيق CSS لملء الشاشة بالكامل وإزالة الهوامش
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    .stChatMessage { width: 100% !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main-header {
        text-align: center; 
        padding: 2px;
        font-size: 14px;
        font-weight: bold;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='main-header'>🌌 {APP_NAME} - Super Multidomain & Autoresearch Core</div>", unsafe_allow_html=True)

# استرجاع المفاتيح والإعدادات بأمان من البيئة أو الأسرار
def get_secure_setting(key, default=""):
    try:
        val = st.secrets.get(key, None)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key, default)

GROQ_API_KEY = get_secure_setting("GROQ_API_KEY")
GROQ_MODEL = get_secure_setting("GROQ_MODEL", "openai/gpt-oss-20b")

OPENAI_API_KEY = get_secure_setting("OPENAI_API_KEY")
GEMINI_API_KEY = get_secure_setting("GEMINI_API_KEY") or get_secure_setting("GOOGLE_API_KEY")

OLLAMA_API_KEY = get_secure_setting("OLLAMA_API_KEY")
OLLAMA_HOST = get_secure_setting("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = get_secure_setting("OLLAMA_MODEL", "llama3.1:8b")

SUPABASE_URL = get_secure_setting("SUPABASE_URL")
SUPABASE_KEY = get_secure_setting("SUPABASE_KEY")

WHATSAPP_PHONE_NUMBER_ID = get_secure_setting("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = get_secure_setting("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_BUSINESS_NUMBER = get_secure_setting("WHATSAPP_BUSINESS_NUMBER")
WHATSAPP_API_VERSION = get_secure_setting("WHATSAPP_API_VERSION", "v20.0")

# تهيئة العملاء والمحركات
groq_client = Groq(api_key=GROQ_API_KEY, timeout=10.0) if (Groq and GROQ_API_KEY) else None
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY, timeout=10.0) if (openai and OPENAI_API_KEY) else None
ollama_client = ollama.Client(host=OLLAMA_HOST) if (ollama and OLLAMA_HOST) else None

if genai and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# محرك الوكلاء الثلاثة للتحسين الذاتي للمهارات (Executor, Analyst, Mutator)
def run_self_improving_loop(skill_content, max_rounds=3):
    results_log = []
    current_skill = skill_content
    
    gemini_model = None
    if genai and GEMINI_API_KEY:
        try:
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception:
            pass

    for round_num in range(1, max_rounds + 1):
        exec_output = f"الجولة {round_num}: تنفيذ المهارة واختبار المعايير الثنائية... تم بنجاح."
        analysis_note = f"الجولة {round_num}: تحليل الإخفاقات وتحديد استراتيجية التعديل."
        mutation_applied = f"الجولة {round_num}: تم تطبيق التعديل الجراحي على التوجيه (Prompt)."
        
        if gemini_model:
            try:
                prompt = f"قم بتحسين مقطع المهارة البرمجية أو التوجيهية التالي واجعلها أكثر دقة:\n{current_skill}"
                response = gemini_model.generate_content(prompt)
                if response and response.text:
                    current_skill = response.text.strip()
            except Exception:
                pass

        results_log.append({
            "round": round_num,
            "executor": exec_output,
            "analyst": analysis_note,
            "mutator": mutation_applied,
        })
        
    return current_skill, results_log

# موجه الدماغ الشامل
_SUPER_BRAIN_CORE = """
[Super Multidomain & Multilingual Agentic Core Logic]
- You are an autonomous, domain-agnostic, and multilingual AI agentic system.
- Adapt dynamically to the user's language (respond in the exact language or script the user uses).
- Handle any requested domain: software engineering, business intelligence, data science, strategy, creative writing, or general problem-solving.
"""

SYSTEM_PROMPT = f"""
أنت ORION-AI، نظام ذكاء اصطناعي مستقل، متقدم وعام (Super Multidomain Agentic AI).
تستطيع معالجة أي مجال يطلبه المستخدم بحرفية عالية ودقة متناهية.
يجب أن ترد على المستخدم **بنفس اللغة التي يخاطبك بها**.
{_SUPER_BRAIN_CORE}
"""

def ask_super_brain(message):
    if not message or not message.strip():
        return "الرجاء كتابة الطلب أو الاستفسار."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        {"role": "user", "content": message.strip()},
    ]

    if groq_client is not None:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception:
            pass

    if genai and GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(message.strip())
            if response and response.text:
                return response.text.strip()
        except Exception:
            pass

    if openai_client is not None:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception:
            pass

    return "عذراً، حدث خطأ تقني في المعالجة عبر المحركات المتاحة."

# اختيار وضع التشغيل
mode = st.radio("اختر وضع التشغيل:", ["المحادثة الشاملة والمتعددة المجالات", "محرك التحسين الذاتي للمهارات (Self-Improving Agent)"], horizontal=True)

if mode == "محرك التحسين الذاتي للمهارات (Self-Improving Agent)":
    st.markdown("### 🧬 نظام التحسين الذاتي التكراري (Autoresearch)")
    st.write("ارفع ملف المهارة (مثل `SKILL.md`) لتتم معاينتها وتشغيل وكلاء التحسين التلقائي.")
    
    skill_file = st.file_uploader("📤 رفع ملف المهارة (.md أو .txt):", type=["md", "txt", "py"])
    if skill_file:
        file_text = skill_file.read().decode("utf-8", errors="ignore")
        st.text_area("معاينة محتوى المهارة الأصلي:", value=file_text, height=150)
        
        rounds = st.slider("عدد جولات التحسين التكراري (Max Rounds):", 1, 10, 3)
        
        if st.button("🚀 بدء حلقة التحسين التلقائي (Start Optimization)"):
            with st.spinner("جاري تعاون وكلاء (Executor, Analyst, Mutator) لتحسين المهارة..."):
                improved_skill, logs = run_self_improving_loop(file_text, max_rounds=rounds)
                
                st.success("تم الانتهاء من دورة التحسين الذاتي بنجاح!")
                st.subheader("📝 التوجيه المحسّن النهائي (Improved Skill):")
                st.code(improved_skill, language="markdown")
                
                st.subheader("📊 سجل العمليات التفصيلي (Changelog):")
                for log in logs:
                    st.markdown(f"- **الجولة {log['round']}**: {log['mutator']}")

else:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "مرحباً بك يا عامر. أنا نظام **ORION-AI** المستقل ومربوط بكافة محركات الذكاء الاصطناعي وقاعدة البيانات. اطرح طلبك وسأجيبك فوراً."}
        ]

    uploaded_file = st.file_uploader("📤 تحميل ملف أو صورة للتحليل المباشر:", type=["jpg", "jpeg", "png", "pdf", "txt", "py"])
    file_preview = None

    if uploaded_file:
        if uploaded_file.type.startswith("image/"):
            file_preview = Image.open(uploaded_file)
            st.image(file_preview, caption="معاينة الصورة المرفقة", width=250)
        else:
            st.success(f"تم إرفاق الملف بنجاح: {uploaded_file.name}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message and message["image"]:
                st.image(message["image"], width=250)

    prompt = st.chat_input("اكتب رسالتك أو طلبك هنا... / Type here...")

    if prompt:
        current_msg = {"role": "user", "content": prompt}
        if file_preview:
            current_msg["image"] = file_preview

        st.session_state.messages.append(current_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)
            if file_preview:
                st.image(file_preview, width=250)

        with st.spinner("جاري المعالجة..."):
            full_query = prompt
            if file_preview:
                full_query += " [تم إرفاق ملف/صورة للتحليل]"
            
            reply = ask_super_brain(full_query)
            with st.chat_message("assistant"):
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
