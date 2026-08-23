import streamlit as st
from agent import dana_whatsapp_agent, send_whatsapp_message

# ===============================
# إعدادات الواجهة الإمبراطورية
# ===============================
st.set_page_config(
    page_title="Tassaout Omega | AI Imperial System",
    page_icon="👑",
    layout="centered"
)

# تصميم بصري أنيق وخاص
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 45px;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# رأس الصفحة
st.markdown('<div class="main-title">👑 Tassaout Omega OS | النظام الإمبراطوري الشامل</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Agentic Super Multi-Domain AI Platform - سيادة رقمية عالمية</div>', unsafe_allow_html=True)
st.markdown("---")

# ===============================
# شريط اختيار الأقطاب (العيون الذكية)
# ===============================
domain_choice = st.selectbox(
    "🌐 اختر القطاع أو القطب المطلوب:",
    [
        "توجيه ذكي تلقائي (DANA CEO Router)",
        "عقارات",
        "تجارة وأعمال",
        "أسفار وحج وعمرة",
        "سيارات وآليات فلاحية",
        "الصفقات العمومية ومواد البناء",
        "الهندسة المعمارية والديكور"
    ]
)

# خريطة تحويل الأسماء للوكيل الخلفي
domain_mapping = {
    "توجيه ذكي تلقائي (DANA CEO Router)": "عام",
    "عقارات": "عقارات",
    "تجارة وأعمال": "تجارة وأعمال",
    "أسفار وحج وعمرة": "أسفار وحج وعمرة",
    "سيارات وآليات فلاحية": "سيارات وآليات فلاحية",
    "الصفقات العمومية ومواد البناء": "الصفقات العمومية ومواد البناء",
    "الهندسة المعمارية والديكور": "الهندسة المعمارية والديكور"
}

selected_domain = domain_mapping[domain_choice]

# ===============================
# مدخلات المستخدم
# ===============================
user_query = st.text_area(
    "✍️ أدخل سؤالك، مشروعك، أو طلبك هنا بالتفصيل:",
    placeholder="مثال: بغيت مهندس معماري لتصميم وحدة صناعية، أو استشارة حول صفقة عمومية، أو شقة فاخرة..."
)

whatsapp_number = st.text_input(
    "📱 رقم الهاتف للتوصل بالإجابة عبر الواتساب (اختياري):",
    placeholder="مثال: +212600000000"
)

# زر التنفيذ الإمبراطوري
if st.button("🚀 إرسال المهمة للوكيل الفائق"):
    if not user_query.strip():
        st.warning("⚠️ يرجى إدخال السؤال أو الطلب أولاً ليقوم الوكيل بتحليله.")
    else:
        with st.spinner("🔄 جاري معالجة الطلب وتوجيهه للقطب المختص عبر نظام DANA..."):
            # استدعاء الدماغ (agent.py)
            response_result = dana_whatsapp_agent(
                user_question=user_query,
                domain=selected_domain,
                to_number=whatsapp_number.strip()
            )
            
            st.success("✅ تم تنفيذ المهمة بنجاح وانضباط تام!")
            st.markdown("### 📊 تقرير النتيجة:")
            st.info(response_result)

# ===============================
# تذييل الصفحة الرسمي
# ===============================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 13px;'>"
    "APPROUVÉ PAR AMEUR © 2026 - Tassaout Vision Verified | جميع الحقوق محفوظة"
    "</p>", 
    unsafe_allow_html=True
)
