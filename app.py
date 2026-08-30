import streamlit as st
from groq import Groq
from supabase import create_client
from datetime import datetime, timezone
from io import BytesIO
from PIL import Image, ImageDraw
import textwrap
import replicate
import requests
import zipfile

# إعداد الصفحة وتطبيق التصميم المخصص لشريط الإدخال المدمج
data_page_config = st.set_page_config(page_title="مكتب تساوت الرقمي للخدمات والاستشارات", page_icon="💻", layout="centered")

st.markdown("""
<style>
.main-header {text-align: center; color: #1e3a8a; font-weight: 800; font-size: 1.8rem; font-family: 'Cairo';}
.phone-text {text-align: center; color: #0284c7; direction: ltr; font-weight: bold; font-size: 1.2rem;}
.stChatMessage {background-color: #f8fafc; border-radius: 16px; padding: 1rem;}

/* تخصيص مظهر شريط الإدخال ليشبه Gemini تماماً */
[data-testid="stChatInput"] {
    border-radius: 30px !important;
    border: 2px solid #3b82f6 !important;
    background-color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# الاتصال بالخدمات عبر الأسرار
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    replicate.api_token = st.secrets["REPLICATE_API_TOKEN"]
except Exception:
    supabase = None
    groq_client = None

BRAND_PHONE = "+212691897126"
LOCAL_PHONE = "0691897126"
FOUNDER_SIGNATURE = "عامر وسيط خدمات بقلعة السراغنة ومؤسس الذكاء المنطقي السحابي"

# تهيئة الذاكرة المؤقتة للمحادثة
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "مرحباً بك يا سيد الرئيس 👋\nأنا وكيلك الذكي في مكتب تساوت الرقمي للخدمات والاستشارات.\nاستخدم زر الإضافة (+) أدناه لرفع الصور أو الملفات، واكتب طلبك لنقوم بهندسته فوراً."}
    ]

# دالة توليد صورة الإعلان الهندسية الاحترافية
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

# رأس الصفحة والهوية
st.markdown("<h1 class='main-header'>مكتب تساوت الرقمي للخدمات والاستشارات</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='phone-text'>{LOCAL_PHONE}</p>", unsafe_allow_html=True)
st.divider()

# عرض رسائل المحادثة والمرفقات والأزرار السابقة
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

# =====================================================================
# شريط إدخال متفاعل يجمع زر (+) وحقل الكتابة في نفس السطر السفلي (مثل Gemini)
# =====================================================================
col_plus, col_input = st.columns([1, 10])

with col_plus:
    # زر (+) المدمج في نفس سطر الإدخال السفلي
    uploaded_files = st.file_uploader(
        "➕",
        type=["png", "jpg", "jpeg", "mp4", "pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="gemini_plus_uploader"
    )

with col_input:
    prompt = st.chat_input("اكتب طلبك أو كبسولة المعلوميات هنا...")

# معالجة المدخلات والطلبات عند الكتابة أو الرفع
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

    user_msg = {"role": "user", "content": prompt if prompt else "تم رفع ملفات للتحليل", "attachments": attachments, "id": datetime.now().timestamp()}
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

    # معالجة رد الوكيل والذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفاعل وتحليل المرفقات وتوليد الحزم الرقمية..."):

            context = "المستخدم رفع ملفات: " + ", ".join([a['name'] for a in attachments]) if attachments else ""

            system_prompt = f"""
            أنت الوكيل الذكي والمساعد الحصري لـ ({FOUNDER_SIGNATURE}) في مكتب تساوت الرقمي للخدمات والاستشارات بقلعة السراغنة ومراكش.
            قم بصياغة النصوص الإعلانية والتسويقية باحترافية تامة تعكس فلسفة المؤسس.
            اختم دائماً الرد برقم التواصل الرسمي: {BRAND_PHONE}
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

            images = []
            zip_buffer = None

            if any(k in (prompt or "") for k in ["إعلان", "إعلانات", "ولد", "صايب", "تصميم"]) or attachments:
                num_images = 3 if "3" in (prompt or "") else 1
                for _ in range(num_images):
                    img_bytes = generate_ad_image(answer)
                    images.append(img_bytes)
                    st.image(img_bytes, use_container_width=True)

                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as z:
                    for idx, img_data in enumerate(images):
                        z.writestr(f"ad_image_{idx+1}.png", img_data)
                    z.writestr("ad_text.txt", answer)
                
                st.download_button("📥 تحميل حزمة الإعلانات والملفات (ZIP)", zip_buffer.getvalue(), "tassaout_package.zip", key="zip_download_new")

    agent_msg = {"role": "assistant", "content": answer, "images": images if images else None, "zip": zip_buffer.getvalue() if zip_buffer else None, "id": datetime.now().timestamp()}
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
