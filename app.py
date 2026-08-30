import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone
from io import BytesIO
from PIL import Image, ImageDraw
import textwrap
import base64

st.set_page_config(page_title="مكتب تساوت الرقمي للخدمات والاستشارات", page_icon="💻", layout="centered")

# الثيم الأزرق النظيف والاحترافي
st.markdown("""
<style>
.main-header {text-align: center; color: #1e3a8a; font-weight: 800; font-size: 1.8rem; font-family: 'Cairo';}
.phone-text {text-align: center; color: #0284c7; direction: ltr; font-weight: bold;}
.stChatMessage {background-color: #f8fafc; border-radius: 16px; padding: 1rem;}
.upload-box {display: flex; gap: 10px; align-items: center;}
</style>
""", unsafe_allow_html=True)

# الاتصال بالخدمات
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    supabase = None
    groq_client = None

BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"
FOUNDER_SIGNATURE = "عامر وسيط خدمات بقلعة السراغنة ومؤسس الذكاء المنطقي السحابي"

# تهيئة الذاكرة المؤقتة للمحادثة
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "مرحباً بك يا سيد الرئيس 👋\nأنا وكيلك الذكي في مكتب تساوت الرقمي للخدمات والاستشارات.\nاضغط على زر (+) باش ترفع صورة عقار، فيديو، ولا ملف وسأقوم بتحليله وتوليد الإعلان فوراً."}
    ]

# دالة توليد صورة الإعلان الاحترافية
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

# عنوان الهيدر الرئيسي
st.markdown("<h1 class='main-header'>مكتب تساوت الرقمي للخدمات والاستشارات</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='phone-text'>{LOCAL_PHONE}</p>", unsafe_allow_html=True)
st.divider()

# عرض رسائل المحادثة والمرفقات السابقة
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
                    st.download_button(f"📎 {att['name']}", att["data"], att["name"], key=f"history_file_{i}_{att['name']}")

        if "generated_image" in msg:
            st.image(msg["generated_image"], use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 تحميل الصورة", msg["generated_image"], "ad_tassaout.png", "image/png", key=f"img_{i}")
            with col2:
                st.download_button("📄 تحميل النص", msg["content"], "ad.txt", key=f"txt_{i}")

# ==================== شريط الإدخال المدمج مع زر + ====================
col_input, col_btn = st.columns([8, 1])

with col_btn:
    uploaded_files = st.file_uploader(
        "➕",
        type=["png", "jpg", "jpeg", "mp4", "pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="uploader"
    )

with col_input:
    prompt = st.chat_input("اكتب طلبك هنا... أو اضغط على + لرفع ملف أو صورة")

# معالجة المدخلات عند الإرسال أو رفع الملفات
if prompt or uploaded_files:
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

    user_msg = {"role": "user", "content": prompt if prompt else "تم رفع مرفقات للتحليل", "attachments": attachments, "id": datetime.now().timestamp()}
    st.session_state["messages"].append(user_msg)

    with st.chat_message("user"):
        st.write(user_msg["content"])
        for att in attachments:
            if att["type"] == "image":
                st.image(att["data"], caption=att["name"])
            elif att["type"] == "video":
                st.video(att["data"])
            else:
                st.write(f"📎 {att['name']}")

    # معالجة رد الوكيل عبر الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التحليل وتوليد الإعلان هندسياً..."):

            context = "المستخدم رفع ملفات: " + ", ".join([a['name'] for a in attachments]) if attachments else ""

            system_prompt = f"""
            أنت الوكيل الذكي والمساعد الحصري لـ ({FOUNDER_SIGNATURE}) في مكتب تساوت الرقمي للخدمات والاستشارات بقلعة السراغنة ومراكش.
            إذا رفع المستخدم صورة عقار أو مرفق، قم بتحليله وتقديم رؤية هندسية وتسويقية احترافية.
            إذا طلب إعلان، قم بتنظيم وصياغة النص بشكل راقي وجذاب.
            اختم دائماً برقم التواصل الرسمي: {BRAND_PHONE}
            """

            try:
                resp = groq_client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": (prompt if prompt else "") + " " + context}
                    ],
                    temperature=0.6
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                answer = f"عذراً يا سيد الرئيس، حدث خطأ في معالجة الطلب: {e}"

            st.write(answer)

            generated_image = None
            if any(k in (prompt or "") for k in ["إعلان", "ولد", "صايب", "تصميم"]) or attachments:
                generated_image = generate_ad_image(answer)
                st.image(generated_image, use_container_width=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 تحميل الصورة", generated_image, "ad_tassaout.png", key="new_img_dl")
                with col2:
                    st.download_button("📄 تحميل النص", answer, "ad.txt", key="new_txt_dl")

    agent_msg = {"role": "assistant", "content": answer, "id": datetime.now().timestamp()}
    if generated_image:
        agent_msg["generated_image"] = generated_image
    st.session_state["messages"].append(agent_msg)
    
    st.rerun()

# ==================== تذييل الموقع (Footer) الرسمي ====================
st.markdown("---")
whatsapp_url = f"https://wa.me/{LOCAL_PHONE.replace('0', '+212', 1)}"

st.markdown(f"""
    <div style="text-align: center; padding: 15px 0; font-family: 'Cairo', sans-serif; color: #1e3a8a;">
        <p style="font-size: 1.1rem; font-weight: bold; margin-bottom: 5px;">مكتب تساوت الرقمي للخدمات والاستشارات</p>
        <div style="margin-bottom: 12px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-weight: bold; display: inline-block;">
                💬 تواصل عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <hr style="border: none; border-top: 1px solid #cbd5e1; width: 50%; margin: 10px auto;">
        <p style="font-size: 0.95rem; color: #2563eb; font-weight: 600; margin-bottom: 5px;">
            إنتاج: {FOUNDER_SIGNATURE}
        </p>
        <p style="font-size: 0.9rem; color: #64748b; font-weight: bold;">
            كل الحقوق محفوظة 2026
        </p>
    </div>
""", unsafe_allow_html=True)
