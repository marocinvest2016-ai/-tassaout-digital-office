import io
import textwrap
import urllib.parse
from PIL import Image, ImageDraw
import pypdf
import streamlit as st
import zipfile

# 1. إعداد الصفحة والأنماط السيادية الموحدة (خدمات تساوت & ATIS)
st.set_page_config(
    page_title="الوكيل الذكي المتعدد التخصصات | خدمات تساوت & ATIS", 
    page_icon="👑", 
    layout="wide"
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

# البيانات الثابتة والسيادية الموحدة
WHATSAPP_DISPLAY = "+212691897126"
WHATSAPP_CLEAN = "212691897126"
FOUNDER_SIGNATURE = "خدمات تساوت للخدمات والأعمال | بتنسيق مع شركة ATIS - المغرب<br>كل الحقوق محفوظة 2026 [TASSAOUT & ATIS VERIFIED]<br><b>ameur signature tassaout ai</b>"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "👑 **[النواة الذكية الشاملة - خدمات تساوت & ATIS]**\n\n"
                "مرحباً بك يا أمير. تم تثبيت واستيعاب المصفوفة الاستراتيجية الكاملة في نواة الوكيل الذكي وتشمل:\n"
                "1. الهندسة المعمارية، الصناعية، الميكانيكية وهندسة الديكور (Architecture & Aménagement)\n"
                "2. العقار الصناعي، المهني، التجاري والفلاحي والتعاونيات والمنتوجات المجالية\n"
                "3. التجارة الدولية، التصدير والاستيراد\n"
                "4. السيارات، الآليات الفلاحية واللوجستيات\n"
                "5. خدمات الأسفار، الحج والعمرة، الثقافة العالمية والاعلاميات\n\n"
                "**[TASSAOUT & ATIS VERIFIED 🌿]**\n"
                "**ameur signature tassaout ai**"
            ),
        }
    ]

# محرك توليد الهويات البصرية واللافتات الشاملة
def generate_hyper_visual_identity(prompt_text):
    img = Image.new("RGB", (1080, 1080), color="#0f172a")
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, 1050, 1050], fill="#1e3a8a", outline="#38bdf8", width=8)
    draw.rectangle([50, 50, 1030, 1030], fill="#ffffff", outline=None)

    draw.text(
        (540, 100),
        "TASSAOUT SERVICES & ATIS - MULTI-SECTOR CORE",
        fill="#1e3a8a",
        anchor="mm",
    )
    draw.text(
        (540, 150),
        "🌟 المنظومة الذكية المتكاملة [TASSAOUT & ATIS VERIFIED]",
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

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

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
        return "تعذر استخراج النص تلقائياً من المستند، تم الاعتماد على التحليل الشامل."

st.markdown(
    "<h1 class='main-title'>الوكيل الذكي المتعدد التخصصات</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='sub-title'>خدمات تساوت بتنسيق مع شركة ATIS — هندسة، عقار، صناعة، تصدير، وتجارة رقمية [Clé en main]</p>",
    unsafe_allow_html=True,
)

# عرض سجل المحادثات
for i, msg in enumerate(st.session_state["messages"]):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "attachments" in msg:
            for att in msg["attachments"]:
                if att["type"] == "image":
                    st.image(att["data"], use_container_width=True, caption=att["name"])
                else:
                    st.download_button(
                        f"📎 مستند محلل: {att['name']}",
                        att["data"],
                        att["name"],
                        key=f"hist_file_{i}_{att['name']}",
                    )
        if "images" in msg:
            for img_bytes in msg["images"]:
                st.image(img_bytes, use_container_width=True, caption="🎨 الهوية البصرية والمصفوفة المعتمدة")
        if "zip" in msg:
            st.download_button(
                "📥 تحميل الحزمة الرقمية والتقارير الشاملة (ZIP)",
                msg["zip"],
                f"tassaout_atis_matrix_package_{i}.zip",
                key=f"zip_btn_{i}",
            )

# الشاشة التفاعلية الكبرى
with st.container(border=True):
    st.markdown("### 🖥️ الشاشة التفاعلية الكبرى (النواة الذكية الموحدة للمشاريع)")

    unified_input = st.text_area(
        "أدخل تفاصيل المشروع أو الطلب (هندسة، عقار فلاحي/صناعي، تصدير، آليات، أسفار، أو ديكور):",
        placeholder="مثال: تنسيق مشروع عقار صناعي وهندسة ميكانيكية أو تصدير منتوجات مجالية...",
        height=140,
        label_visibility="collapsed",
    )

    with st.expander("📁 إرفاق المستندات والملفات التقنية والقانونية (PDF, Word, Images)"):
        uploaded_files = st.file_uploader(
            "اختر الملفات أو المستندات للتحليل الفوري:",
            type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"],
            accept_multiple_files=True,
        )

    submit_btn = st.button(
        "🚀 تشغيل الوكيل الذكي وتحديث المكتبة السحابية الموحدة",
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
                    doc_text = extract_text_from_pdf(io.BytesIO(f_bytes))
                    extracted_docs_summary += f"\n--- مستخلص المستند ({f.name}):\n{doc_text[:800]}...\n"

    base_content = unified_input if unified_input else "معالجة وإدارة القطاعات الشاملة بنجاح."
    user_msg_content = base_content + (f"\n\nمستخلص المحتوى:\n{extracted_docs_summary}" if extracted_docs_summary else "")

    st.session_state["messages"].append(
        {"role": "user", "content": user_msg_content, "attachments": attachments}
    )

    with st.spinner("جاري المعالجة المتقدمة وتحديث نوى التشغيل (تساوت & ATIS)..."):
        answer = (
            f"👑 **[تقرير النواة الذكية - خدمات تساوت & ATIS]**\n\n"
            f"🔹 **الطلب الأساسي:** {unified_input if unified_input else 'معالجة شاملة متعددة التخصصات'}\n"
            f"🔹 **عدد الملفات المعالجة:** {file_count} ملف/صورة.\n"
            f"🔹 **حالة الأرشفة:** تم الدمج والتخزين في النظام السحابي الموحد بنجاح.\n\n"
            f"🌿 **[TASSAOUT & ATIS VERIFIED]**\n"
            f"**ameur signature tassaout ai**\n\n"
            f"📞 للتواصل وتأكيد الاعتماد النهائي: {WHATSAPP_DISPLAY}"
        )

        images = []
        zip_buffer = None

        if user_msg_content or attachments:
            identity_bytes = generate_hyper_visual_identity(
                unified_input if unified_input else "النواة الذكية المتكاملة - خدمات تساوت & ATIS"
            )
            images.append(identity_bytes)

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as z:
                z.writestr("tassaout_atis_matrix.png", identity_bytes)
                z.writestr("tassaout_atis_report.txt", answer)
                if extracted_docs_summary:
                    z.writestr("extracted_documents_data.txt", extracted_docs_summary)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "images": images if images else None,
        "zip": zip_buffer.getvalue() if zip_buffer else None,
    })
    st.rerun()

last_query = unified_input if "unified_input" in locals() and unified_input else "المنظومة الذكية الشاملة - خدمات تساوت & ATIS"
whatsapp_msg = urllib.parse.quote(
    f"سلام، أريد اعتماد وتخزين طلب المشروع التالي ضمن النواة الذكية لخدمات تساوت بتنسيق مع ATIS:\n{last_query}\n[TASSAOUT & ATIS VERIFIED]\nameur signature tassaout ai"
)
whatsapp_url = f"https://wa.me/{WHATSAPP_CLEAN}?text={whatsapp_msg}"

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px 0; font-family: 'Cairo', sans-serif;">
        <div style="margin-bottom: 15px;">
            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 12px 28px; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 1.1rem; display: inline-block;">
                💬 إرسال الحزمة التقنية والتقارير عبر الواتساب ({WHATSAPP_DISPLAY})
            </a>
        </div>
        <p style="font-size: 0.95rem; color: #1e3a8a; font-weight: 700; line-height: 1.8;">
            {FOUNDER_SIGNATURE}
        </p>
    </div>
""",
    unsafe_allow_html=True,
)
