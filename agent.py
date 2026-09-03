import streamlit as st
from agent import OmegaAgent
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Omega Agentic v3.0 | Tassaout & Atis",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم الواجهة المخصصة (CSS)
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #FF2222;
    }
    .whatsapp-btn {
        display: inline-block;
        background-color: #25D366;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    .whatsapp-btn:hover {
        background-color: #1EBE5D;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. شريط التنقل الجانبي (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.title("OMEGA AGENTIC v3.0")
    st.markdown("---")
    
    # اختيار المجال
    domaine = st.selectbox(
        "🎯 اختر مجال العمل:",
        ["العقار (Real Estate)", "التسويق الرقمي", "السيارات والنقل", "الخدمات الرقمية"]
    )
    
    st.markdown("---")
    st.markdown("### 🛠️ حالة النظام")
    
    meta_check = "✅ مفعل" if st.secrets.get("META_API_KEY") else "❌ مفقود"
    supabase_check = "✅ مفعل" if st.secrets.get("SUPABASE_URL") else "❌ مفقود"
    whatsapp_check = "✅ مفعل" if st.secrets.get("WHATSAPP_BUSINESS_NUMBER") else "⚠️ اختيارى"
    
    st.text(f"Meta AI: {meta_check}")
    st.text(f"Supabase: {supabase_check}")
    st.text(f"WhatsApp: {whatsapp_check}")
    
    st.markdown("---")
    st.info("💡 مدعوم بالكامل عبر نماذج Meta الذكية لتقديم أداء احترافي فائق السرعة.")

# 4. الواجهة الرئيسية
st.title("👑 Omega Agentic Hub - مدعوم بـ Meta AI")
st.markdown("### نظام الوكلاء الأذكياء لإدارة وتطوير الحملات والمشاريع تلقائياً")

task_input = st.text_area(
    "✍️ أخلِق مهمتك أو تفاصيل مشروعك هنا (مثلاً: تسويق بقع سكنية في قلعة السراغنة):",
    placeholder="اكتب تفاصيل العقار، الخدمة، أو الهدف التسويقي...",
    height=120
)

if st.button("🚀 ابدأ تنفيذ العمليات بالوكلاء الأذكياء"):
    if not task_input.strip():
        st.warning("⚠️ يرجى إدخال تفاصيل المهمة أو المشروع أولاً.")
    else:
        agent = OmegaAgent(domaine=domaine)
        
        with st.spinner("⏳ جارٍ العمل عبر شبكة وكلاء Meta الذكية..."):
            
            # الخطوة 1: المدير التنفيذي (CEO)
            st.markdown("---")
            st.subheader("1️⃣ خطة المدير التنفيذي (Meta CEO)")
            ceo_result = agent.ceo(task_input)
            st.markdown(ceo_result)
            
            # الخطوة 2: المدير التقني واستهداف الإعلانات (CTO)
            st.markdown("---")
            st.subheader("2️⃣ الاستراتيجية التقنية واستهداف الجمهور (Meta CTO)")
            cto_result = agent.cto(task_input)
            st.markdown(cto_result)
            
            # الخطوة 3: مدير العمليات والميزانية (COO)
            st.markdown("---")
            st.subheader("3️⃣ خطة العمليات والجدول الزمني (Meta COO)")
            coo_result = agent.coo(task_input)
            st.markdown(coo_result)
            
            # الخطوة 4: صانع المحتوى والإعلانات (Copywriter)
            combined_plan = f"CEO Plan: {ceo_result}\nCTO Strategy: {cto_result}\nCOO Operations: {coo_result}"
            st.markdown("---")
            st.subheader("4️⃣ النصوص الإعلانية الجاهزة (Meta Copywriter)")
            copy_result = agent.copywriter(combined_plan)
            st.markdown(copy_result)
            
            # الخطوة 5: خبير الإغلاق وزيادة المبيعات (FOMO)
            st.markdown("---")
            st.subheader("5️⃣ صيغة الإغلاق وتحفيز العملاء - FOMO (Meta Closer)")
            closer_result = agent.closer(copy_result)
            st.success(closer_result)
            
            # إضافة زر تفاعلي مباشر لرابط الواتساب مع النص الإعلاني الجاهز
            whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
            if whatsapp_num:
                encoded_msg = urllib.parse.quote(f"مرحباً، مهتم بهذا العرض:\n\n{closer_result}")
                wa_link = f"https://wa.me/{whatsapp_num}?text={encoded_msg}"
                st.markdown(f'''
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="{wa_link}" target="_blank" class="whatsapp-btn">
                            💬 إرسال العرض أو مشاركته عبر واتساب مباشرة
                        </a>
                    </div>
                ''', unsafe_allow_html=True)
            
            st.balloons()
            st.success("✅ تمت العملية بنجاح وتم إرسال الإشعارات المطلوبة.")
