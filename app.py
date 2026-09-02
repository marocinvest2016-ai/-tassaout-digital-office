# ==============================================================================
# app.py - Streamlit Interface with VOLT_HUNTER OMEGA + Grok API
# SEAU: TASSAOUT VISION VERIFIED © 2026 | BORDEAUX #800020 & GOLD #D4AF37
# ==============================================================================

import streamlit as st
import os
import json
import requests
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="Agent Appy | OMEGA HUNTER", page_icon="👑", layout="wide")

st.markdown("""
    <style>
   .main-header {font-size: 24px;color: #800020;font-weight: bold;text-align: center;}
   .sub-header {font-size: 16px;color: #D4AF37;text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">👑 [ALPHA CORE NEXUS | OMEGA HUNTER + GROK ACTIVE]</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">خدمات تساوت بتنسيق مع ATIS [Clé en main] | المالك: Ameur Boukhaddada</p>', unsafe_allow_html=True)
st.markdown("---")

# قراءة المفتاح من Streamlit Secrets
XAI_API_KEY = st.secrets.get("XAI_API_KEY")

# كبسولة الذاكرة
MEMORY_FILE = "omega_memory_bank.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {
        "OWNER": {"name": "Ameur Boukhaddada", "tel": "+212691897126", "email": "marocinvest2012@gmail.com"},
        "ATIS": {"ICE": "003787336000007", "tel": "+212691897126", "email": "marocinvest2012@gmail.com"},
        "سجل_الأوامر": []
    }
def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
memory_db = load_memory()

# ================== VOLT_HUNTER OMEGA ==================
def volt_hunter_omega(query):
    """يصيد من كل الانترنيت: مواقع عقار + جوجل + سوشيال"""
    results = []
    city = "قلعة السراغنة"
    query_clean = query.replace(' ', '-')

    # 1. مواقع العقار المغربية الكبار
    sites_to_check = {
        "Avito": f"https://www.avito.ma/ar/{city}/{query_clean}",
        "Mubawab": f"https://www.mubawab.ma/ar/l/{query_clean}/{city.replace(' ', '-')}",
        "Sarayat": f"https://www.sarayat.com/ar/عقار-للبيع/{city}"
    }

    for name, url in sites_to_check.items():
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            if r.status_code == 200:
                results.append(f"✅ {name}: تم العثور على عروض | {url}")
        except:
            results.append(f"⚠️ {name}: تعذر الاتصال")

    # 2. بحث عام عبر DuckDuckGo للسوشيال والمواقع العالمية
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={query}+{city}+عقار+للبيع&format=json"
        ddg = requests.get(ddg_url, timeout=10).json()
        for topic in ddg.get("RelatedTopics", [])[:3]:
            if "Text" in topic:
                results.append(f"🌐 {topic['Text']}")
    except: pass

    return "\n".join(results) if results else "لم يتم العثور على نتائج حية"
# =========================================================

# القائمة الجانبية
st.sidebar.markdown("### 🏛️ محطة القيادة الذكية")
sector = st.sidebar.selectbox("اختر القطاع:", ["🏭 العقار الصناعي والفلاحي والتجاري", "🏗️ الهندسة والبناء", "🌐 التجارة الدولية"])
omega_toggle = st.sidebar.checkbox("⚡ تفعيل VOLT_HUNTER OMEGA", value=True)
st.sidebar.markdown("---")
st.sidebar.info("📞 الهاتف: +212691897126\n📧 marocinvest2012@gmail.com")

# الواجهة
st.markdown(f"### 🎯 القطاع المحدد: {sector}")
user_query = st.text_area("أدخل أمرك:", placeholder="مثال: اراضي فلاحية وفيرمات جاهزة للبيع بقلعة السراغنة")

if st.button("⚡ تنفيذ وكتابة عبر OMEGA HUNTER + Grok"):
    if user_query.strip() == "":
        st.warning("المرجو إدخال أمر صالح.")
    else:
        with st.spinner("🧠 جاري الصيد من كل الويب + توليد المحتوى عبر Grok..."):

            hunted_data = ""
            if omega_toggle:
                with st.status("⚡ VOLT_HUNTER OMEGA يصيد من Avito + Mubawab + Sarayat + الويب..."):
                    hunted_data = volt_hunter_omega(user_query)
                    st.write(hunted_data)

            try:
                client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
                system_prompt = f"""
                أنت الوكيل الذكي السيادي لمنظومة "خدمات تساوت" بتنسيق مع "ATIS".
                القطاع: {sector}

                بيانات السوق الحية التي تم صيدها من OMEGA HUNTER:
                {hunted_data}

                تعليمات:
                1. اكتب تقرير/إعلان احترافي بالعربية بالأيقونات والهاشتاقات.
                2. استند على بيانات السوق اللي صيدناها. اذكر 3 نقاط قوة.
                3. اذكر التواصل: الهاتف: +212691897126 | البريد: marocinvest2012@gmail.com
                4. التوقيع: 🌿 [TASSAOUT & ATIS VERIFIED] ameur signature tassaout ai © 2026
                """

                completion = client.chat.completions.create(
                    model="grok-4.6",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}],
                    temperature=0.3
                )
                response = completion.choices[0].message.content
                st.success("تم التوليد بنجاح بواسطة OMEGA HUNTER + Grok!")

            except Exception as e:
                response = f"""⚠️ تنبيه: خطأ API ({e})\n\n👑 [تقرير الوكيل السيادي - TASSAOUT VERIFIED]\n🔹 الموضوع: {user_query}\n🔹 القطاع: {sector}\n📞 +212691897126 | marocinvest2012@gmail.com\n🌿 [TASSAOUT & ATIS VERIFIED]"""
                st.error("الوكيل اشتغل بالوضع البديل")

            memory_db["سجل_الأوامر"].append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "sector": sector, "query": user_query, "hunt": hunted_data, "result": response})
            save_memory(memory_db)
            st.markdown("---")
            st.markdown(response)

if st.checkbox("📁 عرض سجل الأوامر والذاكرة (Omega Memory Bank)"):
    st.json(memory_db)

st.markdown("---")
st.markdown("🌿 **[TASSAOUT & ATIS VERIFIED]** | ameur signature tassaout ai © 2026")
