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
    page_title="خدمات السراغنة الشاملة - TASSAOUT OMEGA OS",
    page_icon="👑",
    layout="wide"
)

DOCS_FOLDER = "documents_officiels"
os.makedirs(DOCS_FOLDER, exist_ok=True)

# 2. دالة توليد PDF السيادية الشاملة
def generate_official_pdf_report(report_title, sector_data, filename="Rapport_Tassaout_Global.pdf"):
    file_path = os.path.join(DOCS_FOLDER, filename)
    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    gold_color = colors.HexColor("#D4AF37")
    dark_bg = colors.HexColor("#0A0A0A")
    
    title_style = ParagraphStyle("RoyalTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, textColor=gold_color, alignment=1, spaceAfter=10)
    subtitle_style = ParagraphStyle("RoyalSubtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10, textColor=colors.grey, alignment=1, spaceAfter=20)
    
    elements.append(Paragraph("👑 BUREAU NUMÉRIQUE TASSAOUT - GROUPE MULTI-SECTORIEL 👑", title_style))
    elements.append(Paragraph(f"<b>{report_title}</b> | Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}<br/>قلعة السراغنة، مراكش وبني ملال، المغرب", subtitle_style))
    elements.append(Spacer(1, 15))
    
    table_data = [["القطاع / Secteur", "الخدمات والأنشطة / Prestations"]]
    for k, v in sector_data.items(): table_data.append([k, v])
    
    t = Table(table_data, colWidths=[180, 320])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), dark_bg), ("TEXTCOLOR", (0, 0), (-1, 0), gold_color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, gold_color), ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("✒️ Signature : Ameur signature<br/>⚡ TASSAOUT OMEGA OS v4.1 - Multi-Domain Industrial & Commercial", subtitle_style))
    doc.build(elements)
    return file_path

# 3. الشريط الجانبي السيادي
with st.sidebar:
    st.title("👑 مركز القيادة الشامل")
    st.markdown("**TASSAOUT OMEGA OS v4.1**")
    page = st.radio("التنقل بين الوحدات:", [
        "الرئيسية الشاملة", 
        "المعرض المتعدد (Industry & Trade)", 
        "رفع الصور والمستندات (Sélectionner)", 
        "توليد التقارير الشاملة PDF", 
        "الأتمتة والعمليات (Automation)", 
        "التوليد الذكي (Generative AI)",
        "بوابة العملاء والمستثمرين (Client Portal)",
        "واجهة Gemini السيادية",
        "حقن Super Agentic AI (Multi-Domain)",
        "استوديو المحتوى والهوية البصرية",
        "مكتبة الخدمات الشاملة (110 خدمة)"
    ])

# 4. الصفحة الرئيسية الشاملة
if page == "الرئيسية الشاملة":
    st.title("🏭🏢 خدمات السراغنة للتجارة، الصناعة والخدمات والأعمال")
    st.markdown("### المنظومة الذكية المتكاملة لإدارة القطاعات الاقتصادية والتجارية")
    st.markdown("---")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1: st.metric("القطاع الصناعي", "مواد بناء ومعدات")
    with col_stat2: st.metric("التجارة والخدمات", "وساطة وتوزيع رقمي")
    with col_stat3: st.metric("العقار والفلاحة", "أراضي ومستثمرات")
    with col_stat4: st.metric("إدارة الأعمال", "استشارات وحلول ذكية")
    
    st.markdown("---")
    directive = st.text_area(
        "توجيه الوكيل السيادي الشامل", 
        value="أنت الوكيل السيادي لشبكة السراغنة المتكاملة (صناعة، تجارة، خدمات، أعمال، عقار وفلاحة) بقلعة السراغنة، مراكش وبني ملال. نسق العمليات باحترافية تامة.", 
        height=150
    )
    if st.button("🚀 تحديث التوجيه الشامل"):
        st.success("تم تحديث توجيه النظام المتعدد القطاعات بنجاح.")

# 5. المعرض المتعدد (Industry, Trade & Services)
elif page == "المعرض المتعدد (Industry & Trade)":
    st.header("⚙️ Sraghna Multi-Sector Gallery")
    st.markdown("معرض قطاعات: الصناعة، التجارة، الخدمات، الآليات والعقار")
    
    selected_sector_filter = st.selectbox(
        "تصفية حسب القطاع الاقتصادي:",
        ["الكل", "🏭 الصناعة ومواد البناء (مثل STE RITA FER)", "🛒 التجارة العامة والتوزيع", "💼 الخدمات والأعمال والوساطة", "🚜 الفلاحة والآليات الثقيلة", "🏡 العقار والأراضي والتجزئة", "🏛️ الهندسة الرقمية والنمذجة 3D"]
    )
    
    uploaded_files = st.file_uploader(
        "اختر صور المنتجات، المصانع، المعدات، أو العقارات (رفع متعدد):", 
        type=["jpg", "png", "webp", "jpeg"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"عدد الملفات المرفوعة للنطاق ({selected_sector_filter}): {len(uploaded_files)}")
        cols = st.columns(3)
        for i, file in enumerate(uploaded_files):
            image = Image.open(file)
            cols[i % 3].image(image, caption=f"[{selected_sector_filter}] {file.name}", use_container_width=True)
            
    st.markdown("---")
    st.link_button("💬 طلب استفسار أو صفقة تجارية عبر واتساب", "https://wa.me/212691897126?text=مرحباً، أود الاستفسار بخصوص المعرض التجاري والصناعي الشامل.")

# 6. رفع الصور والمستندات من الهاتف (Sélectionner)
elif page == "رفع الصور والمستندات (Sélectionner)":
    st.header("📱 مركز التحميل الذكي من الهاتف (Sélectionner)")
    st.markdown("ارفع صور الفواتير، السلع الصناعية، العقود، أو معدات الشغل مباشرة (يدعم صيغ HEIC والأجهزة الذكية):")
    
    selected_files = st.file_uploader(
        "Sélectionner des documents ou images", 
        type=["jpg", "jpeg", "png", "webp", "heic", "pdf"], 
        accept_multiple_files=True,
        key="global_phone_upload"
    )
    
    if selected_files:
        st.success(f"تم اختيار {len(selected_files)} ملف بنجاح سيدي الرئيس 👑")
        cols = st.columns(2)
        for index, file_item in enumerate(selected_files):
            try:
                if file_item.type.startswith("image/"):
                    cols[index % 2].image(Image.open(file_item), caption=f"ملف {index+1}: {file_item.name}", use_container_width=True)
                else:
                    cols[index % 2].success(f"تم استقبال المستند التجاري/الصناعي: {file_item.name}")
            except Exception as e:
                cols[index % 2].error(f"خطأ في معالجة الملف: {e}")
                
        st.markdown("---")
        if st.button("🚀 اعتماد الملفات في النظام الشامل"):
            st.success("تم تسجيل ومزامنة الملفات ضمن قاعدة بيانات العمليات بنجاح!")

# 7. توليد التقارير الشاملة PDF
elif page == "توليد التقارير الشاملة PDF":
    st.header("📑 DANA-Global Document Engine")
    
    GLOBAL_SERVICES_DB = {
        "🏭 الصناعة ومواد البناء": "حديد التسليح (STE RITA FER)، الخرسانة والمعدات الصناعية",
        "🛒 التجارة والتوزيع": "التجارة العامة، توريد البلعوم والمنتجات، سلاسل الإمداد",
        "💼 الخدمات والأعمال": "الوساطة التجارية، الاستشارات، إدارة المشاريع الرقمية",
        "🚜 الفلاحة والآليات": "جرارات Massey Ferguson، محاريث، تجهيزات الضخ",
        "🏡 العقار والأراضي": "بقع تجزئة (الهدى)، أراضي فلاحية والصناعية بمراكش والسراغنة",
        "🏛️ DANA Digital Designer": "النمذجة 3D، الهندسة المعمارية والديكور والتصوير الاحترافي",
        "🚗 DANA Media": "تأجير السيارات الفاخرة والنقل السياحي (مراكش وبني ملال)"
    }
    
    if st.button("⚡ توليد البروشور والتقرير التجاري الشامل PDF"):
        pdf_path = generate_official_pdf_report("RAPPORT GLOBAL DES SERVICES (Industrie, Commerce, Services)", GLOBAL_SERVICES_DB, "Rapport_Tassaout_Global.pdf")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 تحميل التقرير الشامل PDF", f, "Rapport_Tassaout_Global.pdf", "application/pdf")
        st.success(f"تم التوليد بنجاح: {pdf_path}")

# 8. الأتمتة والعمليات (Automation)
elif page == "الأتمتة والعمليات (Automation)":
    st.header("⚡ DANA-Automation Hub (Industrial & Commercial)")
    st.markdown("إدارة الأتمتة والربط بين قنوات المبيعات والشركاء التجاريين.")
    
    auto_action = st.selectbox(
        "اختر تدفق الأتمتة للتنفيذ:",
        ["مزامنة طلبات العملاء التجاريين (B2B)", "إرسال عروض الأسعار الصناعية تلقائياً", "أرشفة الفواتير والعقود العقارية", "ربط منصة n8n مع واتساب المبيعات"]
    )
    
    if st.button("▶️ تنفيذ الأتمتة الفورية"):
        st.success(f"تم تشغيل التدفق الآلي بنجاح: {auto_action} ⚡")

# 9. التوليد الذكي (Generative AI)
elif page == "التوليد الذكي (Generative AI)":
    st.header("🧠 DANA-Gen AI (Business & Marketing)")
    gen_topic = st.text_input("أدخل موضوع الإعلان أو العرض (صناعي، تجاري، عقاري، خدمي):", value="عرض توريد حديد البناء ومواد الصلب للورش الكبرى")
    if st.button("✨ توليد محتوى تسويقي احترافي"):
        st.info(f"جاري صياغة المحتوى الموجه لـ: {gen_topic} ...")
        st.success("تم التوليد بنجاح وجاهز للاستخدام الفوري في الحملات.")

# 10. بوابة العملاء والمستثمرين (Client Portal)
elif page == "بوابة العملاء والمستثمرين (Client Portal)":
    st.header("🔐 بوابة الشركاء والعملاء التجاريين والصناعيين")
    st.markdown("منصة استقبال طلبات الشركات، المستثمرين، والتجار بقلعة السراغنة وبني ملال ومراكش.")
    
    c_name = st.text_input("اسم العميل / اسم الشركة / المؤسسة:")
    c_phone = st.text_input("رقم الهاتف أو الواتساب الرسمي:")
    c_sector = st.selectbox("قطاع الطلب:", ["🏭 الصناعة ومواد البناء", "🛒 التجارة العامة", "💼 الخدمات والأعمال", "🚜 الفلاحة والآليات", "🏡 العقار والاستثمار", "🏛️ الهندسة الرقمية والنمذجة 3D"])
    c_details = st.text_area("تفاصيل الطلب أو المشروع:")
    
    if st.button("📤 إرسال الطلب المباشر للإدارة والوسيط"):
        if c_name and c_phone:
            st.success(f"تم تسجيل طلبك التجاري والصناعي بنجاح يا {c_name}!")
            st.link_button("💬 إرسال الطلب فوراً عبر واتساب", f"https://wa.me/212691897126?text=مرحباً، أنا المؤسسة/العميل {c_name}، قطاع ({c_sector})، تفاصيل الطلب: {c_details}")
        else:
            st.error("المرجو إدخال اسم العميل ورقم الهاتف للمتابعة.")

# 11. واجهة Gemini السيادية
elif page == "واجهة Gemini السيادية":
    st.header("✨ واجهة Gemini السيادية للتفاعل الشامل")
    st.markdown("المساعد الذكي المتخصص في قطاعات الصناعة، التجارة، الخدمات، والأعمال.")
    
    if "global_messages" not in st.session_state:
        st.session_state.global_messages = [
            {"role": "assistant", "content": "أهلاً بك سيدي الرئيس. النظام مهيأ بالكامل لإدارة الصناعة، التجارة، الخدمات، والأعمال. كيف نبدأ الضربات الميدانية؟"}
        ]
        
    for msg in st.session_state.global_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if user_in := st.chat_input("اكتب توجيهك الصناعي أو التجاري هنا..."):
        st.session_state.global_messages.append({"role": "user", "content": user_in})
        with st.chat_message("user"):
            st.markdown(user_in)
            
        bot_reply = f"تم استلام التوجيه الشامل: '{user_in}' وجاري التنسيق بين قطاعات الصناعة والتجارة والخدمات لتنفيذه بدقة."
        st.session_state.global_messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

# 12. حقن Super Agentic AI (Multi-Domain)
elif page == "حقن Super Agentic AI (Multi-Domain)":
    st.header("🧬 Super Multidomaine Agentic AI - مركز التوجيه الشامل")
    st.markdown("حقن التعليمات المتقدمة لإدارة شبكة الشركات والمشاريع المتعددة القطاعات:")
    
    target_dom = st.selectbox(
        "اختر النطاق الاقتصادي المستهدف:",
        ["🌐 كافة النطاقات الاقتصادية (شامل)", "🏭 النطاق الصناعي ومواد البناء", "🛒 النطاق التجاري وخدمات التوزيع", "💼 نطاق الأعمال والوساطة", "🚜 النطاق الفلاحي والآليات", "🏡 النطاق العقاري ومراكش-السراغنة", "🏛️ الهندسة الرقمية DANA Designer"]
    )
    
    sys_injection = st.text_area(
        "نص الحقن المباشر للنواة (System Prompt Core):",
        value="أنت نظام Super Agentic AI الشامل لمنظومة السراغنة (صناعة، تجارة، خدمات، أعمال، عقار، فلاحة، هندسة رقمية). نسق الموارد والصفقات تلقائياً.",
        height=160
    )
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚡ حقن وتفعيل النطاق الاقتصادي"):
            st.success(f"تم حقن التوجيه بنجاح في قطاع: {target_dom} 👑")
    with c2:
        if st.button("🔄 إعادة ضبط المصنع الافتراضي"):
            st.warning("تمت استعادة الإعدادات الأصلية للنواة.")

# 13. استوديو المحتوى والهوية البصرية
elif page == "استوديو المحتوى والهوية البصرية":
    st.header("🎨✨ استوديو المحتوى التجاري والصناعي والهوية البصرية")
    st.markdown("توليد الحملات الإعلانية الموجهة لقطاعات الصناعة، التجارة، والخدمات والأعمال.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        ad_category = st.selectbox(
            "اختر قطاع الحملة الإعلانية:",
            ["إعلان صناعي (مواد بناء / مصانع)", "إعلان تجاري عام وتوزيع", "إعلان خدمات وأعمال B2B", "عرض عقاري أو فلاحي استثماري", "تصميم هندسي وديكور 3D"]
        )
    with col_b:
        design_style = st.selectbox(
            "الهوية البصرية المعتمدة:",
            ["Royal Gold & Black (أسود وذهبي ملكي)", "Industrial Steel & Dark (فولاذي صناعي)", "Executive Corporate (أعمال رسمي فاخر)"]
        )
        
    campaign_title = st.text_input("موضوع الحملة التجارية / الصناعية:", value="حملة تسويق مواد البناء والحديد والخدمات الصناعية الكبرى")
    
    if st.button("🚀 توليد الإعلان والحملة الاحترافية"):
        st.success("تم توليد الحملة المتكاملة بنجاح سيدي الرئيس 👑")
        
        st.markdown("---")
        st.subheader("📝 المحتوى الكتابي للإعلان (جاهز للنسخ والترويج):")
        
        commercial_text = f"""
        🔥 **فرصة استثمارية وتجارية كبرى بقلعة السراغنة، بني ملال ومراكش** 🔥
        
        ضمن شبكة **TASSAOUT OMEGA OS** للخدمات الصناعية والتجارية والعقارية:
        🎯 **النشاط:** {ad_category}
        📌 **التفاصيل:** {campaign_title}
        
        نلبي احتياجات المستثمرين، المقاولين، والتجار بأعلى معايير الجودة والاحترافية.
        
        📞 **للتواصل المباشر وطلب العروض والصفقات التجارية:**
        [+212691897126](https://wa.me/212691897126?text=مرحباً، مهتم بعرض: {campaign_title})
        
        📧 البريد الإلكتروني: marocinvest2012@gmail.com
        """
        st.info(commercial_text)
        
        st.markdown("---")
        st.subheader("🎨 مواصفات التصميم والهوية البصرية:")
        st.markdown(f"""
        * **النمط البصري:** {design_style}
        * **الخطوط:** Montserrat / Helvetica-Bold
        * **الألوان:** تدرجات الذهبي الملكي والفولاذي الداكن.
        * **التوقيع الرسمي:** `Ameur signature - Sraghna Business & Industrial Network`
        """)
        
        st.link_button("💬 مشاركة الحملة عبر واتساب", f"https://wa.me/212691897126?text=مرحباً، إليك الحملة التجارية: {campaign_title}")

# 14. مكتبة الخدمات الشاملة (110 خدمة)
elif page == "مكتبة الخدمات الشاملة (110 خدمة)":
    st.header("📋 دليل الخدمات الشامل (110 خدمة معتمدة)")
    st.markdown("قائمة كاملة بجميع الخدمات المدمجة ضمن منظومة **TASSAOUT OMEGA OS**:")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏭 الصناعة (1-15)", 
        "🛒 التجارة (16-30)", 
        "💼 الأعمال (31-50)", 
        "🚜 الفلاحة (51-70)", 
        "🏡 العقار (71-85)", 
        "🏛️ الهندسة 3D (86-95)", 
        "💻 التسويق (96-110)"
    ])
    
    with tab1:
        st.markdown("""
        1. توريد حديد التسليح والصلب (STE RITA FER).
        2. توريد الخرسانة الجاهزة لمشاريع البناء.
        3. استيراد وتوريد المعدات والآليات الصناعية.
        4. توفير هياكل البناء المعدنية والمستودعات.
        5. استشارات هندسية للمنشآت الصناعية.
        6. إدارة سلاسل الإمداد والتوريد للمصانع.
        7. توزيع مواد البناء الأساسية (إسمنت، رمل، حصى).
        8. صيانة المعدات الثقيلة وخطوط الإنتاج.
        9. خدمات التخزين اللوجستي والمستودعات.
        10. توفير حلول الطاقة المستدامة للمصانع (طاقة شمسية).
        11. تقييم وفحص الجودة للمنتجات الصناعية.
        12. إدارة المخلفات الصناعية وإعادة التدوير.
        13. دراسات جدوى للمشاريع الصناعية الكبرى.
        14. الوساطة في شراء وبيع المصانع والوحدات الإنتاجية.
        15. توفير قطع الغيار الأصلية للمعدات الثقيلة.
        """)
    with tab2:
        st.markdown("""
        16. التجارة العامة واستيراد وتصدير السلع.
        17. توزيع المنتجات الغذائية والاستهلاكية بالجملة.
        18. إدارة شبكات التوزيع والتوصيل السريع (B2B و B2C).
        19. الوساطة التجارية بين الشركات والموردين.
        20. إدارة المعارض الرقمية للسلع والمنتجات.
        21. تنظيم الحملات الترويجية للمتاجر والشركات.
        22. خدمات التغليف والتعبئة الحديثة للسلع.
        23. إدارة المخزون الرقمي وأنظمة الجرد الآلي.
        24. تسويق المنتجات الحرفية والتقليدية إلكترونياً.
        25. تقديم استشارات تسعير المنتجات ودراسة السوق.
        26. توفير نقاط بيع رقمية وأنظمة كاشير ذكية.
        27. تنظيم عقود التوكيلات التجارية والحصرية.
        28. تسهيل عمليات الاستيراد والتخليص الجمركي.
        29. خدمات المبيعات الميدانية والتغطية الجغرافية.
        30. إدارة خدمة العملاء ودعم المبيعات هاتفياً ورقمياً.
        """)
    with tab3:
        st.markdown("""
        31. إعداد دراسات الجدوى الاقتصادية للمشاريع الناشئة.
        32. تأسيس الشركات والمقاولات واستخراج السجلات.
        33. الاستشارات القانونية والإدارية للأعمال.
        34. إدارة الحسابات والمسك الدفتري والمالي.
        35. صياغة العقود التجارية واتفاقيات الشراكة.
        36. إدارة الموارد البشرية والتوظيف الذكي.
        37. التخطيط الإستراتيجي لتطوير الشركات.
        38. إدارة الأزمات وحلول استمرارية الأعمال.
        39. استشارات الضرائب والتصريحات القانونية.
        40. الوساطة في عقد الشراكات الاستثمارية.
        41. إدارة المشاريع الرقمية ونظم التشغيل (ERP).
        42. أتمتة العمليات الإدارية عبر المنصات الذكية (n8n).
        43. هندسة وتصميم أنظمة الوكلاء الذكيين (Agentic AI).
        44. توليد التقارير المالية والإدارية الآلية (PDF Engine).
        45. خدمات الترجمة الرسمية والمعتمدة للوثائق.
        46. تنظيم المؤتمرات، الندوات، والاجتماعات الافتراضية.
        47. استشارات إدارة المخاطر المؤسسية.
        48. تقديم برامج تدريبية وتطويرية للموظفين.
        49. تحليل البيانات التجارية واستخراج مؤشرات الأداء.
        50. إعداد خطط العمل التنفيذية (Business Plans).
        """)
    with tab4:
        st.markdown("""
        51. بيع وتأجير جرارات Massey Ferguson والمحاريث.
        52. توريد أنظمة الري الحديث (القطر، الرش).
        53. استصلاح الأراضي الزراعية وتهيئتها.
        54. توريد الأسمدة والمبيدات الزراعية المعتمدة.
        55. توفير البذور والشتلات عالية الإنتاجية.
        56. استشارات هندسية زراعية للمزارع الكبرى.
        57. صيانة وإصلاح الآليات والمعدات الفلاحية في الميدان.
        58. حفر وتجهيز آبار السقي والمضخات الشمسية.
        59. إدارة سلاسل إنتاج وتصدير المحاصيل الفلاحية.
        60. تثمين المنتجات الفلاحية المحلية (تعاونيات).
        61. تأجير الحصادات والمعدات الموسمية.
        62. الوساطة في بيع وشراء الضيعات الفلاحية.
        63. استشارات التسميد الحديث وتحليل التربة.
        64. توفير شبكات الحماية من الصقيع والشمس للمزارع.
        65. إدارة مزارع الأشجار المثمرة (زيتون، حمضيات).
        66. توفير تجهيزات تربية المواشي والدواجن.
        67. تقديم حلول تخزين الحبوب والمحاصيل (صوامع).
        68. ترشيد استهلاك المياه في السقي الفلاحي.
        69. تنظيم المعارض الزراعية الجهوية والمحلية.
        70. إعداد دراسات جدوى للمشاريع الفلاحية والاستثمار القروي.
        """)
    with tab5:
        st.markdown("""
        71. بيع وشراء الأراضي الفلاحية والصناعية.
        72. تسويق البقع الأرضية للتجزئات السكنية والتجارية (تجزئة الهدى).
        73. الوساطة العقارية وتسهيل الصفقات بين البائع والمشتري.
        74. تقييم وتثمين العقارات والممتلكات.
        75. إدارة الأملاك العقارية وتأجيرها.
        76. استشارات هندسة وتصميم واجهات العقارات.
        77. إعداد ملفات الرخص والرسوم العقارية والتحفيظ.
        78. تسويق الشقق والمحلات التجارية والمستودعات.
        79. تقديم استشارات الاستثمار العقاري الآمن.
        80. تنظيم المعارض العقارية الرقمية.
        81. متابعة ملفات القروض العقارية وشراكات التمويل.
        82. إدارة عقود الكراء التجاري والسكني.
        83. توثيق العقارات بالصور والمسيرات الجوية (Drone).
        84. تقديم استشارات التخطيط العمراني والتقسيم.
        85. تسهيل عمليات تسجيل العقارات لدى الجهات المختصة.
        """)
    with tab6:
        st.markdown("""
        86. النمذجة الرقمية ثلاثية الأبعاد (Modélisation 3D) للقطع والآليات والمشاريع.
        87. التصميم المعماري وهندسة الديكور الداخلي والخارجي (Architecture & Déco).
        88. التصوير الفوتوغرافي الاحترافي للآليات الثقيلة، الشاحنات، وورش العمل والمصانع.
        89. التصوير الاحترافي للعقارات والأراضي لإبراز قيمتها الاستثمارية.
        90. تصميم الواجهات والمساحات بالهوية البصرية الملكية (Gold & Black).
        91. إنتاج وتصميم البانرات الإعلانية والبروشورات الرسمية.
        92. محاكاة المشاريع الهندسية والعقارية قبل إنجازها.
        93. ربط التصاميم المعمارية بأنظمة التشغيل الذكية والمنصات الرقمية.
        94. إعداد المخططات التقنية المعتمدة للشركات والمستثمرين.
        95. إدارة العروض المرئية الموجهة للعملاء عبر الوسائط الحديثة.
        """)
    with tab7:
        st.markdown("""
        96. تصميم الحملات الإعلانية الممولة (فيسبوك، إنستغرام، واتساب).
        97. توليد المحتوى الإعلاني والتسويقي بالدارجة واللغات الأخرى (Gen AI).
        98. تصميم الهوية البصرية وشعارات الشركات والمؤسسات.
        99. بناء وبرمجة تطبيقات الويب والمواقع الذكية (Streamlit).
        100. إدارة صفحات شبكات التواصل الاجتماعي للشركات.
        101. تطوير منصات الدردشة التلقائية والرد الآلي (AI Chatbots).
        102. تصميم البروشورات والكتالوجات الرسمية بصيغة PDF.
        103. تحسين ظهور النشاط التجاري في محركات البحث (SEO).
        104. تصميم البانرات الإعلانية الرقمية الثابتة والمتحركة.
        105. إدارة حملات الرسائل النصية الموجهة للعملاء (SMS & WhatsApp).
        106. إعداد استراتيجيات التسويق الرقمي المتكاملة B2C و B2B.
        107. تحليل أداء الحملات الرقمية وقياس العائد على الاستثمار.
        108. توفير روابط طلب مباشر ومؤتمنة عبر تطبيق واتساب (0 احتكاك).
        109. تقديم استشارات التحول الرقمي وإدارة الأنظمة التقنية للشركات.
        110. التنسيق الشامل للعمليات عبر منظومة **TASSAOUT OMEGA OS** الذكية.
        """)

st.markdown("---")
st.markdown("**📞 التواصل الرسمي:** +212691897126 | marocinvest2012@gmail.com")
st.caption("TASSAOUT OMEGA OS v4.1 - الصناعة، التجارة، الخدمات، الأعمال، الفلاحة والعقار (جميع الحقوق محفوظة 2026)")
