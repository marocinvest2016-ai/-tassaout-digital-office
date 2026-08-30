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
st.set_page_config(page_title="خدمات تساوت الرقمية", page_icon="💻", layout="centered")

st.markdown("""
<style>
.main-header {
    text-align: center; 
    color: #1e3a8a; 
    font-weight: 800; 
    font-size: 1.5rem; 
    font-family: 'Cairo', sans-serif; 
    margin-bottom: 20px;
    margin-top: 10px;
}
.stChatMessage {
    background-color: #f8fafc; 
    border-radius: 16px; 
    padding: 1rem; 
    margin-bottom: 10px;
}
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
FOUNDER_SIGNATURE = "انتاج السيد عامر مؤسس الذكاء المنطقي السحابي المركب<br>جهة مراكش اسفي<br>كل الحقوق محفوظة 2026"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

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

# العنوان المطلوب فقط فوق الشاشة
st.markdown("<h1 class='main-header'>خدمات تساوت الرقمية للعقار والاعمال بقلعة السراغنة</h1>", unsafe_allow_html=True)

# عرض سجل المحادثات إن وجدت
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
            st.download_button("📥 تحميل حزمة الإعلانات والملفات (ZIP)", msg["zip"], f"tassaout_package_{i}.zip", key=f"zip_btn_{i}")

# الشاشة التفاعلية الكبيرة
with st.container(border=True):
    uploaded_files = st.file_uploader(
        "📁 اختر أو اسحب الملفات، الصور، أو الفيديوهات للرفع",
        type=["png", "jpg", "jpeg", "mp4", "pdf", "docx"],
        accept_multiple_files=True,
        key="large_box_uploader"
    )
    
    prompt = st.text_area(
        "اكتب طلبك أو كبسولة المعلوميات هنا...",
        placeholder="اكتب تفاصيل الإعلان العقاري، الاستشارة، أو الطلب المراد تنفيذه...",
        height=140,
        key="large_box_prompt"
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

    with st.spinner("جاري المعالجة وهندسة المحتوى الرقمي..."):
        context = "المستخدم رفع ملفات: " + ", ".join([a['name'] for a in attachments]) if attachments else ""
        system_prompt = f"""
        أنت الوكيل الذكي والمساعد الحصري في خدمات تساوت الرقمية للعقار والأعمال بقلعة السراغنة، جهة مراكش آسفي.
        قم بصياغة النصوص الإعلانية والتسويقية العقارية باحترافية تامة. اختم دائماً برقم التواصل الرسمي: {BRAND_PHONE}
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
                answer = "عذراً، عميل الذكاء الاصطناعي غير متصل حالياً."
        except Exception as e:
            answer = f"حدث خطأ في المعالجة: {e}"

        images = []
        zip_buffer = None

        if any(k in (prompt or "") for k in ["إعلان", "عقار", "شقة", "بقعة", "منزل", "ولد", "صايب", "تصميم"]) or attachments:
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

# التذييل في أسفل الموقع حسب الطلب تماماً
whatsapp_url = f"https://wa.me/{LOCAL_PHONE.replace('0', '+212', 1)}"
st.markdown(f"""
    <div style="text-align: center; padding: 20px 0; font-family: 'Cairo', sans-serif; color: #1e3a8a;">
        <div style="margin-bottom: 12px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 24px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">
                💬 تواصل عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <p style="font-size: 0.95rem; color: #2563eb; font-weight: 700; line-height: 1.8;">
            {FOUNDER_SIGNATURE}
        </p>
    </div>
""", unsafe_allow_html=True)
