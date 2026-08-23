import streamlit as st
from agent import dana_whatsapp_agent, send_whatsapp_message
import datetime
import urllib.parse
from io import BytesIO

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
    .whatsapp-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #25D366;
        color: white !important;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        width: 100%;
        margin-top: 10px;
        text-align: center;
        font-size: 16px;
    }
    .whatsapp-btn:hover {
        background-color: #22BF5B;
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
st.markdown('<div class="main-title">👑 Alpha Core Nexus | مكتب تساوت الرقمي العقار والأعمال</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">الشاشة التفاعلية الكبرى - الإعلانات والصفقات التجارية بذكاء مستقل دون تشويش هندسي</div>', unsafe_allow_html=True)
st.markdown("---")

# 🧠 تهيئة الذاكرة المؤقتة لمنع ضياع الاختيارات
if "active_domain" not in st.session_state:
    st.session_state.active_domain = "🏠 العقار المتكامل (بيع، كراء، تسويق، بقع، إعلانات)"

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

if "saved_files" not in st.session_state:
    st.session_state.saved_files = []

# اختيار الوكيل المختص ووضع الكاميرا
st.markdown("### ⚙️ تحديد القطاع النشط ووضع الكاميرا المناسب")
col_agent1, col_agent2 = st.columns(2)

with col_agent1:
    selected_domain = st.selectbox(
        "🌐 اختر الوكيل المختص / طبيعة المهمة:",
        [
            "🏠 العقار المتكامل (بيع، كراء، تسويق، بقع، إعلانات)",
            "📊 الأعمال والصفقات العمومية ومواد البناء",
            "🚗 السيارات (المستوردة، المستعملة، والآليات الفلاحية)",
            "🤖 الشاشة التفاعلية للمحتوى والهوية البصرية",
            "✈️ الأسفار، السياحة، والحج والعمرة",
            "📚 الثقافة والعلوم والأبحاث",
            "📐 الهندسة المعمارية والديكور الداخلي (عند الطلب الهندسي فقط)",
            "⚡ مختلفات وطلبات استثنائية الطوارئ"
        ],
        key="main_agent_select"
    )
    st.session_state.active_domain = selected_domain

with col_agent2:
    camera_mode = st.selectbox(
        "📷 وضع الكاميرا والدستور البصري الإعلاني:",
        [
            "PRODUIT & ANNONCE (إعلانات المنتجات، العقارات، والسيارات العادية)",
            "MAGASIN & SHOWROOM (المحلات التجارية والواجهات)",
            "PORTRAIT (صور شخصية وفريق العمل المهني)",
            "CINEMA & DRONE (تصوير جوي سينمائي للمشاريع الكبرى)",
            "ARCHITECTURE & 3D (هندسة المعمار وتصميم الديكور - عند الطلب الهندسي)"
        ],
        key="main_camera_select"
    )

st.markdown(f'<div class="active-agent-box">⚡ القطاع قيد التشغيل: {st.session_state.active_domain}</div>', unsafe_allow_html=True)
st.markdown("---")

# الواجهة الرئيسية
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### ✍️ الشاشة التفاعلية لاستقبال الإعلانات والطلبات")
    user_query = st.text_area(
        "أدخل تفاصيل الإعلان، الصفقة، أو الطلب المراد تنفيذه:",
        placeholder="مثال: اكتب إعلان تسويقي لبيع شقة بقلعة السراغنة بثمن تنافسي مع رقم الاتصال...",
        height=160,
        key="user_query_input"
    )

with col2:
    st.markdown("### 📸 مركز رفع الأصول والصور الإعلانية")
    st.info("💡 ارفع صور العقار، السيارة، أو المنتج لتوليد الإعلان والمحتوى التسويقي فورا.")
    
    uploaded_files = st.file_uploader(
        "رفع الصور والمستندات:",
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
if st.button("🚀 تشغيل المنظومة وتوليد المحتوى الفوري", key="execute_button"):
    if not user_query.strip() and not uploaded_files:
        st.warning("⚠️ يرجى إدخال تفاصيل الإعلان أو رفع ملف واحد على الأقل ليتمكن الوكيل من التنفيذ.")
    else:
        with st.spinner(f"🔄 جاري معالجة الطلب عبر وكيل [{st.session_state.active_domain}]..."):
            
            files_count = len(uploaded_files) if uploaded_files else 0
            current_domain = st.session_state.active_domain
            
            # 🧠 توجيه ذكي دقيق: لا يوجد تدخل هندسي نهائياً إلا إذا تم اختيار قطاع الهندسة صراحة
            if "الهندسة المعمارية والديكور الداخلي" in current_domain:
                expert_persona = "أنت لجنة هندسية عليا وخبراء في المعمار والديكور الداخلي. مطلوب تقديم دراسة هندسية، مقترحات تصميم، وبرومبت بصري دقيق."
            elif "العقار المتكامل" in current_domain:
                expert_persona = "أنت خبير تسويق عقاري احترافي بجهة مراكش آسفي (قلعة السراغنة، مراكش). تخصصك صياغة إعلانات عقارية تجارية جذابة وواضحة للزبناء دون أي تشويش هندسي."
            elif "السيارات" in current_domain:
                expert_persona = "أنت خبير تسويق سيارات، آليات فلاحية، ومركبات نفعية. صغ إعلانات تجارية جذابة وسريعة."
            elif "الأعمال والصفقات العمومية" in current_domain:
                expert_persona = "أنت مستشار أعمال وخبير في تدبير الصفقات العمومية وتوريدات المواد."
            else:
                expert_persona = f"أنت وكيل ذكي محترف في قطاع: {current_domain}."

            full_prompt = f"""
            [تعليمات النظام]:
            {expert_persona}
            
            [دستور وضع الكاميرا]: {camera_mode}
            
            [طلب المستخدم]:
            {user_query}
            
            [عدد الملفات المرفقة]: {files_count}
            
            [المطلوب]: تقديم مخرجات احترافية نظيفة، مباشرة، وتخدم الهدف الإعلاني أو التجاري المطلوب بدقة متناهية دون حشو أو خروج عن السياق.
            """
            
            # استدعاء الذكاء الاصطناعي المنطقي وتخزين النسخ في الجلسة
            response_result = dana_whatsapp_agent(full_prompt)
            st.session_state.last_result = response_result
            st.session_state.saved_files = uploaded_files if uploaded_files else []
            
            # إرسال واتساب إذا وُجد الرقم تلقائياً عبر الدالة البرمجية
            if whatsapp_number.strip():
                send_whatsapp_message(whatsapp_number.strip(), response_result)

# 📊 عرض النتائج الثابتة في الجلسة مع أيقونة واتساب تفاعلية ومعاينة الصور الصحيحة
if st.session_state.last_result:
    st.success(f"✅ تم إنجاز الطلب الإعلاني/التجاري بنجاح!")
    st.markdown("### 📊 تقرير المخرجات والنتيجة النهائية:")
    st.markdown(st.session_state.last_result)
    
    # 🟢 زر واتساب تفاعلي يتيح إرسال النتيجة بضغطة زر مباشرة
    encoded_text = urllib.parse.quote(st.session_state.last_result)
    wa_link = f"https://api.whatsapp.com/send?text={encoded_text}"
    st.markdown(f'<a href="{wa_link}" target="_blank" class="whatsapp-btn">💬 إرسال ومشاركة المخرجات عبر واتساب فوراً</a>', unsafe_allow_html=True)
    
    if st.session_state.saved_files:
        st.markdown("#### 📂 الملفات والأصول المرتبطة:")
        for file in st.session_state.saved_files:
            st.text(f"✔️ {file.name} - تم ربطه بنجاح.")
            # استخدام BytesIO لضمان ظهور الصور وثباتها وعدم اختفائها
            if file.type.startswith("image/"):
                try:
                    bytes_data = file.getvalue()
                    st.image(BytesIO(bytes_data), caption=f"معاينة: {file.name}", use_column_width=True)
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
