import streamlit as st
import urllib.parse
from supabase import create_client
from agent import OmegaAgent

st.set_page_config(page_title="OMEGA AGENTIC META", page_icon="👑", layout="wide")
st.markdown('<h1 style="text-align:center;color:#800020;">👑 OMEGA AGENTIC SUPER AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">Powered by META AI MUSE-SPARK 1.2 | TASSAOUT & ATIS</p>', unsafe_allow_html=True) # <-- مذكور Meta

# الاتصال
SUPA_URL = st.secrets["SUPABASE_URL"]
SUPA_KEY = st.secrets["SUPABASE_KEY"]
WA_NUM = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "212691897126")
supabase = create_client(SUPA_URL, SUPA_KEY)

domaine = st.selectbox("🏛️ المجال", ["العقار", "الهندسة", "التجارة"])
task = st.text_area("🎯 المهمة", "شقق للبيع في قلعة السراغنة")
send_to = st.text_input("📞 رقم الواتساب", WA_NUM)

if st.button("⚡ فعل وكلاء Meta"):
    agent = OmegaAgent(domaine)

    with st.spinner("MUSE-SPARK 1.2 من Meta يخدم..."): # <-- مذكور Meta
        plan = agent.ceo(task)
        st.subheader("🧠 المدير التنفيذي - Meta AI")
        st.write(plan)

        ad = agent.copywriter(plan)
        st.subheader("📢 الكاتب - Meta AI")
        st.write(ad)

        final_ad = agent.closer(ad)
        st.subheader("🔥 الإعلان النهائي - Meta AI")
        st.success(final_ad)

        link = f"https://wa.me/{send_to}?text={urllib.parse.quote(final_ad)}"
        st.markdown(f"[📲 اضغط للإرسال عبر واتساب]({link})")

        supabase.table("ads").insert({"domaine": domaine, "ad": final_ad}).execute()
        st.info("💾 تم الحفظ في Supabase")

st.markdown("---")
st.markdown("🌿 Powered by META | TASSAOUT & ATIS © 2026")
