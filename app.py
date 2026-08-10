import streamlit as st
from datetime import datetime
import os
import urllib.parse
from PIL import Image
import google.generativeai as genai
from PyPDF2 import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# ==========================================
# 1. تهيئة النظام السيادي والإعدادات
# ==========================================
st.set_page_config(page_title="TASSAOUT OMEGA OS v4.1", layout="wide", page_icon="👑")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_status = "✅ Active"
except Exception as e:
    api_status = "❌ API Key Missing in Secrets"

UPLOAD_FOLDER = "uploads"
DOCS_FOLDER = "documents_officiels"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCS_FOLDER, exist_ok=True)

# ==========================================
# 2. الذاكرة السيادية (Session State)
# ==========================================
if "injection_memory" not in st.session_state:
    st.session_state.injection_memory = "أنت الوكيل السيادي لمكتب تساوت الرقمي بقلعة السراغنة. قدم إجابات احترافية ودقيقة."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "سيدي الرئيس، نظام TASSAOUT OMEGA OS v4.1 بكامل الأركان جاهز للتشغيل السيادي."}]

if "uploaded_file_obj" not in st.session_state:
    st.session_state.uploaded_file_obj = None

SERVICES_DB = {
    "🏡 العقار": "بقع تجزئة الهدى، أراضي فلاحية، كراء وبيع",
    "💼 الأعمال": "دراسة جدوى، شراكات استراتيجية، استشارات",
    "🛠️ الخدمات": "تصوير احترافي 100MP، لوجستيات، شحن",
    "🕋 الحج والعمرة": "عروض عمرة 15 يوم، تنظيم حج القرعة",
    "🎉 الحفلات": "تموين ملكي، تزيين، دي جي، تصوير سينمائي",
    "🎵 الرياضة": "ملاعب القرب، تأطير المدربين، دوريات جهوية",
    "🎓 الدراسة": "دورات تكوينية، دعم مدرسي رقمي، تكوين مهني",
    "🌍 الترجمة": "ترجمة معتمدة، ملفات فيزا وإقامة، استشارات سفر"
}

# ==========================================
# 3. الدوال المركزية (DANA Engine)
# ==========================================
def generate_whatsapp_link(title, content):
    full_message = f"--- 👑 {title} 👑 ---\n[ TASSAOUT OMEGA OS v4.1 ]\n\n{content}\n\n✒️ Ameur\n⚡ SOVEREIGN SYSTEM"
    return "https://wa.me/212691897126?text=" + urllib.parse.quote(full_message)

def analyze_with_gemini(prompt, image=None, pdf_text=None):
    full_prompt = f"التوجيه السيادي الحالي: {st.session_state.injection_memory}\n\nسؤال المستخدم: {prompt}"
    if pdf_text:
        full_prompt += f"\n\n[محتوى ملف الـ PDF المرفوع]:\n{pdf_text[:5000]}..."

    parts = [full_prompt]
    if image:
        parts.append(image)
    
    try:
        response = model.generate_content(parts)
        return response.text
    except Exception as e:
        return f"❌ خطأ في معالجة Gemini: تأكد من صحة الـ API Key في إعدادات السحاب. التفاصيل: {e}"

def generate_ai_image_prompt(description):
    return f"Photorealistic, cinematic, luxury ad poster for 'TASSAOUT OMEGA OS' in Kalaat Sraghna, Morocco. Theme: {description}. Colors: Royal Gold (#D4AF37) and Matte Black (#0A0A0A). High tech, detailed neural network background, Moroccan architectural elements. Hasselblad X2D, 100MP."

def generate_official_pdf_report(report_title, sector_data, filename):
    file_path = os.path.join(DOCS_FOLDER, filename)
    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    gold_color = colors.HexColor("#D4AF37")
    dark_bg = colors.HexColor("#0A0A0A")

    title_style = ParagraphStyle("RoyalTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=20, textColor=gold_color, alignment=1, spaceAfter=12)
    subtitle_style = ParagraphStyle("RoyalSubtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10, textColor=colors.grey, alignment=1, spaceAfter=30)
    
    elements.append(Paragraph("👑 BUREAU NUMÉRIQUE TASSAOUT 👑", title_style))
    elements.append(Paragraph("SYSTÈME SOUVERAIN - قلعة السراغنة، المغرب", subtitle_style))
    elements.append(Paragraph(f"<b>{report_title}</b>", ParagraphStyle("DocTitle", parent=styles["Heading2"], fontSize=16, textColor=colors.black, alignment=1, spaceAfter=20)))

    table_data = [["القطاع / Secteur", "الخدمة / Prestation Stratégique"]]
    for k, v in sector_data.items():
        table_data.append([Paragraph(k, styles["Normal"]), Paragraph(v, styles["Normal"])])
    
    t = Table(table_data, colWidths=[160, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), dark_bg),
        ('TEXTCOLOR', (0,0), (-1,0), gold_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, gold_color),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 50))

    footer_style = ParagraphStyle("RoyalFooter", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, textColor=dark_bg, alignment=2)
    elements.append(Paragraph("✒️ Signature : Ameur signature", footer_style))
    elements.append(Paragraph("⚡ TASSAOUT OMEGA OS v4.1", footer_style))

    doc.build(elements)
    return file_path

# ==========================================
# 4. الواجهة الرئيسية (Dashboard Structure)
# ==========================================
st.title("👑 TASSAOUT OMEGA OS v4.1 - AUTONOMOUS SOVEREIGN COMMAND")
st.caption(f"نطاق التشغيل: هندسة النظم الرقمية والذكاء الاصطناعي السيادي | حالة النظام: {api_status}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 القيادة", "⚡ الأتمتة", "🎨 التوليد", "👥 بوابة العميل", "📑 تقارير PDF"])

with tab1:
    col_ctrl, col_chat = st.columns([1, 3])
    with col_ctrl:
        st.subheader("⚙️ مركز التحكم السيادي")
        new_injection = st.text_area("أمر الحقن الرئاسي (توجيه الوكيل):", value=st.session_state.injection_memory, height=120)
        if st.button("🚀 تحديث التوجيه", type="primary"):
            st.session_state.injection_memory = new_injection
            st.success("✅ تم تحديث التوجيه السيادي")
        
        st.markdown("---")
        st.markdown("📂 **تحليل الملفات الذكي:**")
        uploaded_file = st.file_uploader("اختر صورة أو ملف PDF للتحليل", type=["jpg", "jpeg", "png", "webp", "pdf"], key="uploader1")
        if uploaded_file:
            st.session_state.uploaded_file_obj = uploaded_file
            st.success(f"تم رفع الملف: {uploaded_file.name}")
            if uploaded_file.type.startswith("image"):
                st.image(Image.open(uploaded_file), caption="المرفق البصري", use_column_width=True)

    with col_chat:
        st.subheader("💬 مركز القيادة التشغيلي")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("أعط الأمر للوكيل السيادي..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.spinner("جاري معالجة الأمر..."):
                image_part = None
                pdf_text_part = None
                if st.session_state.uploaded_file_obj:
                    file = st.session_state.uploaded_file_obj
                    if file.type.startswith("image"):
                        image_part = Image.open(file)
                    elif file.type == "application/pdf":
                        reader = PdfReader(file)
                        pdf_text_part = "".join([page.extract_text() for page in reader.pages])
                
                ai_response = analyze_with_gemini(prompt, image=image_part, pdf_text=pdf_text_part)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.uploaded_file_obj = None 
                st.rerun()

with tab2:
    st.subheader("⚡ DANA-Automation: التقارير التلقائية")
    report_content = st.text_area("نص التقرير اليومي السيادي:", f"تقرير الأنشطة اليومية - {datetime.now().strftime('%Y-%m-%d')}\n\n- حالة النظام: تشغيل سيادي كامل بقلعة السراغنة.")
    if st.button("🔗 إنشاء رابط الإرسال للواتساب"):
        wa_link = generate_whatsapp_link("تقرير الأنشطة اليومية", report_content)
        st.success("✅ تم إنشاء الرابط بنجاح")
        st.link_button("📱 إرسال التقرير الآن للواتساب", wa_link, type="primary")

with tab3:
    st.subheader("🎨 DANA-Branding: مولد الصور الإعلانية")
    img_desc = st.text_input("صف الصورة المطلوبة:", "مجمع تجاري فاخر وسط مدينة قلعة السراغنة ليلاً")
    if st.button("🚀 توليد الـ Prompt السيادي"):
        st.code(generate_ai_image_prompt(img_desc), language="text")

with tab4:
    st.subheader("👥 بوابة العميل السيادية")
    client_msg = st.text_input("اكتب سؤالك أو طلبك هنا:")
    if st.button("إرسال للوكيل", key="client_btn"):
        if client_msg:
            with st.spinner("جاري الرد..."):
                st.markdown(f"**الوكيل:** {analyze_with_gemini(f'بصفتك وكيل تساوت، أجب العميل بمهنية عالية: {client_msg}')}")
                st.link_button("📱 تواصل معنا واتساب", "https://wa.me/212691897126")

with tab5:
    st.subheader("📑 DANA-PDF: تحميل الوثائق الرسمية")
    doc_type = st.selectbox("اختر نوع الوثيقة:", ["تقرير القطاعات الشامل", "بروشور الخدمات السيادي"])
    if st.button("⚡ تحميل PDF بالهوية الملكية"):
        with st.spinner("جاري توليد الوثيقة..."):
            filename = f"Tassaout_Rapport_{datetime.now().strftime('%Y%m%d')}.pdf" if doc_type == "تقرير القطاعات الشامل" else "Brochure_Services_Souverains.pdf"
            pdf_path = generate_official_pdf_report(doc_type, SERVICES_DB, filename)
            with open(pdf_path, "rb") as f:
                st.download_button(label="📥 تحميل الملف النهائي", data=f, file_name=filename, mime="application/pdf")
            st.success(f"✅ تم توليد الوثيقة: {filename}")
