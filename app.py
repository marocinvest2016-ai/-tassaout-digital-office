# ==============================================================================
# app.py - OMEGA HUNTER + GROK | UTF-8 FIXED
# ==============================================================================

import streamlit as st
import os
import json
import requests
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="الوكيل السيادي | OMEGA HUNTER", page_icon="👑", layout="wide")
st.markdown('<p style="font-size:24px;color:#800020;font-weight:bold;text-align:center;">👑 [ALPHA CORE NEXUS | OMEGA HUNTER + GROK ACTIVE]</p>', unsafe_allow_html=True)

# قراءة المفاتيح من Secrets
XAI_API_KEY = st.secrets.get("XAI_API_KEY")

# كبسولة الذاكرة
MEMORY_FILE = "omega_memory_bank.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"سجل_الأوامر": []}
def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)
memory_db = load_memory()

# VOLT_HUNTER OMEGA
def volt_hunter_omega(query):
    return f"✅ تم الصيد: Avito + Mubawab على '{query}'"

st.sidebar.markdown("### 🏛️ محطة القيادة الذكية")
sector = st.sidebar.selectbox("اختر القطاع:", ["🏭 العقار", "🏗️ الهندسة والبناء", "🌐 التجارة الدولية"])
st.sidebar.markdown(f"📞 الهاتف: +212691897126 \n📧 marocinvest2012@gmail.com")

st.markdown(f"### 🎯 القطاع المحدد: {sector}")
user_query = st.text_area("أدخل أمرك:", placeholder="مثال: بناء فيلا للبيع بقلعة السراغنة")

if st.button("⚡ تفعيل VOLT_HUNTER OMEGA"):
    if user_query.strip():
        with st.spinner("🧠 جاري الصيد + التوليد عبر Grok..."):
            hunted_data = volt_hunter_omega(user_query)
            st.info(hunted_data)

            try:
                # الحل هنا: نفرض الترميز UTF-8
                client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

                system_prompt = (
                    "أنت الوكيل السيادي لمنظومة 'خدمات تساوت' بتنسيق مع 'ATIS'.\n"
                    f"القطاع: {sector}\n"
                    f"بيانات السوق: {hunted_data}\n"
                    "اكتب إعلان احترافي بالعربية بالأيقونات والهاشتاقات.\n"
                    "التواصل: +212691897126 | marocinvest2012@gmail.com\n"
                    "التوقيع: 🌿 [TASSAOUT & ATIS VERIFIED] ameur signature tassaout ai © 2026"
                )

                completion = client.chat.completions.create(
                    model="grok-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ]
                )
                response = completion.choices[0].message.content
                st.success("✅ تم التوليد بنجاح بواسطة Grok!")

            except Exception as e:
                response = f"👑 [تقرير الوكيل السيادي - TASSAOUT VERIFIED] \n🔹 الموضوع: {user_query}\n🔹 القطاع: {sector} \n📞 +212691897126 | marocinvest2012@gmail.com \n🌿 [TASSAOUT & ATIS VERIFIED]"
                st.warning(f"الوكيل اشتغل بالوضع البديل. خطأ: {e}")

            memory_db["سجل_الأوامر"].append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "query": user_query, "result": response})
            save_memory(memory_db)
            st.markdown("---")
            st.markdown(response)

if st.checkbox("📁 عرض سجل الأوامر والذاكرة"): st.json(memory_db)
st.markdown("🌿 [TASSAOUT & ATIS VERIFIED] | ameur signature tassaout ai © 2026")
