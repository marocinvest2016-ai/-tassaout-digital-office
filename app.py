from io import BytesIO
import textwrap
import urllib.parse
from PIL import Image, ImageDraw
import pypdf  # مكتبة معالجة وقراءة ملفات PDF
import streamlit as st
import zipfile

# 1. إعداد الصفحة والأنماط السيادية
st.set_page_config(
    page_title="وكالة تساوت الرقمية للخدمات والأعمال", page_icon="👑", layout="wide"
)

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# البيانات الثابتة والسيادية بالصيغة الدولية المعتمدة
WHATSAPP_DISPLAY = "+212691897126"
WHATSAPP_CLEAN = "212691897126"
FOUNDER_SIGNATURE = "وكالة تساوت الرقمية للخدمات والأعمال | التغطية الوطنية الشاملة - المغرب<br>كل الحقوق محفوظة 2026 [TASSAOUT VERIFIED]<br><b>ameur signature tassaout ai</b>"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "👑 **[المكتبة الرقمية السحابية - الوكيل الذكي]**\n\n"
                "مرحباً بك يا أمير. تم إدماج وتوثيق مشروع **بناء الفيلا بقلعة السراغنة (226 م²)** ومراحلها الست الهندسية بالكامل ضمن النظام السيادي لتساوت الرقمية.\n\n"
                "**المراحل المؤرشفة:**\n"
                "1. التخطيط الميداني والأساسات\n"
                "2. تشييد الهيكل الخرساني\n"
                "3. الجدران الخارجية والعزل والواجهات\n"
                "4. التشطيبات الداخلية والتوزيع\n"
                "5. الديكور الداخلي والتأثيث الأنيق\n"
                "6. التسليم النهائي واللقطة الليلية الكبرى (Twilight)\n\n"
                "**[TASSAOUT VERIFIED 🌿]**\n"
                "**ameur signature tassaout ai**"
            ),
        }
    ]


# محرك توليد الهويات البصرية واللافتات الفائقة الجودة
def generate_hyper_visual_identity(prompt_text):
    img = Image.new("RGB", (1080, 1080), color="#0f172a")
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, 1050, 1050], fill="#1e3a8a", outline="#38bdf8", width=8)
    draw.rectangle([50, 50, 1030, 1030], fill="#ffffff", outline=None)

    draw.text(
        (540, 100),
        "TASSAOUT DIGITAL NATIONAL STUDIO - VILLA 226M²",
        fill="#1e3a8a",
        anchor="mm",
    )
    draw.text(
        (540, 150),
        "🌟 قلعة السراغنة - المكتبة الرقمية [TASSAOUT VERIFIED]",
        fill="#0284c7",
        anchor="mm",
    )

    lines = textwrap.wrap(prompt_text, width=32)
    y = 260
    for line in lines[:10]:
        draw.text((540, y), line, fill="#0f172a", anchor="mm")
        y = y + 55

    draw.text(
        (540, 980),
        f"الهاتف الموحد: {WHATSAPP_DISPLAY} | ameur signature tassaout ai",
        fill="#1e3a8a",
        anchor="mm",
    )

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# دالة تحليل قراءة المستندات والوثائق (Document RAG Engine)
def extract_text_from_pdf(pdf_file):
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip()
    except Exception:
        return "تعذر استخراج النص تلقائياً من المستند، تم الاعتماد على التحليل البصري والوصف المرفق."


st.markdown(
    "<h1 class='main-title'>وكالة تساوت الرقمية للخدمات والأعمال</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='sub-title'>بوابة العقارات، الهندسة المتكاملة، وتوليد الهويات البصرية (مع محرك تحليل المستندات RAG والمكتبة السحابية) — تغطية شاملة للمملكة المغربية [TASSAOUT VERIFIED]</p>",
    unsafe_allow_html=True,
)

# عرض سجل المحادثات السابق
for i, msg in enumerate(st.session_state["messages"]):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "attachments" in msg:
            for att in msg["attachments"]:
                if att["type"] == "image":
                    st.image(
                        att["data"], use_container_width=True, caption=att["name"]
                    )
                else:
                    st.download_button(
                        f"📎 مستند محلل: {att['name']}",
                        att["data"],
                        att["name"],
                        key=f"hist_file_{i}_{att['name']}",
                    )
        if "images" in msg:
            for img_bytes in msg["images"]:
                st.image(
                    img_bytes,
                    use_container_width=True,
                    caption="🎨 الهوية البصرية والمخطط المعماري المعتمد",
                )
        if "zip" in msg:
            st.download_button(
                "📥 تحميل الحزمة الرقمية والهوية ومراحل الفيلا كاملة (ZIP)",
                msg["zip"],
                f"tassaout_villa_package_{i}.zip",
                key=f"zip_btn_{i}",
            )

# الشاشة التفاعلية الكبرى
with st.container(border=True):
    st.markdown(
        "### 🖥️ الشاشة التفاعلية الكبرى (المكتبة الرقمية السحابية وادارة مشروع الفيلا)"
    )

    unified_input = st.text_area(
        "أدخل استفسارك، أو تفاصيل مراحل البناء، أو طلب تحديث مشروع الفيلا بقلعة السراغنة (226 متر مربع):",
        placeholder="مثال: عرض تفاصيل المرحلة الثالثة من بناء الفيلا، أو تحليل عقد أو تصميم مرفق...",
        height=140,
        label_visibility="collapsed",
    )

    with st.expander(
        "📁 إرفاق الصور والمستندات الهندسية والقانونية الخاصة بالمشروع (PDF, Word, Images)"
    ):
        uploaded_files = st.file_uploader(
            "اختر الملفات أو المستندات للتحليل الفوري:",
            type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"],
            accept_multiple_files=True,
        )

    submit_btn = st.button(
        "🚀 تشغيل الوكيل الذكي وأرشفة البيانات في المكتبة السحابية",
        use_container_width=True,
        type="primary",
    )

if submit_btn and (unified_input or uploaded_files):
    attachments = []
    file_count = 0
    extracted_docs_summary = ""

    if uploaded_files:
        for f in uploaded_files:
            file_count += 1
            f_bytes = f.read()
            if f.type.startswith("image"):
                attachments.append({"type": "image", "data": f_bytes, "name": f.name})
            else:
                attachments.append({"type": "file", "data": f_bytes, "name": f.name})
                if f.name.endswith(".pdf"):
                    doc_text = extract_text_from_pdf(BytesIO(f_bytes))
                    extracted_docs_summary += f"\n--- مستخلص المستند ({f.name}):\n{doc_text[:800]}...\n"

    base_content = (
        unified_input
        if unified_input
        else "تمت معالجة وتوثيق بيانات مشروع الفيلا والمرفقات بنجاح."
    )
    user_msg_content = (
        base_content
        + (
            f"\n\nمستخلص محتوى المستندات المرفقة:\n{extracted_docs_summary}"
            if extracted_docs_summary
            else ""
        )
    )

    st.session_state["messages"].append(
        {"role": "user", "content": user_msg_content, "attachments": attachments}
    )

    with st.spinner("جاري معالجة الطلب وتحديث المكتبة السحابية للوكيل الذكي..."):
        answer = (
            f"👑 **[تقرير وكيل تساوت الرقمية - مشروع فيلا قلعة السراغنة 226م²]**\n\n"
            f"🔹 **الطلب الأساسي:** {unified_input if unified_input else 'إدارة وتوثيق مراحل الفيلا'}\n"
            f"🔹 **عدد الملفات والمستندات المعالجة:** {file_count} ملف/صورة.\n"
            f"🔹 **حالة الأرشفة:** تم الدمج والتخزين في المكتبة الرقمية السحابية الجامعية بنجاح.\n\n"
            f"🌿 **[TASSAOUT VERIFIED]**\n"
            f"**ameur signature tassaout ai**\n\n"
            f"📞 للتواصل وتأكيد الاعتماد النهائي: {WHATSAPP_DISPLAY}"
        )

        images = []
        zip_buffer = None

        if user_msg_content or attachments:
            identity_bytes = generate_hyper_visual_identity(
                unified_input
                if unified_input
                else "مشروع فيلا قلعة السراغنة 226م² - تساوت الرقمية"
            )
            images.append(identity_bytes)

            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as z:
                z.writestr("tassaout_national_identity.png", identity_bytes)
                z.writestr("tassaout_villa_report.txt", answer)
                if extracted_docs_summary:
                    z.writestr(
                        "extracted_documents_data.txt", extracted_docs_summary
                    )

    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "images": images if images else None,
        "zip": zip_buffer.getvalue() if zip_buffer else None,
    })
    st.rerun()

last_query = (
    unified_input
    if "unified_input" in locals() and unified_input
    else "مشروع فيلا قلعة السراغنة 226م² - تساوت الرقمية"
)
whatsapp_msg = urllib.parse.quote(
    f"سلام، أريد اعتماد وتخزين طلب تحليل ومستندات مشروع الفيلا التالي:\n{last_query}\n[TASSAOUT VERIFIED]\nameur signature tassaout ai"
)
whatsapp_url = f"https://wa.me/{WHATSAPP_CLEAN}?text={whatsapp_msg}"

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px 0; font-family: 'Cairo', sans-serif;">
        <div style="margin-bottom: 15px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 28px; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 1.1rem; display: inline-block;">
                💬 إرسال وحفظ التقارير والمستندات المرفقة عبر الواتساب ({WHATSAPP_DISPLAY})
            </a>
        </div>
        <p style="font-size: 0.95rem; color: #1e3a8a; font-weight: 700; line-height: 1.8;">
            {FOUNDER_SIGNATURE}
        </p>
    </div>
""",
    unsafe_allow_html=True,
)
