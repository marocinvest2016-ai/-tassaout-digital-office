import streamlit as st
from openai import OpenAI
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="DANA OMEGA BRAIN", page_icon="🧠", layout="wide")

# 2. الاتصال بـ Groq بأمان
@st.cache_resource
def get_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error("❌ خطأ فادح: GROQ_API_KEY غير موجود فـ Streamlit Secrets")
        st.info("سير لـ Settings > Secrets وزيد: GROQ_API_KEY = 'gsk_xxx'") # هنا صلحت القوس
        st.stop()

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

client = get_client()

# 3. دالة الاتصال بـ Groq
def call_dana(prompt, model="openai/gpt-oss-120b"):
    system_prompt = "أنت DANA OMEGA BRAIN. مساعد ذكي مغربي. جاوب بالدارجة + العربية الفصحى. استعمل نقاط و emojis و جداول."
    try:
        with st.spinner("🧠 DANA كيفكر..."):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.75,
                max_tokens=2000
            )
        result = response.choices[0].message.content
        st.session_state.last_result = result
        return result
    except Exception as e:
        return f"❌ خطأ من Groq: {e}"

# 4. الواجهة
st.title("🧠 DANA OMEGA BRAIN v3.0")
st.caption("مدعوم بـ Groq + Llama + GPT-OSS")

tab1, tab2 = st.tabs(["💬 الدردشة", "📄 محلل نصوص Grok"])

with tab1:
    user_input = st.text_area("سول DANA على أي حاجة", height=150, placeholder="مثال: استراتيجية بيع شقة فقلعة السراغنة")
    if st.button("🚀 أطلق DANA", type="primary"):
        if user_input.strip():
            output = call_dana(user_input)
            st.markdown("### النتيجة:")
            st.markdown(output)
        else:
            st.warning("كتب السؤال أولا")

with tab2:
    st.subheader("الصق ما كتبه Grok هنا ونحللو ليك")
    grok_text = st.text_area("نص Grok", height=200, key="grok")
    if st.button("🔍 حلل ليا"):
        if grok_text.strip():
            prompt = f"حلل ليا هاد النص ديال Grok: {grok
