```python
import streamlit as st
from PIL import Image
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# 1. إعدادات الصفحة السيادية
st.set_page_config(
    page_title="خدمات السراغنة - TASSAOUT OMEGA OS",
    page_icon="👑",
    layout="wide"
)

DOCS_FOLDER = "documents_officiels"
os.makedirs(DOCS_FOLDER, exist_ok=True)

# 2. دالة توليد PDF السيادية
def generate_official_pdf_report(report_title, sector_data, filename="Rapport_Tassaout.pdf"):
    file_path = os.path.join(DOCS_FOLDER, filename)
    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    gold_color = colors.HexColor("#D4AF37")
    dark_bg = colors.HexColor("#0A0A0A")
    
    title_style = ParagraphStyle("RoyalTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, textColor=gold_color, alignment=1, spaceAfter=10)
    subtitle_style = ParagraphStyle("RoyalSubtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10, textColor=colors.grey, alignment=1, spaceAfter=20)
    
    elements.append(Paragraph("👑 BUREAU NUMÉRIQUE TASSAOUT 👑", title_style))
    elements.append(Paragraph(f"<b>{report_title}</b> | Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>قلعة السراغنة, Maroc", subtitle_style))
    elements.append(Spacer(1, 15))
    
    table_data = [["القطاع / Secteur", "الخدمة / Prestation"]]
    for k, v in sector_data.items(): table_data.append([k, v])
    
    t = Table(table_data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), dark_bg), ("TEXTCOLOR", (0, 0), (-1, 0), gold_color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, gold_color), ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("✒️ Signature : Ameur signature<br/>⚡ TASSAOUT OMEGA OS v4.1", subtitle_style))
    doc.build(elements)
    return file_path

# 3. الشريط الجانبي
with st.sidebar:
    st.title("👑 مركز القيادة السيادي")
    st.markdown("**TASSAOUT OMEGA OS v4.1**")
    page = st.radio("التنقل", [
        "الرئيسية", 
        "المعرض الرقمي (Gallery)", 
        "رفع الصور من الهاتف (Sélectionner)", 
        "توليد التقارير PDF", 
        "الأتمتة (Automation)", 
        "التوليد الذكي (Generative)",
        "بوابة العميل (Client Portal)",
        "واجهة Gemini التفاعلية (Gemini Interface)",
        "حقن Super Agentic AI (Multi-Domain)",
        "توليد المحتوى والهوية البصرية (AI Studio)"
    ])

# 4. الصفحة الرئيسية
if page == "الرئيسية":
    st.title("💐 خدمات السراغنة للتسويق الرقمي")
    st.markdown("### المعرض الرقمي للسيارات والآليات الفلاحية")
    st.markdown("---")
    directive = st.text_area("توجيه الوكيل السيادي", value="أنت الوكيل السيادي لخدمات السراغنة بقلعة السراغنة وبني ملال. قدم إجابات احترافية.", height=150)
    if st.button("🚀 تحديث التوجيه"):
        st.success("تم تحديث التوجيه بنجاح.")

# 5. صفحة المعرض الرقمي
elif page == "المعرض الرقمي (Gallery)":
    st.header("🚜 Sraghna Digital Gallery")
    uploaded_files = st.file_uploader("اختر صور الآليات:", type=["jpg", "png", "webp"], accept_multiple_files=True)
    if uploaded_files:
        cols = st.columns(3)
        for i, file in enumerate(uploaded_files):
            cols[i % 3].image(Image.open(file), use_container_width=True)
    st.link_button("💬 طلب عبر واتساب", "https://wa.me/212691897126")

# 6. رفع الصور من الهاتف
elif page == "رفع الصور من الهاتف (Sélectionner)":
    st.header("📱 مركز تحميل الصور من الهاتف المحمول")
    selected_files = st.file_uploader("Sélectionner des images", type=["jpg", "jpeg", "png", "webp", "heic"], accept_multiple_files=True, key="phone_gallery_upload")
    if selected_files:
        st.success(f"تم بنجاح اختيار {len(selected_files)} صورة من هاتفك سيدي الرئيس 👑")
        cols = st.columns(2)
        for index, img_file in enumerate(selected_files):
            cols[index % 2].image(Image.open(img_file), caption=f"صورة {index+1}: {img_file.name}", use_container_width=True)

# 7. توليد التقارير PDF
elif page == "توليد التقارير PDF":
    st.header("📑 DANA-Document Engine")
    SERVICES_DB = {"🚜 الآليات الفلاحية": "جرارات، محاريث", "🏡 العقار": "أراضي", "💼 الأعمال": "دراسة جدوى", "🚗 DANA Media": "تأجير سيارات"}
    if st.button("⚡ توليد البروشور الرسمي"):
        pdf_path = generate_official_pdf_report("BROCHURE OFFICIELLE", SERVICES_DB, "Brochure_Tassaout.pdf")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 تحميل PDF", f, "Brochure_Tassaout.pdf", "application/pdf")

# 8. الأتمتة
elif page == "الأتمتة (Automation)":
    st.header("⚡ DANA-Automation Hub")
    if st.selectbox("المهمة:", ["مزامنة واتساب", "تصدير تقارير", "إرسال تلقائي"]):
        if st.button("▶️ تنفيذ"): st.success("تم تنفيذ المهمة.")

# 9. التوليد الذكي
elif page == "التوليد الذكي (Generative)":
    st.header("🧠 DANA-Gen AI")
    user_prompt = st.text_input("أدخل موضوع المحتوى:")
    if st.button("✨ توليد محتوى"):
        st.success("تم التوليد بنجاح.")

# 10. بوابة العميل
elif page == "بوابة العميل (Client Portal)":
    st.header("🔐 بوابة العميل التفاعلية")
    client_name = st.text_input("اسم العميل / الشركة:")
    client_phone = st.text_input("رقم الهاتف / واتساب:")
    if st.button("📤 إرسال الطلب للوسيط"):
        if client_name and client_phone:
            st.success(f"تم تسجيل طلبك بنجاح يا {client_name}!")
            st.link_button("💬 تأكيد الطلب عبر واتساب", f"https://wa.me/212691897126?text=مرحباً، أنا العميل {client_name}")

# 11. واجهة Gemini
elif page == "واجهة Gemini التفاعلية (Gemini Interface)":
    st.header("✨ واجهة Gemini السيادية للتفاعل المباشر")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "أهلاً بك سيدي الرئيس."}]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        resp = f"تم استلام توجيهك السيادي: '{prompt}' وجاري تنفيذه."
        st.session_state.messages.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"): st.markdown(resp)

# 12. حقن Super Agentic AI
elif page == "حقن Super Agentic AI (Multi-Domain)":
    st.header("🧬 Super Multidomaine Agentic AI - مركز الحقن السيادي")
    selected_domain = st.selectbox("اختر النطاق المستهدف للحقن (Domain):", ["🌍 النطاق الشامل", "🚜 قطاع الآليات والفلاحة", "🏡 قطاع العقار"])
    agent_instruction = st.text_area("حقل الحقن المباشر:", value="أنت نظام Super Agentic AI المخصص لإدارة منظومة السراغنة.", height=150)
    if st.button("⚡ حقن وتنشيط النظام السيادي"):
        st.success(f"تم حقن التوجيه بنجاح في النطاق: {selected_domain} 👑")

# 13. واجهة توليد المحتوى الكتابي والهوية البصرية (AI Studio)
elif page == "توليد المحتوى والهوية البصرية (AI Studio)":
    st.header("🎨✨ استوديو توليد المحتوى الكتابي والهوية البصرية")
    st.markdown("منصة سيادية لتوليد الإعلانات، النصوص التسويقية، وتحديد الهوية البصرية الملكية (Royal Gold & Black).")
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        content_type = st.selectbox(
            "اختر نوع المحتوى الكتابي:",
            ["إعلان تجاري لـ واتساب", "منشور تسويقي للآليات الفلاحية", "عروض العقار والأراضي", "رسالة ترويجية رسمية"]
        )
    with col_opt2:
        visual_theme = st.selectbox(
            "اختر الهوية البصرية:",
            ["Royal Gold & Black (ملكي أسود وذهبي)", "Emerald & Dark (أخضر زمردي وداكن)", "Cinematic Minimalist (سينيمائي مبسط)"]
        )
        
    campaign_topic = st.text_input("أدخل موضوع الحملة أو تفاصيل الآلية/العقار:", value="عرض خاص لجرارات Massey Ferguson بقلعة السراغنة")
    
    if st.button("🚀 توليد المحتوى والهوية البصرية الآن"):
        st.success("تم توليد المحتوى والهوية البصرية بنجاح سيدي الرئيس 👑")
        
        st.markdown("---")
        st.subheader("📝 المحتوى الكتابي المولّد (جاهز للنسخ ونشره):")
        
        generated_text = f"""
        🔥 **عرض حصري ومباشر من قلعة السراغنة وبني ملال** 🔥
        
        نقدم لكم أفضل الحلول والخدمات ضمن منظومة **TASSAOUT OMEGA OS**:
        🎯 **الموضوع:** {campaign_topic}
        
        🚜 متوفر الآن بجاهزية تامة للميدان وبأفضل الشروط الفلاحية والتجارية.
        
        📞 **للحجز والاستفسار المباشر:**
        تواصل معنا عبر الوكيل الرسمي أو عبر الزر أدناه:
        [+212691897126](https://wa.me/212691897126?text=مرحباً، أود الاستفسار بخصوص: {campaign_topic})
        
        📧 البريد الإلكتروني: marocinvest2012@gmail.com
        """
        st.info(generated_text)
        
        st.markdown("---")
        st.subheader("🎨 مواصفات الهوية البصرية المقترحة:")
        st.markdown(f"""
        * **الطابع البصري:** {visual_theme}
        * **الخطوط:** Montserrat / Helvetica-Bold
        * **الألوان المعتمدة:** تدرجات الذهبي الفاخر (`#D4AF37`) مع الخلفية الداكنة (`#0A0A0A`).
        * **التوقيع السيادي:** `Ameur signature - Sraghna Immobilière`
        """)
        
        st.link_button("💬 مشاركة المحتوى مباشرة عبر واتساب", f"https://wa.me/212691897126?text=مرحباً، إليك المحتوى المولّد للحملة: {campaign_topic}")

st.markdown("---")
st.markdown("**📞 التواصل:** +212691897126 | marocinvest2012@gmail.com")
st.caption("TASSAOUT OMEGA OS v4.1 - جميع الحقوق محفوظة 2026")

```
