# ==============================================================================
# app.py - OMEGA AGENT CLEAN | NO ASCII ERRORS
# ==============================================================================

import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

st.set_page_config(page_title="الوكيل الذكي النقي", page_icon="👑", layout="centered")

# الهيدر
st.markdown('<h1 style="text-align:center;color:#800020;">👑 OMEGA AGENT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">VOLT_HUNTER + GROK | TASSAOUT & ATIS</p>', unsafe_allow_html=True)
st.markdown("---")

# المفاتيح
XAI_API_KEY = st.secrets.get("XAI_API_KEY")

# الذاكرة
MEMORY_FILE = "memory.json"
def load_mem():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return []
def save_mem(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
memory = load_mem()

# الصيد
def hunt(query):
    return f"Market data found for: {query}"

# الواجهة
sector = st.selectbox("اختر القطاع", ["🏭 العقار", "🏗️ الهندسة", "🌐 التجارة"])
user_input = st.text_area("أدخل طلبك", placeholder="مثال: شقق للبيع في قلعة السراغنة")

if st.button("⚡ شغل الوكيل"):
    if user_input:
        with st.spinner("جاري التوليد..."):

            # 1. الصيد
            hunt_data = hunt(user_input)
            st.info(f"✅ {hunt_data}")

            # 2. التوليد عبر Grok - كلشي انجليزي للداخل
            try:
                client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

                prompt = f"""
                You are a marketing agent for Tassaout & ATIS.
                Sector: {sector}
                User request: {user_input}
                Market data: {hunt_data}
                Contact: +212691897126 | marocinvest2012@gmail.com
                Task: Write a professional ad in MOROCCAN ARABIC with emojis and hashtags.
                End with: 🌿 [TASSAOUT & ATIS VERIFIED] ameur signature tassaout ai © 2026
                """

                res = client.chat.completions.create(
                    model="grok-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                output = res.choices[0].message.content
                st.success("✅ تم التوليد بواسطة Grok")

            except Exception as e:
                output = f"👑 [تقرير بديل]\nالموضوع: {user_input}\nالقطاع: {sector}\n📞 +212691897126\n🌿 [TASSAOUT & ATIS VERIFIED]"
                st.error(f"الوضع البديل: {e}")

            # 3. الحفظ
            memory.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "request": user_input, "output": output})
            save_mem(memory)

            st.markdown("---")
            st.markdown(output)

# عرض الذاكرة
with st.expander("📁 سجل الأوامر"):
    st.json(memory)

st.markdown("🌿 [TASSAOUT & ATIS VERIFIED] | ameur signature tassaout ai © 202
