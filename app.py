import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw
import textwrap
import zipfile

# محاولة استيراد المكتبات الأساسية
try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from supabase import create_client
except ImportError:
    create_client = None

try:
    import replicate
except ImportError:
    replicate = None

# إعداد الصفحة
st.set_page_config(page_title="مكتب تساوت الرقمي", page_icon="💻", layout="centered")

st.markdown("""
<style>
.main-header {text-align: center; color: #1e3a8a; font-weight: 800; font-size: 1.7rem; font-family: 'Cairo'; margin-bottom: 15px;}
.stChatMessage {background-color: #f8fafc; border-radius: 16px; padding: 1rem; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# الاتصال بالخدمات
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]) if create_client else None
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"]) if Groq else None
    if replicate:
        replicate.api_token = st.secrets["REPLICATE_API_TOKEN"]
except Exception:
    supabase = None
    groq_client = None

BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"
FOUNDER_SIGNATURE = "عامر وسيط خدمات بقلعة السراغنة ومؤسس الذكاء المنطقي السحابي"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "مرحباً بك يا سيد الرئيس 👋\nأنا وكيلك الذكي في مكتب تساوت الرقمي. استخدم الشاشة التفاعلية الكبيرة أدناه لرفع الملفات وكتابة طلبك."}
    ]

def generate_ad_image(text):
    img = Image.new('RGB', (1080, 1080), color='#1e3a8a')
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 1040, 1040], fill='white', outline='#0284c7', width=10)
    draw.text((540, 90), "مكتب تساوت الرقمي - إعلان", fill='#1e3a8a', anchor="mm")
    draw.text((540, 140), f"الهاتف: {LOCAL_PHONE}", fill='#0284c7', anchor="mm")
    lines = textwrap.wrap(text, width=32)
    y = 240
    for line in lines[:12]:
        draw.text((540, y), line, fill='black', anchor="mm")
        y += 55
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# العنوان فقط فوق الشاشة
st.markdown("<h1 class='main-header'>مكتب تساوت الرقمي | العقار والأعمال بقلعة السراغنة</h1>", unsafe_allow_html=True)

# عرض سجل المحادثات
for i, msg in enumerate(st.session_state["messages"]):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "attachments" in msg:
            for att in msg["attachments"]:
                if att["type"] == "image":
                    st.image(att["data"], use_container_width=True)
                elif att["type"] == "video":
                    st.video(att["data"])
                elif att["type"] == "file":
                    st.download_button(f"📎 {att['name']}", att["data"], att["name"], key=f"hist_file_{i}_{att['name']}")
        if "images" in msg:
            for img_bytes in msg["images"]:
                st.image(img_bytes, use_container_width=True)
        if "zip" in msg:
            st.download_button("📥 تحميل الحزمة (ZIP)", msg["zip"], f"tassaout_package_{i}.zip", key=f"zip_btn_{i}")

st.divider()

# الشاشة التفاعلية الكبيرة (تحتوي الزر ومساحة الكتابة بداخلها)
with st.container(border=True):
    st.markdown("### 🎛️ الشاشة التفاعلية للتشغيل والتحكم")
    
    uploaded_files = st.file_uploader(
        "➕ اختر أو اسحب الصور، الفيديوهات أو المستندات هنا",
        type=["png", "jpg", "jpeg", "mp4", "pdf", "docx"],
        accept_multiple_files=True,
        key="inside_uploader"
    )
    
    prompt = st.text_area(
        "اكتب طلبك أو كبسولة المعلوميات هنا...",
        placeholder="اكتب هنا تفاصيل الإعلان أو الطلب المراد تنفيذه...",
        height=130,
        key="inside_prompt"
    )
    
    submit_btn = st.button("🚀 تنفيذ الطلب وإرسال", use_container_width=True, type="primary")

if submit_btn and (prompt or uploaded_files):
    attachments = []
    if uploaded_files:
        for file in uploaded_files:
            file_bytes = file.read()
            if file.type.startswith("image"):
                attachments.append({"type": "image", "data": file_bytes, "name": file.name})
            elif file.type.startswith("video"):
                attachments.append({"type": "video", "data": file_bytes, "name": file.name})
            else:
                attachments.append({"type": "file", "data": file_bytes, "name": file.name})

    user_msg = {"role": "user", "content": prompt if prompt else "تم رفع ملفات للتحليل", "attachments": attachments}
    st.session_state["messages"].append(user_msg)

    with st.spinner("جاري المعالجة وتوليد الحزمة الرقمية..."):
        context = "المستخدم رفع ملفات: " + ", ".join([a['name'] for a in attachments]) if attachments else ""
        system_prompt = f"""
        أنت الوكيل الذكي والمساعد الحصري لـ ({FOUNDER_SIGNATURE}) في مكتب تساوت الرقمي للخدمات والاستشارات بقلعة السراغنة ومراكش.
        قم بصياغة النصوص الإعلانية والتسويقية باحترافية. اختم دائماً برقم التواصل الرسمي: {BRAND_PHONE}
        """

        try:
            if groq_client:
                resp = groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": (prompt if prompt else "") + " " + context}
                    ],
                    temperature=0.6
                )
                answer = resp.choices[0].message.content
            else:
                answer = "عذراً، عميل الذكاء الاصطناعي (Groq) غير متصل حالياً."
        except Exception as e:
            answer = f"حدث خطأ في المعالجة: {e}"

        images = []
        zip_buffer = None

        if any(k in (prompt or "") for k in ["إعلان", "إعلانات", "ولد", "صايب", "تصميم"]) or attachments:
            img_bytes = generate_ad_image(answer)
            images.append(img_bytes)

            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as z:
                z.writestr("ad_image_1.png", img_bytes)
                z.writestr("ad_text.txt", answer)

    agent_msg = {
        "role": "assistant",
        "content": answer,
        "images": images if images else None,
        "zip": zip_buffer.getvalue() if zip_buffer else None
    }
    st.session_state["messages"].append(agent_msg)
    st.rerun()

# التذييل وزر الواتساب السفلي
whatsapp_url = f"https://wa.me/{LOCAL_PHONE.replace('0', '+212', 1)}"
st.markdown(f"""
    <div style="text-align: center; padding: 15px 0; font-family: 'Cairo', sans-serif; color: #1e3a8a;">
        <div style="margin-bottom: 12px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 24px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">
                💬 تواصل عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <p style="font-size: 0.9rem; color: #2563eb; font-weight: 600;">إنتاج: {FOUNDER_SIGNATURE}</p>
        <p style="font-size: 0.85rem; color: #64748b;">كل الحقوق محفوظة 2026</p>
    </div>
""", unsafe_allow_html=True)
