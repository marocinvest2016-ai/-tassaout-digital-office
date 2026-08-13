import streamlit as st
from supabase import create_client
import schedule, time, threading, random, requests
from datetime import datetime
from bs4 import BeautifulSoup
from fpdf import FPDF

st.set_page_config(page_title="👑 Meta Tassaout - العنكبوت السيادي", layout="wide")

# ====== 1. السيكريتس ======
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    WHATSAPP_TOKEN = st.secrets.get("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID = st.secrets.get("WHATSAPP_PHONE_ID", "")
except:
    st.warning("⚠️ عَمّر السيكريتس فـ Settings > Secrets")
    SUPABASE_URL = ""; SUPABASE_KEY = ""; WHATSAPP_TOKEN = ""; WHATSAPP_PHONE_ID = ""

CTA_OFFICIEL = "212691897126"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

# ====== 2. المواقع و الكلمات المفاتيح ======
SITES_A_SCRAPER = {
    "الوطنية": "https://www.marchespublics.gov.ma/pmmp/recherche/recherAvis.do",
    "جماعة قلعة السراغنة": "https://www.sraghna.gov.ma",
    "جماعة أكادير": "https://www.agadir.ma",
    "جهة مراكش آسفي": "https://www.regionmarrakechsafi.ma"
}
MOTS_CLES = "Bon de Commande سند طلب اسمنت حديد بناء فلاحة مكتبيات متلاشيات توريد"

# ====== 3. مولد PDF ======
def creer_bc_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "BON DE COMMANDE / سند الطلب", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 8, f"N°: BC-{random.randint(1000,9999)}")
    pdf.cell(100, 8, f"Date: {datetime.now().strftime('%d/%m/%Y')}", ln=1)
    pdf.ln(5)
    pdf.cell(200, 8, "De: Administration / الإدارة", ln=1)
    pdf.cell(200, 8, f"A: SRAGHNA DIGITAL MARKET - Tel: {CTA_OFFICIEL}", ln=1)
    pdf.ln(5)
    pdf.cell(20, 8, "Qté", 1); pdf.cell(100, 8, "Désignation / البيان", 1); pdf.cell(40, 8, "P.U HT", 1); pdf.cell(30, 8, "Total HT", 1, ln=1)
    pdf.cell(20, 8, "100", 1); pdf.cell(100, 8, "Sacs Ciment CPJ 45 / أكياس الاسمنت", 1); pdf.cell(40, 8, "...... DH", 1); pdf.cell(30, 8, "...... DH", 1, ln=1)
    pdf.ln(10)
    pdf.cell(200, 8, "Lieu de livraison: قلعة السراغنة", ln=1)
    pdf.cell(200, 8, "Délai: 48H | Paiement: 45 Jours", ln=1)
    pdf.ln(15)
    pdf.cell(200, 8, "Cachet et Signature", ln=1, align='R')
    return bytes(pdf.output())

# ====== 4. العنكبوت ======
def formater_alerte(source, titre, acheteur, delai):
    message = f"""🏛️ *تنبيه جديد - {source}*
📋 *الموضوع*: {titre}
🏢 *الجهة*: {acheteur}
⏳ *آخر أجل*: {delai}
🎯 *SRAGHNA DIGITAL MARKET*
📞 {CTA_OFFICIEL}"""
    return {"content": titre, "message": message, "source": source, "created_at": datetime.now().isoformat()}

def robot_cherche_partout():
    if not supabase: return 0
    nouvelles_alerts = 0
    try:
        params = {"mode": "rechercheSimple", "motsCles": MOTS_CLES}
        r = requests.get(SITES_A_SCRAPER["الوطنية"], params=params, timeout=15)
        soup = BeautifulSoup(r.content, 'lxml')
        for row in soup.find_all("tr", class_="ligneResultat")[:3]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                alert = formater_alerte("الوطنية", cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip())
                if not supabase.table("instant_ads").select("id").eq("content", alert['content']).execute().data:
                    supabase.table("instant_ads").insert(alert).execute(); nouvelles_alerts += 1
    except Exception as e: st.error(f"خطأ: {e}")
    return nouvelles_alerts

def tache_autonome():
    st.toast("🕷️ العنكبوت كيقلب...")
    count = robot_cherche_partout()
    if count > 0: st.success(f"✅ تم تسجيل {count} تنبيه جديد")
    else: st.info("لا توجد صفقات جديدة")

# ====== 5. المجدول ======
if 'scheduler' not in st.session_state and supabase:
    schedule.every(4).hours.do(tache_autonome)
    def run_schedule():
        while True: schedule.run_pending(); time.sleep(60)
    threading.Thread(target=run_schedule, daemon=True).start()
    st.session_state.scheduler = True

# ====== 6. الواجهة ======
st.title("👑 Meta Tassaout - العنكبوت السيادي")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 مسح شامل الآن", use_container_width=True, type="primary"):
        tache_autonome()
with col2:
    pdf_data = creer_bc_pdf()
    st.download_button("🧾 تحميل BC PDF", pdf_data, "BC_SRAGHNA.pdf", "application/pdf", use_container_width=True)

st.divider()
st.subheader("📊 اخر 10 تنبيهات")
if supabase:
    ads = supabase.table("instant_ads").select("message").order("created_at", desc=True).limit(10).execute().data
    for ad in ads: st.code(ad['message'], language="markdown")
