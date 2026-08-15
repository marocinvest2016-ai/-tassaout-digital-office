import os
import streamlit as st
import pandas as pd
import requests
import schedule
import time
import threading
from datetime import datetime
from fpdf import FPDF
from supabase import create_client, Client

st.set_page_config(page_title="Meta Tassaout - المكتب السيادي", page_icon="👑", layout="wide")

# 1. الاتصال بـ Supabase + Secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
WHATSAPP_TOKEN = st.secrets.get("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = st.secrets.get("WHATSAPP_PHONE_ID", "")
MY_PHONE = "212691897126" # رقمك المعتمد

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AmarAgent:
    def __init__(self, nom_entreprise):
        self.nom = nom_entreprise
        self.priorite_regions = ["Marrakech-Safi", "Beni Mellal-Khenifra", "Souss-Massa"]

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

# 2. دالة الإرسال عبر WhatsApp API
def send_whatsapp_alert(message_text):
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": MY_PHONE, "type": "text", "text": {"body": message_text[:4096]}}
    response = requests.post(url, headers=headers, json=data, timeout=30)
    return response.json()

# 3. دالة المهمة التلقائية
def job_quotidien():
    log_msg = f"[{datetime.now().strftime('%H:%M')}] بدأ البحث التلقائي..."
    st.session_state.log.append(log_msg)
    amar = AmarAgent("Sraghna Digital Market")
    city = "مراكش"
    opps_brutes = amar.scanner_domain(city)
    if opps_brutes:
        opps_analyse = amar.analyse_domain(opps_brutes)
        rapport = amar.rapport_comm(opps_analyse)
        status = send_whatsapp_alert(rapport)
        if "messages" in status:
            st.session_state.log.append(f"[{datetime.now().strftime('%H:%M')}] ✅ تم الإرسال للواتساب")
        else:
            st.session_state.log.append(f"[{datetime.now().strftime('%H:%M')}] ❌ فشل: {status}")
    else:
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M')}] ⚠️ لا توجد صفقات جديدة")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

# 4. الواجهة
st.title("👑 Meta Tassaout - المكتب السيادي v5.1")
st.markdown("### الحالة: 🟢 وكيل مستقل + WhatsApp API مباشر")

if 'log' not in st.session_state:
    st.session_state.log = []

amar = AmarAgent("Sraghna Digital Market")
city = st.sidebar.text_input("المدينة للبحث", "مراكش")

st.sidebar.header("⚙️ التحكم اليدوي")
if st.sidebar.button("🚀 تشغيل الوكيل وإرسال للواتساب"):
    job_quotidien()
    st.sidebar.success("تم تشغيل الوكيل وإرسال التقرير بنجاح")

st.sidebar.header("🤖 الأوتوماتيك")
if st.sidebar.button("تشغيل الجدولة 08:00"):
    schedule.clear()
    schedule.every().day.at("08:00").do(job_quotidien)
    thread = threading.Thread(target=run_schedule, daemon=True)
    thread.start()
    st.sidebar.success("✅ الأوتوماتيك مفعل كل 8h00 الصباح")

st.subheader("📜 سجل العمليات")
st.text_area("", "\n".join(st.session_state.log), height=300)
