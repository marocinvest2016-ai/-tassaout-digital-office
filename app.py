import streamlit as st
from agent import dana_whatsapp_agent, send_whatsapp_message
import datetime

# ===============================
# إعدادات الواجهة الإمبراطورية الموحدة (Alpha Core Nexus)
# ===============================
st.set_page_config(
    page_title="مكتب تساوت الرقمي | العقار والأعمال والذكاء الاصطناعي",
    page_icon="👑",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 13px;
        color: #4B5563;
        margin-bottom: 15px;
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
    .active-agent-box {
        background-color: #EFF6FF;
        border: 2px solid #3B82F6;
        padding: 10px 15px;
        border-radius: 8px;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# رأس المنصة السيادية
st.markdown('<div class="main-title">👑 Alpha Core Nexus | مكتب تساوت الرقمي العقار والأعمال</div>', unsafe_allow_html=TaskView if 'TaskView' in globals() else True)
st.markdown('<div class="subtitle">الشاشة التفاعلية الكبرى - تفعيل هندسة الديكور، المعماريين، والبرومبتات البصرية بالذكاء الاصطناعي المنطقي</div>', unsafe_allow_html=True)
st.markdown("---")

# 🧠 تهيئة الذاكرة المؤقتة لمنع ضياع الاختيارات
if "active_domain" not in st.session_state:
    st.session_state.active_domain = "🏠 العقار المتكامل (سكني، مهني، صناعي، فلاحي)"

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

if "saved_files" not in st.session_state:
    st.session_state.saved_files = []

# اختيار الوكيل المختص ووضع الكاميرا والمهندسين
st.markdown("### ⚙️ تفعيل القطاع، الطاقم الهندسي، والدستور البصري")
col_agent1, col_agent2 = st.columns(2)

with col_agent1:
    selected_domain = st.selectbox(
        "🌐 اختر الوكيل المختص:",
        [
            "🏠 العقار المتكامل (سكني، مهني، صناعي، فلاحي)",
            "📐 الهندسة المعمارية، الصناعية، والديكور الداخلي",
            "🤖 الشاشة التفاعلية للمحتوى والهوية البصرية (Interactive & Content Studio)",
            "📊 الأعمال والصفقات العمومية ومواد البناء",
            "✈️ الأسفار، السياحة، والحج والعمرة",
            "🚗 السيارات (المستوردة، المستعملة، والآليات الفلاحية)",
            "📚 الثقافة والعلوم والأبحاث",
            "⚡ مختلفات وطلبات استثنائية الطوارئ"
        ],
        key="main_agent_select"
    )
    st.session_state.active_domain = selected_domain

with col_agent2:
    camera_mode = st.selectbox(
        "📷 وضع الكاميرا والدستور البصري المعماري:",
        [
            "ARCHITECTURE & 3D INTERIOR (هندسة المعمار وتصميم الديكور الداخلي 3D)",
            "PRODUIT (المنتجات والعقارات المعروضة)",
            "MAGASIN & SHOWROOM (المحلات التجارية والواجهات)",
            "PORTRAIT (صور الفريق الهندسي والمهني)",
            "VOITURE (السيارات والآليات الفلاحية)",
            "CINEMA & REAL ESTATE DRONE (تصوير جوي سينمائي للمشاريع الكبرى)"
        ],
        key="main_camera_select"
    )

st.markdown(f'<div class="active-agent-box">⚡ الوكيل المفعل حالياً: {st.session_state.active_domain} | الطاقم الهندسي والبصري في وضع الاستعداد التام</div>', unsafe_allow_html=True)
st.markdown("---")

# الواجهة الرئيسية
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### ✍️ الشاشة التفاعلية لاستقبال البرومبتات الهندسية والبصرية")
    user_query = st.text_area(
        "أدخل تفاصيل التصميم، فكرة الديكور، المخطط المعماري، أو الطلب البصري:",
        placeholder="مثال: صمم لي صالون مغربي مودرن مع إضاءة خفية، أو برومبت لتصميم واجهة فيلا فخمة بقلعة السراغنة...",
        height=160,
        key="user_query_input"
    )

with col2:
    st.markdown("### 📸 مركز رفع المخططات والأصول البصرية")
    st.info("💡 ارفع المخططات الهندسية، صور الفراغات، أو الواجهات لمعالجتها وتوجيه المهندسين لإنتاج الإنستنت والتصميم.")
    
    uploaded_files = st.file_uploader(
        "رفع الصور، المخططات، والمستندات:",
        type=["jpg", "jpeg", "png", "pdf", "docx", "mp4"],
        accept_multiple_files=True,
        key="file_uploader_input"
    )
    
    whatsapp_number = st.text_input(
        "رقم الواتساب للتوصل بالتقرير الهندسي فورا:",
        placeholder="+212600000000",
        key="whatsapp_input"
    )

st.markdown("---")

# زر التنفيذ السيادي
if st.button("🚀 تشغيل الطاقم الهندسي وتوليد البرومبت والتصميم البصري", key="execute_button"):
    if not user_query.strip() and not uploaded_files:
        st.warning("⚠️ يرجى إدخال البرومبت أو رفع مخطط هندسي لكي يباشر المهندسون المعماريون والديكور العمل.")
    else:
        with st.spinner(f"🔄 جاري استدعاء المهندسين المعماريين وخبراء الديكور وتفعيل وضع الكاميرا [{camera_mode}]..."):
            
            files_count = len(uploaded_files) if uploaded_files else 0
            
            # 🧠 محرك تفعيل المهندسين المعماريين والديكور والبرومبت البصري
            current_domain = st.session_state.active_domain
            
            if "الهندسة المعمارية، الصناعية، والديكور" in current_domain or "العقار المتكامل" in current_domain:
                expert_persona = """
                أنت لجنة هندسية عليا تضم:
                1. مهندساً معمارياً أول (Senior Architect).
                2. خبيراً في التصميم الداخلي والديكور (Interior Designer & 3D Visualizer).
                3. مهندساً مدنياً مختصاً في دفاتر التحملات وتقييم التكاليف بجهة مراكش آسفي.
                """
            else:
                expert_persona = f"أنت وكيل ذكي خبير ومستشار محترف في قطاع: {current_domain}."

            full_prompt = f"""
            [تعليمات النظام السيادي واللجنة الهندسية]:
            {expert_persona}
            
            [دستور الكاميرا والبرومبت البصري المطلوب]:
            تم تفعيل وضع التصوير والمعالجة البصرية التالي: {camera_mode}
            قم بصياغة (Prompt مرئي دقيق ومحترف باللغات الثلاث أو الإنجليزية المخصصة لبرامج التوليد المرئي) وتوجيهات هندسية تتماشى تماماً مع هذا البرومبت البصري.
            
            [مدخلات المستخدم والطلب الفعلي]:
            {user_query}
            
            [عدد الملفات والأصول المرفقة]: {files_count}
            
            [المخرجات المطلوبة]:
            1. التحليل الهندسي والمقترحات الإبداعية المفصلة بناءً على نوع الكاميرا والطلب.
            2. برومبت بصري هندسي جاهز للاستخدام في برامج التوليد (Midjourney/Stable Diffusion/DALL-E).
            3. خطة عمل تنفيذية واضحة (عقارية، هندسية، أو تسويقية).
            """
            
            # استدعاء الذكاء الاصطناعي المنطقي
            response_result = dana_whatsapp_agent(full_prompt)
            st.session_state.last_result = response_result
            st.session_state.saved_files = uploaded_files if uploaded_files else []
            
            # إرسال واتساب إذا وُجد الرقم
            if whatsapp_number.strip():
                send_whatsapp_message(whatsapp_number.strip(), response_result)

# 📊 عرض النتائج الثابتة في الجلسة
if st.session_state.last_result:
    st.success(f"✅ تم إنجاز التقرير الهندسي والبصري بنجاح بواسطة الطاقم المختص!")
    st.markdown("### 📊 مخرجات الطاقم الهندسي والبرومبت البصري:")
    st.markdown(st.session_state.last_result)
    
    if st.session_state.saved_files:
        st.markdown("#### 📂 المخططات والأصول المرفقة والمعالجة:")
        for file in st.session_state.saved_files:
            st.text(f"✔️ {file.name} - تم ربطه بالدراسة الهندسية.")
            if file.type.startswith("image/"):
                try:
                    st.image(file, caption=f"معاينة المخطط/الأصل: {file.name}", use_column_width=True)
                except Exception as img_err:
                    st.warning(f"تعذر عرض الصورة {file.name}: {img_err}")

# تذييل الموقع الرسمي المعتمد
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #1E3A8A; font-weight: bold; font-size: 14px; margin-top: 20px; padding: 15px; border-top: 2px solid #E5E7EB; background-color: #F9FAFB; border-radius: 8px;">
    مكتب تساوت الرقمي العقار والاعمال مدعوم بالذكاء الاصطناعي المنطقي<br>
    <span style="color: #4B5563; font-size: 12px; font-weight: normal;">
        انتاج السيد عامر بوخدادة قلعة السراغنة مراكش | كل الحقوق محفوظة © 2026
    </span>
</div>
""", unsafe_allow_html=True)
