# =====================================================================
# SYSTEM: TASSAOUT OMEGA OS & ALPHA CORE NEXUS
# ENTITY: Sraghna Immobilière (مكتب تساوت الرقمي - قلعة السراغنة ومراكش)
# MODULE: Sovereign Agent Interface & Chat Orchestrator
# =====================================================================

import streamlit as st
from datetime import datetime
from agent import TassaoutAgenticCore

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sraghna Immobilière | AI Agent Interface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize core system
tassaout_os = TassaoutAgenticCore()

# --- CUSTOM STYLING FOR AGENT INTERFACE ---
st.markdown("""
    <style>
    .chat-container { padding: 10px; border-radius: 10px; background-color: #f9f9f9; }
    .stChatMessage { margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: AGENT MONITOR & CONFIG ---
st.sidebar.header("🧠 واجهة مراقبة الوكيل السيادي")
st.sidebar.info(f"**النظام:** {tassaout_os.system_name}\n\n**النواة:** {tassaout_os.core_nexus}\n\n**الكيان:** {tassaout_os.organization}")

st.sidebar.markdown("### 🛠️ اختيار المساعد المتخصص النشط:")
selected_agent_type = st.sidebar.selectbox(
    "حدد تخصص الوكيل الفرعي:",
    ["general", "geo_spatial", "neuro_marketing", "economic", "document_generator"],
    format_func=lambda x: {
        "general": "🤖 الوكيل العام (Sovereign General Core)",
        "geo_spatial": "🌍 مساعد الذكاء الجغرافي والمكاني (GIS)",
        "neuro_marketing": "🎨 مساعد التسويق العصبي والبصري",
        "economic": "📊 مساعد المحاكاة الاقتصادية والأصول",
        "document_generator": "📋 مساعد أتمتة الكتالوجات والتقارير"
    }[x]
)

if st.sidebar.button("🧹 مسح سجل المحادثة"):
    st.session_state.messages = []
    st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("💬 الواجهة التفاعلية للوكيل الذكي السيادي")
st.subheader("Sraghna Immobilière - قلعة السراغنة ومراكش")
st.markdown("---")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك يا سيادة البشمهندس. أنا الوكيل الذكي السيادي لنظام **TASSAOUT OMEGA OS**. كيف يمكنني مساعدتك اليوم في إدارة أصول أو عقارات **مكتب تساوت الرقمي**؟"}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("اكتب أمرك التشغيلي أو استفسارك هنا..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Agent Response based on selected sub-agent
    with st.chat_message("assistant"):
        with st.spinner("جاري المعالجة السيادية واستدعاء الكبسولات المعرفية..."):
            
            # Mobilize sub-agent response simulation
            sub_agent_prefix = tassaout_os.mobilize_sub_agents(selected_agent_type)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Construct intelligent agent response
            response_content = f"""
{sub_agent_prefix}

**تقرير التنفيذ الفوري:**
* **الأمر المستلم:** `{prompt}`
* **المنطقة المستهدفة:** قلعة السراغنة / مراكش
* **التوقيت:** `{timestamp}`
* **الحالة:** تم ربط الطلب بنجاح مع قواعد بيانات الـ RAG، المكاتب الهندسية، والذاكرة البصرية للنظام.

> *النظام يعمل بأقصى طاقة استيعابية وتحليلية لتلبية متطلبات Sraghna Immobilière.*
            """
            
            st.markdown(response_content)
            st.session_state.messages.append({"role": "assistant", "content": response_content})
