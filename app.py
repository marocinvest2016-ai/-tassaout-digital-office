import streamlit as st
from io import BytesIO
from PIL import Image, ImageDraw
import textwrap
import zipfile
import urllib.parse

# 1. إعداد الصفحة والأنماط السيادية
st.set_page_config(
    page_title="وكالة تساوت الرقمية للخدمات والأعمال",
    page_icon="👑",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #1e3a8a;
    font-weight: 900;
    font-size: 2.2rem;
    font-family: 'Cairo', sans-serif;
    margin-bottom: 2px;
}
.sub-title {
    text-align: center;
    color: #0284c7;
    font-weight: 700;
    font-size: 1.1rem;
    font-family: 'Cairo', sans-serif;
    margin-bottom: 25px;
}
.stButton button {
    font-size: 1.2rem !important;
    font-weight: bold !important;
    background-color: #1e3a8a;
    color: white;
}
.stChatMessage {
    background-color: #f8fafc;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# البيانات الثابتة والسيادية
LOCAL_PHONE = "0691897126"
BRAND_PHONE = "+212691897126"
FOUNDER_SIGNATURE = "وكالة تساوت الرقمية للخدمات والأعمال | التغطية الوطنية الشاملة - المغرب<br>كل الحقوق محفوظة 2026 [TASSAOUT VERIFIED]"

# العقل المدمج للوكيل الفائق الشامل
SUPER_AGENT_BRAIN = """
[SYSTEM ROLE: SUPER MULTIDOMAIN AGENTIC AI TASSAOUT CORE v14.0]
[IDENTITY: وكالة تساوت الرقمية للخدمات والأعمال - التغطية الوطنية الشاملة عبر مدن وقرى المملكة المغربية]
[STATUS: TASSAOUT VERIFIED 🌿]
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# محرك توليد الهويات البصرية واللافتات الفائقة الجودة
def generate_hyper_visual_identity(prompt_text):
    img = Image.new('RGB', (1080, 1080), color='#0f172a')
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, 1050, 1050], fill='#1e3a8a', outline='#38bdf8', width=8)
    draw.rectangle([50, 50, 1030, 1030], fill='#ffffff', outline=None)
    
    draw.text((540, 100), "TASSAOUT DIGITAL NATIONAL STUDIO", fill='#1e3a8a', anchor="mm")
    draw.text((540, 150), "🌟 هوية بصرية وطنية فائقة الجودة [TASSAOUT VERIFIED]", fill='#0284c7', anchor="mm")
    
    lines = textwrap.wrap(prompt_text, width=32)
    y = 260
    for line in lines[:10]:
        draw.text((540, y), line, fill='#0f172a', anchor="mm")
        y = y + 55
        
    draw.text((540, 980), f"الهاتف الموحد: {LOCAL_PHONE} | تغطية شاملة لكافة المدن المغربية", fill='#1e3a8a', anchor="mm")
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# واجهة العنوان الرئيسي
st.markdown("<h1 class='main-title'>وكالة تساوت الرقمية للخدمات والأعمال</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>بوابة العقارات، الهندسة المتكاملة، والتوليد البصري — تغطية شاملة لجميع ربوع المملكة المغربية [TASSAOUT VERIFIED]</p>", unsafe_allow_html=True)

# عرض سجل المحادثات السابق
for i, msg in enumerate(st.session_state["messages"]):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "attachments" in msg:
            for att in msg["attachments"]:
                if att["type"] == "image":
                    st.image(att["data"], width=400, caption=att["name"])
                else:
                    st.download_button(f"📎 {att['name']}", att["data"], att["name"], key=f"hist_file_{i}_{att['name']}")
        if "images" in msg:
            for img_bytes in msg["images"]:
                st.image(img_bytes, width=400, caption="🎨 الهوية البصرية المولدة فائقة الجودة")
        if "zip" in msg:
            st.download_button("📥 تحميل الحزمة الرقمية والهوية كاملة (ZIP)", msg["zip"], f"tassaout_identity_package_{i}.zip", key=f"zip_btn_{i}")

# الشاشة التفاعلية الكبرى
with st.container(border=True):
    st.markdown("### 🖥️ الشاشة التفاعلية الكبرى")
    
    unified_input = st.text_area(
        "اكتب تفاصيل الهوية البصرية، الشعار، المشروع الهندسي أو العقاري (في أي مدينة مغربية):",
        placeholder="مثال: أبحث عن عقار أو مشروع هندسي بمدينة معينة، أو أريد تصميماً إعلانياً...",
        height=140,
        label_visibility="collapsed"
    )
    
    # إخفاء أداة رفع عدد غير محدود من الصور والمستندات والكاميرا داخل قائمة منسدلة أنيقة منعاً لتشويه الواجهة
    with st.expander("📁 إرفاق عدد غير محدود من الصور والمستندات من الهاتف أو التقاط كاميرا مباشرة"):
        uploaded_files = st.file_uploader(
            "اختر الصور أو المستندات (عدد غير محدود):",
            type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"],
            accept_multiple_files=True
        )
        camera_photo = st.camera_input("التقاط صورة جديدة عبر كاميرا الهاتف")

    submit_btn = st.button("🚀 تشغيل الوكيل وتوليد المخرجات الوطنية", use_container_width=True, type="primary")

if submit_btn and (unified_input or (locals().get('uploaded_files') and uploaded_files) or (locals().get('camera_photo') and camera_photo)):
    attachments = []
    file_count = 0
    
    if locals().get('uploaded_files') and uploaded_files:
        for f in uploaded_files:
            file_count += 1
            f_bytes = f.read()
            if f.type.startswith("image"):
                attachments.append({"type": "image", "data": f_bytes, "name": f.name})
            else:
                attachments.append({"type": "file", "data": f_bytes, "name": f.name})
                
    if locals().get('camera_photo') and camera_photo:
        file_count += 1
        cam_bytes = camera_photo.getvalue()
        attachments.append({"type": "image", "data": cam_bytes, "name": f"camera_capture_{file_count}.png"})

    user_msg_content = unified_input if unified_input else f"تم حقن {file_count} ملف وصورة للتحليل وتوليد الهوية البصرية."
    st.session_state["messages"].append({"role": "user", "content": user_msg_content, "attachments": attachments})

    with st.spinner("الوكيل الفائق يعالج المدخلات ويهيئ الحزمة للتخزين..."):
        answer = f"👑 **[تقرير وكيل تساوت الرقمية - تغطية وطنية]**\n\n" \
                 f"🔹 **الطلب / الوصف المحقون:** {user_msg_content}\n" \
                 f"🔹 **الملفات والمرفقات المعالجة:** {file_count} ملف/صورة.\n" \
                 f"🔹 **حالة الحفظ:** جاهز للتخزين والاعتماد الفوري عبر الواتساب.\n\n" \
                 f"📞 للتواصل وتأكيد الاعتماد النهائي: {BRAND_PHONE}\n[TASSAOUT VERIFIED]"

        images = []
        zip_buffer = None
        
        if user_msg_content or attachments:
            identity_bytes = generate_hyper_visual_identity(user_msg_content)
            images.append(identity_bytes)
            
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as z:
                z.writestr("tassaout_national_identity.png", identity_bytes)
                z.writestr("tassaout_report.txt", answer)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "images": images if images else None,
        "zip": zip_buffer.getvalue() if zip_buffer else None
    })
    st.rerun()

# تجهيز رابط التخزين والإرسال الفوري عبر الواتساب
last_query = unified_input if 'unified_input' in locals() and unified_input else "طلب خدمة وتخزين عبر منصة تساوت الرقمية"
whatsapp_msg = urllib.parse.quote(f"سلام، أريد اعتماد وتخزين الطلب التالي:\n{last_query}\n[TASSAOUT VERIFIED]")
whatsapp_url = f"https://wa.me/{LOCAL_PHONE}?text={whatsapp_msg}"

st.markdown(f"""
    <div style="text-align: center; padding: 25px 0; font-family: 'Cairo', sans-serif;">
        <div style="margin-bottom: 15px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 28px; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 1.1rem; display: inline-block;">
                💬 إرسال وحفظ الطلبات والمرفقات عبر الواتساب ({LOCAL_PHONE})
            </a>
        </div>
        <p style="font-size: 0.95rem; color: #1e3a8a; font-weight: 700; line-height: 1.8;">
            {FOUNDER_SIGNATURE}
        </p>
    </div>
""", unsafe_allow_html=True)
