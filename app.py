import streamlit as st
from supabase import create_client
from google import genai
from google.genai import types
import requests

# ==========================================
# 1. تهيئة الإعدادات والمفاتيح
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://rbyjjnkhdjfksyodiujs.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "sb_publishable_Rf29NrOcmLnj0woKiYNFXw_8R5C8sP-")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "106540352242922")
WHATSAPP_ACCESS_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_BUSINESS_NUMBER = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "212691897126")
WHATSAPP_API_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")
WHATSAPP_LINK = "https://wa.me/212691897126"

# ==========================================
# 2. مصفوفة التشغيل الذاتي للأفرقة
# ==========================================
AGENTIC_MATRIX = f"""
أنت النظام المركزي "Claude Bernard OS" - المدير العام لـ Super Multi-Domain Agentic AI

لديك 3 وكلاء مستقلين يعملون في حلقة مغلقة:

**1. Arch-Industrial Agentic AI**
المجالات: التخطيط المعماري، BIM & 3D CAD، حساب التكاليف، قوانين البناء
القدرات: توليد مخططات أوتوماتيكياً، محاكاة السلامة، تصحيح الأخطاء قبل التصدير
المخرج: مخطط + تقرير تكاليف + ملاحظات سلامة

**2. Interior & Decor Agentic AI**  
المجالات: الهندسة الداخلية، الإضاءة الفيزيائية، الخامات، VR
القدرات: مطابقة الألوان للميزانية، توزيع الإضاءة، إنشاء ديكور متناغم مع المخطط
المخرج: مشهد 3D مفروش + قائمة مواد + ستايل إضاءة

**3. Visual & Studio Agentic AI**
المجالات: CGI سينمائي، فوتوشوب ذكي، تسويق
القدرات: اختيار زوايا الكاميرا، تصحيح لوني، رندر، أرشفة في Supabase، إرسال واتساب
المخرج: 8 زوايا تصوير + نص إعلان جذاب

قاعدة العمل: فكر -> نفذ -> صحح -> مرر للوكيل التالي -> أرشف -> أرسل
في نهاية كل دورة ضع: 📲 {WHATSAPP_LINK} | TASSAOUT AGENTIC AI
"""

# ==========================================
# 3. عملاء الخدمات (Clients Init)
# ==========================================
@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_resource
def get_gemini():
    if GEMINI_API_KEY:
        return genai.Client(api_key=GEMINI_API_KEY)
    return None

supabase = get_supabase()
gemini_client = get_gemini()

# ==========================================
# 4. دوال الوكلاء والحلقة الذكية
# ==========================================
def agent_arch(prompt: str) -> str:
    if not gemini_client:
        return "⚠️ مفتاح GEMINI_API_KEY غير متوفر."
    res = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"[المهمة]: {prompt}\n[المخرج المطلوب]: مخطط + تكاليف + ملاحظات سلامة",
        config=types.GenerateContentConfig(
            system_instruction="أنت Arch-Industrial Agentic AI. فكر، صمم، صحح أخطائك المعمارية والإنشائية.",
            temperature=0.2
        )
    )
    return res.text

def agent_decor(arch_output: str) -> str:
    if not gemini_client:
        return "⚠️ مفتاح GEMINI_API_KEY غير متوفر."
    res = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"[مدخل من المهندس]: {arch_output}\n[المهمة]: صمم الديكور والإضاءة والخامات والتأثيث",
        config=types.GenerateContentConfig(
            system_instruction="أنت Interior & Decor Agentic AI. اقرأ المخطط وافرشه بذكاء مع اختيار الألوان والمواد.",
            temperature=0.4
        )
    )
    return res.text

def agent_visual(decor_output: str, original_prompt: str) -> str:
    if not gemini_client:
        return "⚠️ مفتاح GEMINI_API_KEY غير متوفر."
    res = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"[مدخل من الديكور]: {decor_output}\n[المهمة الأصلية]: {original_prompt}\n[المخرج]: 8 زوايا تصوير سينمائي + نص إعلان جاهز",
        config=types.GenerateContentConfig(
            system_instruction="أنت Visual & Studio Agentic AI. حدد زوايا التصوير، الرندر، واكتب الإعلان التسويقي النهائي.",
            temperature=0.5
        )
    )
    return res.text

def send_wa(msg: str):
    if not WHATSAPP_ACCESS_TOKEN:
        return
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_BUSINESS_NUMBER,
        "type": "text",
        "text": {"body": msg}
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"}
    try:
        requests.post(url, headers=headers, json=payload)
    except Exception as e:
        st.error(f"خطأ في إرسال واتساب: {e}")

def save_ad(content: str, message: str, source: str):
    try:
        supabase.table("instant_ads").insert({
            "content": content,
            "message": message,
            "source": source
        }).execute()
    except Exception as e:
        st.error(f"خطأ في الحفظ بـ Supabase: {e}")

def get_ads():
    try:
        res = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        return res.data or []
    except Exception:
        return []

def agentic_loop(user_prompt: str):
    with st.status("🔄 تشغيل الحلقة الأجنتية الثلاثية...", expanded=True) as status:
        st.write("🏗️ 1. Arch-Industrial Agentic AI: توليد المخطط وتحديد التكاليف...")
        arch_res = agent_arch(user_prompt)
        
        st.write("🎨 2. Interior & Decor Agentic AI: تجهيز الديكور والإضاءة والخامات...")
        decor_res = agent_decor(arch_res)
        
        st.write("📸 3. Visual & Studio Agentic AI: تحديد الزوايا وصياغة الإعلان...")
        visual_res = agent_visual(decor_res, user_prompt)
        
        final_output = f"### 🏗️ المخطط والتكاليف (Arch AI)\n{arch_res}\n\n---\n### 🎨 الديكور والخامات (Decor AI)\n{decor_res}\n\n---\n### 📸 الإخراج والإعلان (Visual AI)\n{visual_res}\n\n📲 {WHATSAPP_LINK} | TASSAOUT AGENTIC AI"
        
        st.write("💾 4. الأرشفة في Supabase والتوجيه إلى WhatsApp...")
        save_ad(user_prompt, final_output, "Agentic-Loop-300")
        send_wa(final_output)
        
        status.update(label="✅ اكتملت الدورة الأجنتية بنجاح!", state="complete")
        return final_output

# ==========================================
# 5. الواجهة البرمجية (Streamlit UI)
# ==========================================
st.set_page_config(page_title="TASSAOUT AGENTIC AI", page_icon="🤖", layout="wide")

st.title("🤖 TASSAOUT VISION — Super Multi-Domain Agentic AI")
st.caption("نظام التشغيل الذاتي: 3 وكلاء مستقلون | حلقة عمل مغلقة | تفكير + تنفيذ + تصحيح ذاتي")
st.link_button("📲 واتساب مباشر", WHATSAPP_LINK, type="primary")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ إدخال المهمة للذكاء الأجنتي")
    prompt = st.text_area(
        "صف المشروع أو العقار المطلوب:",
        placeholder="مثال: فيلا 200م للبيع بقلعة السراغنة، R+1 مع مسبح وحديقة",
        height=150
    )
    
    if st.button("🚀 تشغيل الحلقة الأجنتية الكاملة", type="primary"):
        if not prompt:
            st.warning("يرجى كتابة تفاصيل المشروع أولاً.")
        else:
            result = agentic_loop(prompt)
            st.session_state["result"] = result

with col2:
    st.subheader("📜 المخرجات النهائية للحلقة")
    if "result" in st.session_state:
        st.markdown(st.session_state["result"])
    else:
        st.info("في انتظار تشغيل الحلقة لعرض النتائج هنا.")

st.divider()

st.subheader("📋 أرشيف العمليات الأجنتية المسجلة")
ads = get_ads()
if ads:
    for ad in ads:
        with st.expander(f"🤖 {ad.get('source', 'Agent')} | {ad.get('content', '')[:60]}"):
            st.markdown(ad.get("message", ""))
            st.caption(f"التاريخ: {ad.get('created_at', '')}")
else:
    st.info("لا توجد سجلات مؤرشفة حالياً.")
