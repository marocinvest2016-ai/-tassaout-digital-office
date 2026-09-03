import streamlit as st
import urllib.parse
from supabase import create_client
from agent import OmegaAgent

st.set_page_config(page_title="OMEGA AGENTIC META", page_icon="👑", layout="wide")
st.markdown('<h1 style="text-align:center;color:#800020;">👑 OMEGA AGENTIC SUPER AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">Powered by META AI MUSE-SPARK 1.2 | TASSAOUT & ATIS</p>', unsafe_allow_html=True)

# الاتصال بقاعدة البيانات
try:
    SUPA_URL = st.secrets["SUPABASE_URL"]
    SUPA_KEY = st.secrets["SUPABASE_KEY"]
    supabase = create_client(SUPA_URL, SUPA_KEY)
except Exception as e:
    st.error(f"⚠️ خطأ في الاتصال بقاعدة بيانات Supabase: {e}")

WA_NUM = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "212691897126")

domaine = st.selectbox("🏛️ المجال", ["العقار", "الهندسة", "التجارة"])
task = st.text_area("🎯 المهمة", "شقق للبيع في قلعة السراغنة")
send_to = st.text_input("📞 رقم الواتساب", WA_NUM)

if st.button("⚡ فعل وكلاء Meta"):
    if not task.strip():
        st.warning("⚠️ يرجى إدخال تفاصيل المهمة أولاً.")
    else:
        agent = OmegaAgent(domaine)

        with st.spinner("MUSE-SPARK 1.2 من Meta يخدم..."):
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
            st.markdown(f'<a href="{link}" target="_blank" style="display:inline-block;background-color:#25D366;color:white;padding:12px 20px;border-radius:8px;font-weight:bold;text-decoration:none;margin-top:10px;text-align:center;width:100%;">📲 اضغط للإرسال عبر واتساب</a>', unsafe_allow_html=True)

            try:
                supabase.table("ads").insert({"domaine": domaine, "ad": final_ad}).execute()
                st.info("💾 تم الحفظ في Supabase بنجاح")
            except Exception as db_err:
                st.warning(f"⚠️ تعذر الحفظ في قاعدة البيانات (تأكد من وجود جدول ads): {db_err}")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #4B5563; font-size: 13px;">🌿 Powered by META | TASSAOUT & ATIS © 2026</div>', unsafe_allow_html=True)
