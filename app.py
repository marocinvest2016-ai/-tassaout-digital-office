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
    page = st.radio("التنقل", ["الرئيسية", "الآليات الفلاحية", "توليد التقارير PDF"])

# 4. الصفحة الرئيسية
if page == "الرئيسية":
    st.title("💐 خدمات السراغنة للتسويق الرقمي")
    st.markdown("### المعرض الرقمي للسيارات والآليات الفلاحية")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["⚙️ مركز التحكم", "📂 تحليل الملفات"])
    
    with tab1:
        directive = st.text_area("توجيه الوكيل السيادي", value="أنت الوكيل السيادي لخدمات السراغنة بقلعة السراغنة وبني ملال. قدم إجابات احترافية.", height=150)
        if st.button("🚀 تحديث التوجيه"):
            st.success("تم تحديث التوجيه بنجاح.")
    
    with tab2:
        uploaded_file = st.file_uploader("ارفع صورة أو PDF للآلية", type=["jpg", "png", "pdf"])
        if uploaded_file:
            if uploaded_file.type.startswith("image/"):
                st.image(Image.open(uploaded_file), caption=uploaded_file.name, use_container_width=True)
            else:
                st.success(f"تم رفع: {uploaded_file.name}")

# 5. صفحة الآليات الفلاحية
elif page == "الآليات الفلاحية":
    st.header("🚜 Sraghna Digital Gallery")
    st.markdown("المعرض الرقمي الأول للآليات الفلاحية بقلعة السراغنة")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Massey Ferguson 290", "الحالة: ممتازة")
    with col2: st.metric("محاريث", "متوفرة للتأجير")
    with col3: st.metric("معدات ثقيلة", "جاهزة للميدان")
    
    st.link_button("💬 طلب عبر واتساب", "https://wa.me/212691897126")

# 6. صفحة توليد PDF
elif page == "توليد التقارير PDF":
    st.header("📑 DANA-Document Engine")
    SERVICES_DB = {
        "🚜 الآليات الفلاحية": "جرارات Massey Ferguson، محاريث، تأجير",
        "🏡 العقار": "بقع تجزئة الهدى، أراضي فلاحية",
        "💼 الأعمال": "دراسة جدوى، شراكات",
        "🚗 DANA Media": "تأجير سيارات بمراكش"
    }
    
    if st.button("⚡ توليد البروشور الرسمي"):
        pdf_path = generate_official_pdf_report("BROCHURE OFFICIELLE", SERVICES_DB, "Brochure_Tassaout.pdf")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 تحميل PDF", f, "Brochure_Tassaout.pdf", "application/pdf")
        st.success(f"تم التوليد: {pdf_path}")

st.markdown("---")
st.markdown("**📞 التواصل:** +212691897126 | marocinvest2012@gmail.com")
st.caption("TASSAOUT OMEGA OS v4.1 - جميع الحقوق محفوظة 2026")
