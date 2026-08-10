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
    page_title="TASSAOUT OMEGA OS - لوحة الإدارة الفورية والمدير الذكي",
    page_icon="👑",
    layout="wide"
)

# إنشاء مجلدات الحفظ الدائم
DOCS_FOLDER = "documents_officiels"
UPLOADS_FOLDER = "uploaded_assets"
os.makedirs(DOCS_FOLDER, exist_ok=True)
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# تهيئة ذاكرة الإعلانات والعروض الفورية في الجلسة
if "instant_ads" not in st.session_state:
    st.session_state.instant_ads = [
        {
            "title": "عرض خاص: توريد حديد التسليح (STE RITA FER)",
            "sector": "القطاع الصناعي",
            "details": "أسعار تنافسية وتوريد مباشر للورش الكبرى والمشاريع بقلعة السراغنة ومراكش.",
            "time": "2026-08-10 17:00"
        },
        {
            "title": "تجزئة الهدى: بقع سكنية وتجارية",
            "sector": "القطاع العقاري",
            "details": "فرصة استثمارية ممتازة لبناء مسكن العمر أو مشروع تجاري بمواقع استراتيجية.",
            "time": "2026-08-10 17:05"
        }
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "أهلاً بك سيدي الرئيس AMEUR 👑. أنا وكيل Gemini السيادي ومدير الموقع. الموقع جاهز الآن للنشر اللحظي الفوري للإعلانات والعروض من خلال هذه الواجهة مباشرة دون الحاجة لـ GitHub."}
    ]

# 2. دالة توليد PDF السيادية
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
    st.title("👑 مركز القيادة السيادي")
    st.markdown("**TASSAOUT OMEGA OS v4.1**")
    page = st.radio("التنقل بين الوحدات الحية:", [
        "لوحة المدير ونشر الإعلانات لحظياً (Admin Live Hub)",
        "واجهة Gemini السيادية التفاعلية (مع رفع الصور)",
        "لائحة العروض والخدمات الحية (الواجهة الرسمية للعملاء)",
        "المعرض المتعدد والأصول الرقمية (Gallery & Assets)",
        "المكتبة السحابية والربط العالمي (Cloud & Maps)",
        "استوديو تساوت للإنتاج الرقمي وتوليد الصور",
        "توليد التقارير الشاملة PDF"
    ])

# 4. لوحة المدير ونشر الإعلانات لحظياً (Admin Live Hub)
if page == "لوحة المدير ونشر الإعلانات لحظياً (Admin Live Hub)":
    st.header("⚡ لوحة التحكم الفورية والنشر اللحظي للإعلانات")
    st.markdown("قم بإضافة أي إعلان أو عرض جديد أدناه ليتم نشره **لحظياً** وبشكل مباشر على الموقع ليراه العملاء والزوار فورا دون أي تعديل بركودات خارجية.")
    
    with st.form("instant_ad_form"):
        ad_title = st.text_input("عنوان الإعلان أو العرض الجديد:")
        ad_sector = st.selectbox("القطاع المرتبط:", ["القطاع الصناعي (STE RITA FER)", "القطاع العقاري والاستثماري", "القطاع الفلاحي والآليات", "التجارة العامة والخدمات", "الهندسة الرقمية والديكور"])
        ad_details = st.text_area("تفاصيل العرض أو الإعلان:")
        submit_ad = st.form_submit_button("🚀 نشر الإعلان لحظياً في الموقع")
        
        if submit_ad and ad_title:
            new_ad = {
                "title": ad_title,
                "sector": ad_sector,
                "details": ad_details,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.instant_ads.insert(0, new_ad)
            st.success(f"✅ تم نشر الإعلان '{ad_title}' لحظياً بنجاح وأصبح متاحاً للعملاء في الموقع!")

    st.markdown("---")
    st.subheader("📢 الإعلانات والعروض المنشورة حالياً في واجهة الموقع:")
    if st.session_state.instant_ads:
        for idx, ad in enumerate(st.session_state.instant_ads):
            with st.container():
                st.info(f"### 🏷️ {ad['title']}\n* **القطاع:** {ad['sector']} | 🕒 **وقت النشر:** {ad['time']}\n\n{ad['details']}")
                if st.button(f"🗑️ حذف الإعلان #{idx+1}", key=f"del_ad_{idx}"):
                    st.session_state.instant_ads.pop(idx)
                    st.rerun()
    else:
        st.warning("لا توجد إعلانات منشورة حالياً.")

# 5. واجهة Gemini السيادية التفاعلية (مع رفع الصور)
elif page == "واجهة Gemini السيادية التفاعلية (مع رفع الصور)":
    st.header("✨ واجهة الوكيل الذكي Gemini (مدير الموقع السيادي)")
    st.markdown("تفاعل مباشرة مع الوكيل الذكي، ارفع الصور، الحقن بالمعلومات، واستقبل البرومبتات وتوجيهات النشر الفوري.")
    
    chat_uploaded_img = st.file_uploader("📸 رفع الصور للتحليل والحفظ الفوري (جرارات، معدات، عقارات):", type=["jpg", "png", "jpeg", "webp"], key="interactive_chat_img")
    if chat_uploaded_img:
        save_path = os.path.join(UPLOADS_FOLDER, chat_uploaded_img.name)
        with open(save_path, "wb") as f:
            f.write(chat_uploaded_img.getbuffer())
        st.image(chat_uploaded_img, caption=f"تم استلام الصورة وحفظها بنجاح: {chat_uploaded_img.name}", width=300)
        st.success("👑 تم تخزين الصورة في مستودع النظام الدائم بنجاح.")

    st.markdown("---")
    st.subheader("💬 سجل المحادثة مع المدير السيادي:")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if user_prompt := st.chat_input("اكتب توجيهك أو اطلب نشر إعلان جديد..."):
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
            
        agent_response = f"أمرك سيدي الرئيس AMEUR 👑. بصفتي مديراً للموقع، قمت بمعالجة توجيهك: '{user_prompt}'. النظام متصل بالكامل وجاهز لتنفيذ طلباتك ونشر الإعلانات لحظياً."
        st.session_state.chat_history.append({"role": "assistant", "content": agent_response})
        with st.chat_message("assistant"):
            st.markdown(agent_response)

# 6. لائحة العروض والخدمات الحية (الواجهة الرسمية للعملاء)
elif page == "لائحة العروض والخدمات الحية (الواجهة الرسمية للعملاء)":
    st.header("📋 لائحة العروض والإعلانات الحية للعملاء والزوار")
    st.markdown("هنا يطالع العملاء أحدث العروض والخدمات المنشورة **لحظياً** من طرف إدارة المنظومة:")
    
    # عرض الإعلانات الحية المنشورة من لوحة المدير
    st.subheader("🔥 العروض والإعلانات الحية الجديدة:")
    if st.session_state.instant_ads:
        for ad in st.session_state.instant_ads:
            st.success(f"**{ad['title']}** ({ad['sector']})\n\n{ad['details']}\n\n[💬 اطلب هذا العرض عبر واتساب](https://wa.me/212691897126?text=مرحباً، أهتم بعرض: {ad['title']})")
    else:
        st.info("لا توجد إعلانات حية جديدة في الوقت الحالي.")

    st.markdown("---")
    st.subheader("🌟 باقة الخدمات الأساسية (110 خدمة معتمدة):")
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.markdown("""
        * **🏭 القطاع الصناعي:** توريد حديد التسليح (STE RITA FER)، الخرسانة الجاهزة والمعدات الصناعية.
        * **🚜 القطاع الفلاحي:** جرارات Massey Ferguson، أنظمة الري، واستصلاح الأراضي.
        * **🏡 القطاع العقاري:** بقع تجزئة الهدى، الأراضي الاستثمارية بمراكش والسراغنة.
        """)
    with col_o2:
        st.markdown("""
        * **🏛️ الهندسة والنمذجة 3D:** تصاميم معمارية وديكورات فاخرة.
        * **🚗 النقل والخدمات:** تأجير السيارات الفاخرة DANA Media.
        * **💻 الوساطة والتسويق الرقمي:** إعلانات موجهة وحملات احترافية.
        """)
    st.link_button("💬 تواصل مباشر مع الإدارة والوسيط", "https://wa.me/212691897126?text=مرحباً، أود الاستفسار حول العروض والخدمات المتاحة في الموقع.")

# 7. المعرض المتعدد والأصول الرقمية (Gallery & Assets)
elif page == "المعرض المتعدد والأصول الرقمية (Gallery & Assets)":
    st.header("⚙️ Sraghna Multi-Sector Gallery & Assets")
    st.markdown("استعراض الصور والمعدات والعقارات المخزنة في النظام:")
    
    uploaded_files = st.file_uploader("اختر صور إضافية لرفعها مباشرة:", type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            save_path = os.path.join(UPLOADS_FOLDER, file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"تم حفظ {len(uploaded_files)} صورة بنجاح.")

    saved_images = os.listdir(UPLOADS_FOLDER)
    if saved_images:
        cols = st.columns(3)
        for i, img_name in enumerate(saved_images):
            img_path = os.path.join(UPLOADS_FOLDER, img_name)
            if img_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                cols[i % 3].image(img_path, caption=img_name, use_container_width=True)
    else:
        st.info("لا توجد صور مخزنة حالياً.")

# 8. المكتبة السحابية والربط العالمي (Cloud & Maps)
elif page == "المكتبة السحابية والربط العالمي (Cloud & Maps)":
    st.header("☁️🌐 المكتبة الرقمية السحابية الجامعة & ربط الخرائط")
    st.markdown("الأرشيف السحابي المركزي، الإحداثيات الجغرافية، والكاميرا العالمية.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.success("### 📂 المستندات والسحابة الرسمية")
        st.link_button("📂 فتح مستندات السحابة المركزية", "https://docs.google.com/document/d/1Lofby7y_eb9rn4W0EZM-KWDwSEmHR867xDyNZZJFnE8/edit?usp=drive_web")
    with col_c2:
        st.warning("### 📍 المواقع الجغرافية")
        st.link_button("📍 عرض المواقع على Google Maps", "https://maps.google.com/?q=El+Kelaa+des+Sraghna+Marrakech")

# 9. استوديو تساوت للإنتاج الرقمي وتوليد الصور
elif page == "استوديو تساوت للإنتاج الرقمي وتوليد الصور":
    st.header("🎨✨ استوديو تساوت للإنتاج الرقمي وتوليد البرومبتات")
    img_category = st.selectbox("نوع التصميم المطلوب:", ["تصميم إعلاني صناعي (STE RITA FER)", "تصميم جرارات وآليات فلاحية", "تصميم عقاري وتجزئة الهدى", "تصميم هندسي 3D وديكور"])
    prompt_text = st.text_area("تفاصيل البرومبت المطلوب:", value="صورة إعلانية فاخرة بالهوية الملكية (أسود وذهبي)، جودة سينمائية 4K.")
    if st.button("🚀 توليد وتجهيز البرومبت الفوري"):
        st.success(f"تم اعتماد وتوليد البرومبت بنجاح لقطاع: {img_category} 👑")
        st.info(f"📌 **النتيجة:** {prompt_text}")

# 10. توليد التقارير الشاملة PDF
elif page == "توليد التقارير الشاملة PDF":
    st.header("📑 DANA-Global Document Engine")
    GLOBAL_SERVICES_DB = {
        "🏭 الصناعة ومواد البناء": "حديد التسليح (STE RITA FER)، الخرسانة والمعدات",
        "🛒 التجارة والتوزيع": "التجارة العامة وتوريد السلع",
        "💼 الخدمات والأعمال": "الوساطة التجارية والاستشارات",
        "🚜 الفلاحة والآليات": "جرارات Massey Ferguson والمحاريث",
        "🏡 العقار والأراضي": "بقع تجزئة الهدى والأراضي الاستثمارية",
        "🏛️ DANA Digital Designer": "النمذجة 3D والتصوير الاحترافي"
    }
    if st.button("⚡ توليد البروشور والتقرير التجاري الشامل PDF"):
        pdf_path = generate_official_pdf_report("RAPPORT GLOBAL DES SERVICES", GLOBAL_SERVICES_DB, "Rapport_Tassaout_Global.pdf")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 تحميل التقرير الشامل PDF", f, "Rapport_Tassaout_Global.pdf", "application/pdf")
        st.success(f"تم التوليد بنجاح: {pdf_path}")

st.markdown("---")
st.markdown("**📞 التواصل الرسمي:** +212691897126 | marocinvest2012@gmail.com")
st.caption("TASSAOUT OMEGA OS v4.1 - إدارة فورية ونشر لحظي للإعلانات (جميع الحقوق محفوظة 2026)")
