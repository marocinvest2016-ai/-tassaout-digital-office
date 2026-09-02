# ==============================================================================
# app.py - OMEGA AGENT CLEAN | GROQ FREE
# ==============================================================================

import streamlit as st
import os
import json
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="الوكيل الذكي | GROQ FREE", page_icon="👑", layout="centered")

st.markdown('<h1 style="text-align:center;color:#800020;">👑 OMEGA AGENT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">VOLT_HUNTER + GROQ LLAMA 3.3 | TASSAOUT & ATIS</p>', unsafe_allow_html=True)
st.markdown("---")

# المفاتيح من Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

# الذاكرة
MEMORY_FILE = "memory.json"
def load_mem():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return []
def save_mem(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
memory = load_mem()

def hunt(query):
    return f"Market data found for: {query}"

# الواجهة
sector = st.selectbox("اختر القطاع", ["🏭 العقار", "🏗️ الهندسة", "🌐 التجارة"])
user_input = st.text_area("أدخل طلبك", placeholder="مثال: شقق للبيع في قلعة السراغنة")

if st.button("⚡ شغل الوكيل"):
    if user_input:
        with st.spinner("جاري التوليد بواسطة Groq..."):

            hunt_data = hunt(user_input)
            st.info(f"✅ {hunt_data}")

            try:
                client = Groq(api_key=GROQ_API_KEY)

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
                    model="llama-3.3-70b-versatile", # أقوى موديل مجاني
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )
                output = res.choices[0].message.content
                st.success("✅ تم التوليد بنجاح بواسطة Groq Llama 3.3")

            except Exception as e:
                output = f"👑 [تقرير بديل]\nالموضوع: {user_input}\nالقطاع: {sector}\n📞 +212691897126\n🌿 [TASSAOUT & ATIS VERIFIED]"
                st.error(f"الوضع البديل: {e}")

            memory.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "request": user_input, "output": output})
            save_mem(memory)

            st.markdown("---")
            st.markdown(output)

with st.expander("📁 سجل الأوامر"):
    st.json(memory)

st.markdown("🌿 [TASSAOUT & ATIS VERIFIED] | ameur signature tassaout ai © 2026")
