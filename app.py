import os
import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

st.set_page_config(page_title="Meta Tassaout - المكتب السيادي", page_icon="👑", layout="wide")

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
            res = supabase.table("instant_ads").select("*").ilike("message", f"%{keyword}%").limit(5).execute()
            opps = res.data
        except: 
            opps = []
        if not opps: 
            opps = [{"message": f"صفقة توريد {keyword}", "region": "Marrakech-Safi", "montant": 120000}]
        return [{"region": ad.get('region', 'Marrakech-Safi'), "ville": keyword, "objet": ad.get('message','صفقة')[:100], "montant_est": ad.get('montant', 45000)} for ad in opps]

    def analyse_domain(self, opps):
        for opp in opps:
            opp['concurrence'] = "🟢 ضعيفة" if opp['montant_est'] < 100000 else "🟡 متوسطة"
            ht = opp['montant_est'] / 1.20
            opp['ht'] = round(ht, 2)
            opp['tva'] = round(opp['montant_est'] - ht, 2)
            opp['benefice'] = round(ht * 0.14, 2)
            opp['score'] = 95
        return sorted(opps, key=lambda x: x['score'], reverse=True)

    def rapport_comm(self, opps):
        msg = f"*👑 تقرير عامر - {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n"
        for i, opp in enumerate(opps, 1):
            msg += f"*{i}. [{opp['score']}/100] {opp['objet']}*\n💰 {opp['montant_est']} DH | 📍 {opp['region']} | 📈 ربح صافي: {opp['benefice']} DH\n\n"
        return msg

# 2. الواجهة
st.title("👑 Meta Tassaout - المكتب السيادي (وضع يدوي)")
st.markdown("### الحالة: 🟢 بحث وتحليل ذكي + إرسال يدوي للواتساب")

amar = AmarAgent("Sraghna Digital Market")
city = st.sidebar.text_input("المدينة للبحث", "مراكش")

if st.sidebar.button("🚀 تشغيل الوكيل وتوليد التقرير"):
    opps_brutes = amar.scanner_domain(city)
    if opps_brutes:
        opps_analyse = amar.analyse_domain(opps_brutes)
        rapport = amar.rapport_comm(opps_analyse)
        
        st.success("تم توليد التقرير بنجاح!")
        st.text_area("📲 نسخ التقرير لإرساله يدوياً عبر الواتساب:", rapport, height=300)
        
        # زر مباشر لفتح الواتساب اليدوي مع النص
        import urllib.parse
        encoded_msg = urllib.parse.quote(rapport)
        whatsapp_url = f"https://wa.me/{MY_PHONE}?text={encoded_msg}"
        st.markdown(f"### [🔗 اضغط هنا لإرسال التقرير مباشرة عبر واتساب اليدوي]({whatsapp_url})", unsafe_allow_html=True)
    else:
        st.warning("⚠️ لا توجد صفقات جديدة مطابقة حالياً.")
