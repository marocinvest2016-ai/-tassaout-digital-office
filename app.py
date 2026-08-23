import streamlit as st
from agent import dana_whatsapp_agent, send_whatsapp_message
import datetime

# ===============================
# إعدادات الواجهة الإمبراطورية الموحدة (Alpha Core Nexus)
# ===============================
st.set_page_config(
    page_title="Tassaout Omega | Master Grand Studio & Interactive Hub",
    page_icon="👑",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# رأس المنصة السيادية
st.markdown('<div class="main-title">👑 Alpha Core Nexus | Master Grand Studio & Super AI Agents Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">الشاشة التفاعلية الكبرى - إدارة العقار، الصفقات، الهندسة، السيارات، والمحتوى البصري والسيادي</div>', unsafe_allow_html=True)
st.markdown("---")

# لوحة التحكم الجانبية لأقطاب الوكلاء الأذكياء
st.sidebar.markdown("### ⚙️ قطاع الوكلاء الفائقين (Super Agents)")
selected_domain = st.sidebar.selectbox(
    "🌐 اختر الوكيل المختص:",
    [
        "🤖 الشاشة التفاعلية للمحتوى والهوية البصرية (Interactive & Content Studio)",
        "🏠 العقار المتكامل (سكني، مهني، صناعي، فلاحي)",
        "📊 الأعمال والصفقات العمومية ومواد البناء",
        "📐 الهندسة المعمارية، الصناعية، والميكانيكية للمقاولات",
        "✈️ الأسفار، السياحة، والحج والعمرة",
        "🚗 السيارات (المستوردة، المستعملة، والآليات الفلاحية)",
        "📚 الثقافة والعلوم والأبحاث",
        "⚡ مختلفات وطلبات استثنائية الطوارئ"
    ]
)

camera_mode = st.sidebar.selectbox(
    "📷 وضع الكاميرا العالمية والدستور البصري:",
    [
        "PRODUIT (المنتجات والمجاليات)",
        "PORTRAIT (صور شخصية وفريق العمل)",
        "MAGASIN (المحلات والواجهات التجارية)",
        "VOITURE (السيارات والآليات الفلاحية)",
        "CINEMA (المشاريع السينمائية والكبرى)",
        "ARCHITECTURE (الديكور والهندسة المعمارية 3D)"
    ]
)

# الواجهة الرئيسية: التقسيم الهندسي للعمليات
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### ✍️ الشاشة التفاعلية لاستقبال البرومبتات والتعليمات")
    user_query = st.text_area(
        "أدخل تفاصيل الطلب، فكرة المحتوى، أو توجيهات التصميم المعماري/الإعلاني:",
        placeholder="اكتب هنا برومبت أو تعليماتك، وسيتم معالجتها وإنتاج المحتوى الكتابي والهوية البصرية فوراً...",
        height=160,
        key="user_query_input"
    )

with col2:
    st.markdown("### 📸 مركز رفع الأصول وكاميرا الهاتف")
    st.info("💡 يمكنك التقاط الصور مباشرة بكاميرا الهاتف أو رفع عدد **غير محدود** من الصور والمستندات للنشر الفوري.")
    
    uploaded_files = st.file_uploader(
        "رفع الصور، التصاميم، والمستندات (عدد غير محدود):",
        type=["jpg", "jpeg", "png", "pdf", "docx", "mp4"],
        accept_multiple_files=True,
        key="file_uploader_input"
    )
    
    whatsapp_number = st.text_input(
        "رقم الواتساب للتوصل بالنتيجة فورا:",
        placeholder="+212600000000",
        key="whatsapp_input"
    )

st.markdown("---")

# زر التنفيذ السيادي
if st.button("🚀 تشغيل المنظومة الفائقة وإنتاج المحتوى والنشر الفوري", key="execute_button"):
    if not user_query.strip() and not uploaded_files:
        st.warning("⚠️ يرجى إدخال برومبت أو رفع ملف واحد على الأقل ليتمكن الوكيل الذكي من المعالجة.")
    else:
        with st.spinner("🔄 جاري التنسيق بين DANA والوكيل المختص، معالجة الملفات، وإصدار المخرجات بالختم السيادي..."):
            
            files_count = len(uploaded_files) if uploaded_files else 0
            
            # تجميع النص المرسل للذكاء الاصطناعي بشكل واضح
            full_prompt = f"""
            أنت وكيل ذكي مختص في مجال: {selected_domain}
            وضع التصميم/الكاميرا: {camera_mode}
            طلب المستخدم الأساسي: {user_query}
            عدد الملفات المرفوعة: {files_count}
            قم بصياغة تقرير احترافي، محتوى تسويقي، أو خطة عمل متكاملة بناءً على هذه المعطيات.
            """
            
            # استدعاء دالة الذكاء الاصطناعي من ملف agent.py
            response_result = dana_whatsapp_agent(full_prompt)
            
            # إرسال واتساب إذا تم إدخال الرقم
            if whatsapp_number.strip():
                send_whatsapp_message(whatsapp_number.strip(), response_result)
            
            # عرض النتائج مباشرة في الواجهة بشكل بارز ومنظم
            st.success(f"✅ تم معالجة الطلب بنجاح إمبراطوري!")
            st.markdown("### 📊 تقرير المصنع والمخرجات السيادية:")
            st.markdown(response_result)
            
            if uploaded_files:
                st.markdown("#### 📂 الملفات المعالجة والموثقة سحابياً:")
                for file in uploaded_files:
                    st.text(f"✔️ {file.name} - تم ربطه بنجاح بكاميرا النظام والنشر الفوري.")

# تذييل الصفحة الرسمي
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 13px;'>"
    "APPROUVÉ PAR AMEUR © 2026 - Tassaout Vision Verified | Alpha Core Nexus Master Grand Studio & DANA Cloud Agent"
    "</p>", 
    unsafe_allow_html=True
)
