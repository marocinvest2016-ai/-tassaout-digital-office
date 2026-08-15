import os
import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import urllib.parse

st.set_page_config(
    page_title="Meta Tassaout - المكتب السيادي", page_icon="👑", layout="wide"
)

# 1. الاتصال بـ Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
MY_PHONE = "212691897126"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class AmarAgent:

    def __init__(self, nom_entreprise):
        self.nom = nom_entreprise

    def scanner_domain(self, keyword):
        try:
            res = (
                supabase.table("instant_ads")
                .select("*")
                .ilike("message", f"%{keyword}%")
                .limit(5)
                .execute()
            )
            opps = res.data
        except:
            opps = []
        if not opps:
            opps = [{
                "message": f"صفقة توريد {keyword}",
                "region": "Marrakech-Safi",
                "montant": 120000,
            }]
        return [
            {
                "region": ad.get("region", "Marrakech-Safi"),
                "ville": keyword,
                "objet": ad.get("message", "صفقة")[:100],
                "montant_est": ad.get("montant", 45000),
            }
            for ad in opps
        ]

    def analyse_domain(self, opps):
        for opp in opps:
            opp["concurrence"] = (
                "🟢 ضعيفة" if opp["montant_est"] < 100000 else "🟡 متوسطة"
            )
            ht = opp["montant_est"] / 1.20
            opp["ht"] = round(ht, 2)
            opp["tva"] = round(opp["montant_est"] - ht, 2)
            opp["benefice"] = round(ht * 0.14, 2)
            opp["score"] = 95
        return sorted(opps, key=lambda x: x["score"], reverse=True)

    def rapport_comm(self, opps):
        msg = f"*👑 تقرير عامر - {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n"
        for i, opp in enumerate(opps, 1):
            msg += (
                f"*{i}. [{opp['score']}/100] {opp['objet']}*\n💰"
                f" {opp['montant_est']} DH | 📍 {opp['region']} | 📈 ربح صافي:"
                f" {opp['benefice']} DH\n\n"
            )
        return msg


# 2. الواجهة وتعدد التبويبات
st.title("👑 Meta Tassaout - المكتب السيادي")
st.markdown("### الحالة: 🟢 نظام إدارة العقارات والخدمات المتعددة")

tab1, tab2, tab3, tab4 = st.tabs([
    "📸 التصوير أو تحميل الصور",
    "🧠 عروض الوكيل والتفاعل",
    "📚 مواضيع أخرى",
    "➕ إضافة عرض جديد",
])

with tab1:
    st.subheader("رفع ومعالجة الصور التسويقية")
    uploaded_files = st.file_uploader(
        "اختر الصور",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        st.success(f"تم تحميل {len(uploaded_files)} صورة بنجاح!")
        cols = st.columns(3)
        for idx, uploaded_file in enumerate(uploaded_files):
            with cols[idx % 3]:
                st.image(uploaded_file, caption=f"صورة {idx+1}", use_container_width=True)

with tab2:
    st.subheader("تحليلات الوكيل وعروض السوق")
    city = st.sidebar.text_input("المدينة للبحث", "قلعة السراغنة")
    amar = AmarAgent("Sraghna Digital Market")

    if st.button("🚀 تشغيل الوكيل وتوليد التقرير"):
        opps_brutes = amar.scanner_domain(city)
        if opps_brutes:
            opps_analyse = amar.analyse_domain(opps_brutes)
            rapport = amar.rapport_comm(opps_analyse)
            st.success("تم توليد التقرير بنجاح!")
            st.text_area("📲 نسخ التقرير:", rapport, height=200)
            encoded_msg = urllib.parse.quote(rapport)
            whatsapp_url = f"https://wa.me/{MY_PHONE}?text={encoded_msg}"
            st.markdown(f"### [🔗 اضغط هنا للإرسال عبر واتساب]({whatsapp_url})", unsafe_allow_html=True)
        else:
            st.warning("⚠️ لا توجد صفقات مطابقة.")

with tab3:
    st.subheader("📚 مواضيع وأقسام إضافية")
    st.markdown("""
    * **أراضي فلاحية وفيرمات** (قلعة السراغنة ومراكش).
    * **بقع أرضية سكنية وتجارية** (الهدى، البدر، المنارة).
    * **مواد البناء** (RITA FER / Tassaout Services).
    * **خدمات رقمية وتسويق** (لوحات إشهارية وأنظمة ذكية).
    """)

with tab4:
    st.subheader("➕ إضافة عرض عقاري أو صفقة جديدة")
    with st.form("add_ad_form"):
        msg = st.text_input("نص العرض/الإعلان")
        reg = st.text_input("المنطقة/المدينة")
        mnt = st.number_input("المبلغ (بالدرهم)", min_value=0)
        submit = st.form_submit_button("حفظ العرض في السيرفر")
        
        if submit:
            if msg and reg:
                try:
                    data = {"message": msg, "region": reg, "montant": mnt}
                    supabase.table("instant_ads").insert(data).execute()
                    st.success("تم حفظ العرض بنجاح! 🚀")
                except Exception as e:
                    st.error(f"خطأ: {e}")
            else:
                st.warning("يرجى ملء البيانات.")
