from datetime import datetime
import io, tempfile, requests
import streamlit as st
from groq import Groq

st.set_page_config(page_title="OMEGA SOA FREE", page_icon="👑", layout="centered")

@st.cache_data(ttl=3600) # كاشي النمادج ساعة باش ما نعاودوش نطلبو
def get_live_groq_models(api_key):
    """يجيب جميع النمادج المفتوحة المصدر الحية من Groq"""
    if not api_key: return []
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        # غير المفتوحة المصدر + المدعومة للـ Chat
        open_models = [m.id for m in models.data if "llama" in m.id or "mixtral" in m.id or "gemma" in m.id or "deepseek" in m.id or "qwen" in m.id]
        # الترتيب حسب القوة
        priority = ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b", "llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it", "llama-3.1-8b-instant"]
        return sorted(open_models, key=lambda x: priority.index(x) if x in priority else 999)
    except: return ["llama-3.3-70b-versatile"] # fallback

def call_super_ai(prompt, agent_name, domain, model):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ ضع GROQ_API_KEY فـ Settings > Secrets")
        st.stop()

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system_prompt = f"You are {agent_name} for '{domain}'. خبير مغربي. Respond in Moroccan Darija + العربية. Bullets + tables + emojis. كن دقيق."
    payload = {"model": model, "messages": [{"role":"system","content":system_prompt},{"role":"user","content":prompt}], "temperature": 0.7, "max_tokens": 4000}
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=120)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e: return f"خطأ فالنموذج {model}: {e}"

def generate_pdf(text):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 10); y = 750
    for line in text.split("\n"):
        c.drawString(50, y, line[:110]); y -= 16
        if y < 50: c.showPage(); c.setFont("Helvetica", 10); y = 750
    c.save(); buffer.seek(0); return buffer.getvalue()

# ===== الواجهة =====
st.title("👑 OMEGA SOA - MULTI MODEL FREE")
st.caption("يختار أقوى نموذج مفتوح المصدر من Groq أوتوماتيك")

api_key = st.secrets.get("GROQ_API_KEY", "")
live_models = get_live_groq_models(api_key)

col1, col2 = st.columns([3,1])
with col1:
    domain = st.selectbox("المجال", ["العقار", "التجارة", "المطاعم", "التعليم", "الصحة"])
    task = st.text_area("وصف المهمة", placeholder="مثال: فيلا 220م R+1 فالقلعة. ميزانية 120 مليون", height=150)
with col2:
    st.write("**🧠 النمادج المتاحة:**")
    selected_model = st.selectbox("اختر النموذج", live_models, index=0, help="OMEGA يختار الأول تلقائيا")
    st.info(f"المختار: {selected_model}")

if st.button("🚀 شغّل OMEGA", type="primary", use_container_width=True):
    if task:
        with st.spinner(f"OMEGA يفكر بـ {selected_model}..."):
            res = call_super_ai(f"ضع خطة شاملة لمشروع {domain}: {task}. SWOT + خطة 90 يوم + الميزانية بالدرهم", "Super CEO", domain, selected_model)
            full_report = f"# OMEGA REPORT FREE\nالنموذج: {selected_model}\nالمجال: {domain}\nالمهمة: {task}\n\n{res}\n\n---\nOMEGA-FREE-FOREVER"
            st.success(f"✅ تمت المهمة بـ {selected_model}")
            st.text_area("الملخص", full_report, height=350)
            st.download_button("📄 تحميل PDF", generate_pdf(full_report), f"OMEGA_{datetime.now().strftime('%Y%m%d')}.pdf")

st.divider()
st.subheader("🎙️ تفريغ صوتي Whisper V3")
client = Groq(api_key=api_key)
audio = st.file_uploader("ارفع صوت/فيديو", type=['mp3','wav','m4a'])
if audio and st.button("🚀 فرّغ"):
    with st.spinner("كنفرغو..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp: tmp.write(audio.getvalue())
        transcription = client.audio.transcriptions.create(file=(audio.name, open(tmp.name,"rb")), model="whisper-large-v3", language="ar")
        st.text_area("النص المفرغ", transcription.text, height=200)
        st.download_button("📄 تحميل النص", transcription.text, "transcript.txt")
