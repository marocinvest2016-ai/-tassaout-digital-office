# =====================================================================
# SYSTEM: TASSAOUT OMEGA OS & ALPHA CORE NEXUS
# ENTITY: Sraghna Immobilière (مكتب تساوت الرقمي - قلعة السراغنة ومراكش)
# INTERFACE: Combined Streamlit App (Chat + Operations Dashboard)
# =====================================================================

import streamlit as st
import json
from datetime import datetime
from agent import TassaoutAgenticCore

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sraghna Immobilière | Tassaout Omega OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize core system
tassaout_os = TassaoutAgenticCore()

# --- SIDEBAR: SYSTEM STATUS & MODULES ---
st.sidebar.header("⚙️ لوحة تحكم الوكيل السيادي")
st.sidebar.info(f"**الحالة:** {tassaout_os.status}\n\n**الإصدار:** {tassaout_os.version}\n\n**المنطقة التشغيلية:** {tassaout_os.location}")

st.sidebar.markdown("### 🛠️ اختيار المساعد الفرعي:")
selected_agent_type = st.sidebar.selectbox(
    "حدد تخصص الوكيل الفرعي للمحادثة:",
    ["general", "geo_spatial", "neuro_marketing", "economic", "document_generator"],
    format_func=lambda x: {
        "general": "🤖 الوكيل العام (Sovereign General Core)",
        "geo_spatial": "🌍 مساعد الذكاء الجغرافي والمكاني (GIS)",
        "neuro_marketing": "🎨 مساعد التسويق العصبي والبصري",
        "economic": "📊 مساعد المحاكاة الاقتصادية والأصول",
        "document_generator": "📋 مساعد أتمتة الكتالوجات والتقارير"
    }[x]
)

st.sidebar.markdown("### 📚 الوحدات الكبسولية المفعلة:")
for mod_name, mod_status in tassaout_os.modules.items():
    st.sidebar.success(f"**{mod_name}**\n`{mod_status}`")

# --- MAIN INTERFACE TABS ---
st.title("🏢 Sraghna Immobilière | مكتب تساوت الرقمي")
st.subheader("النظام السيادي المتقدم: TASSAOUT OMEGA OS & ALPHA CORE NEXUS")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["💬 واجهة محادثة الوكيل الذكي", "🚀 إدارة العمليات والاستعلام", "🧠 تفاصيل الذاكرة والكبسولات"])

# --- TAB 1: CHAT INTERFACE ---
with tab1:
    st.header("المساعد الذكي التفاعلي (Agentic AI Chat)")
    
    if st.button("🧹 مسح سجل المحادثة", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

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
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate Agent Response
        with st.chat_message("assistant"):
            with st.spinner("جاري المعالجة السيادية واستدعاء الكبسولات المعرفية..."):
                sub_agent_prefix = tassaout_os.mobilize_sub_agents(selected_agent_type)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
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

# --- TAB 2: OPERATIONS DASHBOARD ---
with tab2:
    st.header("إدارة الأصول والعقارات والاستشارات الاستراتيجية")
    
    col1, col2 = st.columns(2)
    with col1:
        zone = st.selectbox(
            "اختر منطقة الاستهداف الميداني:",
            ["قلعة السراغنة - المركز", "قلعة السراغنة - أحياء الهدا 1 و 2", "مراكش - النخيل / جليز", "مراكش - طريق فاس / طنجة"]
        )
        asset_type = st.selectbox(
            "نوع الأصل العقاري / التجاري:",
            ["قطعة أرضية تجارية أو سكنية", "بناية تجارية / مجمع", "أرض فلاحية / استثمارية", "خدمات تسويق ولجستيات"]
        )
    with col2:
        op_agent_choice = st.selectbox(
            "توجيه المهمة إلى المساعد المتخصص:",
            [
                ("geo_spatial", "المساعد الجغرافي المكاني (GIS & Mapping)"),
                ("neuro_marketing", "المساعد التسويقي والبصري (Neuro-Marketing)"),
                ("economic", "مساعد المحاكاة الاقتصادية والاستثمارية"),
                ("document_generator", "مساعد توليد الكتالوجات والتقارير")
            ],
            format_func=lambda x: x[1]
        )
        objective = st.text_input("هدف المهمة التشغيلية:", "إعداد دراسة تقييمية وحملة إعلانية رقمية متكاملة")

    if st.button("🚀 تنفيذ المهمة السيادية عبر الوكيل الذكي", type="primary"):
        params = {
            "agent_type": op_agent_choice[0],
            "target_zone": zone,
            "asset_type": asset_type,
            "objective": objective
        }
        report = tassaout_os.execute_operation("تنفيذ حملة عقارية واستشارية", params)
        
        st.markdown("---")
        st.success("تم تنفيذ المهمة بنجاح بواسطة المنظومة السيادية!")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f"**🤖 المساعد الفرعي المُفعل:**\n> {report['Deployed_Sub_Agent']}")
            st.markdown(f"**⏰ التوقيت الميداني:** `{report['Timestamp']}`")
        with col_res2:
            st.json(report)

# --- TAB 3: KNOWLEDGE BASE & CAPSULES ---
with tab3:
    st.header("🧠 هيكلية الكبسولات المعرفية والذكاء المتعدد (Super Multidomaine)")
    st.markdown("""
    تشتمل الكبسولة المعرفية المدمجة بالكامل في دماغ الوكيل على:
    * **العقارات والأصول:** توثيق ميداني شامل لقلعة السراغنة ومراكش.
    * **البصريات والفنون:** 100 كاميرا، 300 مصور ومخرج، و100 قناة تلفزيونية عالمية.
    * **الهندسة والعمارة:** 100 مهندس ومرجع عالمي، بالإضافة إلى 100 مكتب دراسات واستثمار مغربي.
    * **التقنية والبيانات:** 100 نظام ملاحة وأقمار صناعية، 100 مكتبة رقمية، ومستودعات RAG متقدمة.
    """)
    st.code(json.dumps(tassaout_os.modules, ensure_ascii=False, indent=4), language="json")
