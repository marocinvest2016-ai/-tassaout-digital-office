# ==============================================================================
# app.py - Streamlit Interface with Grok API Integration
# SEAU: TASSAOUT VISION VERIFIED © 2026 | BORDEAUX #800020 & GOLD #D4AF37
# ==============================================================================

import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI  # xAI تدعم توافقية OpenAI API

# إعدادات الصفحة والهوية البصرية
st.set_page_config(
    page_title="Agent Appy | Grok Powered Nexus",
    page_icon="👑",
    layout="wide"
)

# تنسيقات الألوان السيادية (Bordeaux #800020 & Gold #D4AF37)
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

st.markdown('<p class="main-header">👑 [ALPHA CORE NEXUS | GROK INTEGRATED ACTIVE]</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">خدمات تساوت بتنسيق مع ATIS [Clé en main] | المالك: Ameur Boukhaddada</p>', unsafe_allow_html=True)
st.markdown("---")

# إعداد مفتاح Grok API (يمكنك وضعه هنا مباشرة أو في متغيرات النظام)
# استبدل "YOUR_XAI_API_KEY" بمفتاحك الحقيقي من منصة xAI
XAI_API_KEY = os.getenv("XAI_API_KEY", "YOUR_XAI_API_KEY")

# كبسولة الذاكرة
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

# القائمة الجانبية للتحكم
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
    "أدخل أمرك أو تفاصيل المشروع ليقوم Grok بصياغته كتابياً:",
    placeholder="مثال: اكتب إعلان عقاري لفيلا للبيع بقلعة السراغنة..."
)

if st.button("⚡ تنفيذ وكتابة عبر Grok"):
    if user_query.strip() == "":
        st.warning("المرجو إدخال أمر أو نص صالح للتنفيذ.")
    else:
        with st.spinner("🧠 جاري إرسال الطلب إلى نموذج Grok عبر xAI API لتوليد المحتوى..."):
            try:
                # الاتصال بـ xAI API باستخدام قاعدة OpenAI Compatible
                client = OpenAI(
                    api_key=XAI_API_KEY,
                    base_url="https://api.x.ai/v1",
                )
                
                system_prompt = f"""
                أنت الوكيل الذكي السيادي لمنظومة "خدمات تساوت" بتنسيق مع شركة "ATIS".
                القطاع الحالي: {sector}
                
                تعليمات صارمة:
                1. اكتب إعلاناً أو تقريراً احترافياً ومفصلاً باللغة العربية، منظماً بالأيقونات، الكلمات المفتاحية، والهاشتاقات المناسبة بناءً على طلب المستخدم.
                2. اذكر تفاصيل التواصل الرسمية الثابتة التالية بدقة في نهاية النص:
                   - الهاتف: +212691897126
                   - البريد الإلكتروني: marocinvest2012@gmail.com
                3. أضف التوقيع الرسمي المعتمد في النهاية:
                   🌿 [TASSAOUT & ATIS VERIFIED]
                   ameur signature tassaout ai © 2026
                """

                completion = client.chat.completions.create(
                    model="grok-4.6",  # استخدام أحدث نموذج Grok متاح
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.3
                )
                
                response = completion.choices[0].message.content

            except Exception as e:
                response = f"""⚠️ تنبيه: لم يتم العثور على مفتاح API صحيح لـ xAI أو حدث خطأ في الاتصال ({e}). 
إليك الصياغة البديلة المعتمدة لطلبك:

👑 **[تقرير وكتابة الوكيل الذكي السيادي - TASSAOUT VERIFIED]**
🔹 **الموضوع:** {user_query}
🔹 **القطاع:** {sector}

📞 للتواصل المباشر: +212691897126 | marocinvest2012@gmail.com

🌿 **[TASSAOUT & ATIS VERIFIED]**  
*ameur signature tassaout ai © 2026*
"""

            # حفظ في سجل الأوامر
            memory_db["سجل_الأوامر"].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sector": sector,
                "query": user_query,
                "result": response
            })
            save_memory(memory_db)

            st.success("تم التوليد والكتابة بنجاح بواسطة Grok!")
            st.markdown("---")
            st.markdown(response)

# عرض سجل الأوامر
if st.checkbox("📁 عرض سجل الأوامر والذاكرة (Omega Memory Bank)"):
    st.json(memory_db)

st.markdown("---")
st.markdown("🌿 **[TASSAOUT & ATIS VERIFIED]** | ameur signature tassaout ai © 2026")
