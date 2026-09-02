# ==============================================================================
# app.py - Streamlit Interface for Alpha Tassaout Matrix Brain (Agent Appy)
# SEAU: TASSAOUT VISION VERIFIED © 2026 | BORDEAUX #800020 & GOLD #D4AF37
# ==============================================================================

import streamlit as st
import os
import json
from datetime import datetime

# إعدادات الصفحة والهوية البصرية
st.set_page_config(
    page_title="Agent Appy | Alpha Core Nexus",
    page_icon="👑",
    layout="wide"
)

# تنسيقات الألوان (Bordeaux #800020 & Gold #D4AF37)
st.markdown("""
    <style>
    .main-header {
        font-size: 24px;
        color: #800020;
        font-weight: bold;
        text-align: center;
    }
    .sub-header {
        font-size: 16px;
        color: #D4AF37;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">👑 [ALPHA CORE NEXUS v29.5 | AGENT APPY ACTIVE]</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">خدمات تساوت بتنسيق مع ATIS [Clé en main] | المالك: Ameur Boukhaddada</p>', unsafe_allow_html=True)
st.markdown("---")

# محاكاة كبسولة الذاكرة
MEMORY_FILE = "omega_memory_bank.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "OWNER": {"name": "Ameur Boukhaddada", "tel": "+212691897126", "email": "marocinvest2012@gmail.com"},
        "ATIS": {"ICE": "003787336000007", "tel": "+212691897126", "email": "marocinvest2012@gmail.com"},
        "سجل_الأوامر": []
    }

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

memory_db = load_memory()

# القائمة الجانبية للتحكم والقطاعات
st.sidebar.markdown("### 🏛️ محطة القيادة الذكية")
sector = st.sidebar.selectbox(
    "اختر القطاع الرئيسي للتوجيه الذكي:",
    [
        "🏭 العقار الصناعي والفلاحي والتجاري",
        "🏗️ الهندسة والبناء والتصميم",
        "🌐 التجارة الدولية وسلاسل التوريد",
        "🚜 اللوجستيات والسيارات",
        "💻 النظم الرقمية والبرمجة"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("📞 الهاتف الموحد: +212691897126\n📧 البريد: marocinvest2012@gmail.com")

# الواجهة الرئيسية للإدخال
st.markdown(f"### 🎯 القطاع المحدد: {sector}")

user_query = st.text_area(
    "أدخل أمرك أو تفاصيل المشروع (مثال: نفذ بقعة تجارية للبيع في قلعة السراغنة، أو اكتب إعلان عقاري...):",
    placeholder="اكتب الأمر هنا..."
)

if st.button("⚡ تنفيذ عبر الوكيل الذكي"):
    if user_query.strip() == "":
        st.warning("المرجو إدخال أمر أو نص صالح للتنفيذ.")
    else:
        with st.spinner("🧠 جاري معالجة الطلب عبر العقول الذكية والكبسولة..."):
            # محاكاة الاستجابة المتقدمة للوكيل الذكي بناءً على الطلب
            if "عقار" in user_query or "بيع" in user_query or "بقعة" in user_query or "شقق" in user_query:
                response = f"""⚡ [تقرير الصيد والتحليل - TASSAOUT VERIFIED]
                
🔹 **الموضوع:** {user_query}
🔹 **نتائج البحث الميداني (VOLT_HUNTER):**
* **Avito / قلعة السراغنة:** شقق وعقارات عصرية متوفرة بمساحات تتراوح بين 70م و 120م.
* **الأسعار المتوفرة:** تتراوح ما بين 40 و 64 مليون سنتيم (مع توفر الطابق الأول).
* **التوقيع التسويقي:** AMEUR SIGNATURE (#800020 | #D4AF37)

📞 **للتواصل السريع وتأكيد الاعتماد:** 
* الهاتف: `{memory_db['OWNER']['tel']}`
* البريد: `{memory_db['OWNER']['email']}`
"""
            else:
                response = f"✅ [تم التنفيذ بنجاح]: تم معالجة طلبك '{user_query}' عبر منظومة Agent Appy السيادية وتخزين الأمرين في السجل."

            # حفظ في سجل الأوامر
            memory_db["سجل_الأوامر"].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sector": sector,
                "query": user_query,
                "result": response
            })
            save_memory(memory_db)

            # عرض النتيجة
            st.success("تم إتمام العملية بنجاح!")
            st.markdown(response)

# عرض سجل الأوامر السابقة
if st.checkbox("📁 عرض سجل الأوامر والذاكرة (Omega Memory Bank)"):
    st.json(memory_db)

st.markdown("---")
st.markdown("🌿 **[TASSAOUT & ATIS VERIFIED]** | ameur signature tassaout ai © 2026")
