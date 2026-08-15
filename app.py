import os, streamlit as st, requests, sqlite3, schedule, time, threading
from datetime import datetime
from fpdf import FPDF
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="AmarAgent v4.1", page_icon="🇲🇦", layout="wide")

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
MY_PHONE = "212691897126"
DB_NAME = "amar_agent_memory.db" # قاعدة البيانات اللي ما كتمسحش

# --- 1. قاعدة البيانات الدائمة ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # جدول الفرص
    c.execute('''CREATE TABLE IF NOT EXISTS opportunites
                 (id INTEGER PRIMARY KEY, date_ajout TEXT, region TEXT, ville TEXT, type TEXT, objet TEXT, 
                 montant REAL, ht REAL, tva REAL, benefice REAL, concurrence TEXT, statut TEXT)''')
    # جدول التقارير
    c.execute('''CREATE TABLE IF NOT EXISTS rapports
                 (id INTEGER PRIMARY KEY, date_rapport TEXT, contenu TEXT)''')
    # جدول الدواسي PDF
    c.execute('''CREATE TABLE IF NOT EXISTS dossiers_pdf
                 (id INTEGER PRIMARY KEY, date_creation TEXT, nom_fichier TEXT, objet TEXT)''')
    conn.commit(); conn.close()

def save_opp(opp):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("INSERT INTO opportunites VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)", 
              (datetime.now(), opp['region'], opp['ville'], opp['type'], opp['objet'], 
               opp['montant'], opp['ht'], opp['tva'], opp['benefice'], opp['concurrence'], "جديد"))
    conn.commit(); conn.close()

def get_all_opps():
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT * FROM opportunites ORDER BY date_ajout DESC")
    data = c.fetchall(); conn.close(); return data

# --- 2. الوكيل الذكي ---
class AmarAgent:
    def __init__(self):
        self.nom = os.getenv("NOM_ENTREPRISE")
        self.ice = os.getenv("ICE"); self.rc = os.getenv("RC")
        self.priorite_regions = ["Marrakech-Safi", "Beni Mellal-Khenifra", "Souss-Massa"]
        self.log = []

    def log_msg(self, msg):
        full_msg = f"[{datetime.now().strftime('%H:%M')}] {msg}"
        self.log.append(full_msg); st.session_state.log.append(full_msg)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def send_whatsapp(self, message_text):
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": MY_PHONE, "type": "text", "text": {"body": message_text[:4096]}}
        return requests.post(url, headers=headers, json=data, timeout=30).json()

    def scanner(self):
        self.log_msg("🔍 السكان فـ 12 جهة + حفظ دائم...")
        opps = []
        # داتا تجريبية - بدلها بسكريبينغ حقي
        opps.append({"region": "Souss-Massa", "ville": "Agadir", "type": "BC", "objet": "Achat Peinture", "montant": 52000})
        opps.append({"region": "Marrakech-Safi", "ville": "Marrakech", "type": "BC", "objet": "Fournitures Bureau", "montant": 45000})
        
        for opp in opps:
            # حساب TVA 20% + الربح + المنافسة
            ht = opp['montant'] / 1.20
            opp['ht'] = round(ht, 2); opp['tva'] = round(opp['montant'] - ht, 2)
            opp['benefice'] = round(ht * 0.14, 2)
            opp['concurrence'] = "🟢 ضعيفة" if opp['montant'] < 100000 else "🟡 متوسطة"
            save_opp(opp) # حفظ لا يمسح
        return opps

    def generer_pdf(self, opp):
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "DOSSIER DE SOUMISSION", 0, 1, 'C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Entreprise: {self.nom}", 0, 1)
        pdf.cell(0, 10, f"ICE: {self.ice} | RC: {self.rc}", 0, 1)
        pdf.cell(0, 10, f"Objet: {opp['objet']}", 0, 1)
        pdf.cell(0, 10, f"HT: {opp['ht']} DH | TVA 20%: {opp['tva']} DH | TTC: {opp['montant']} DH", 0, 1)
        nom_fichier = f"data/Dossier_{opp['ville']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        pdf.output(nom_fichier); self.log_msg(f"✅ PDF محفوظ: {nom_fichier}"); return nom_fichier

    def rapport_quotidien(self):
        opps = self.scanner()
        msg = f"*📊 تقرير عامر اليومي - {datetime.now().strftime('%d/%m %H:%M')}*\n"
        msg += f"*الوكيل المفوض: {self.nom}*\n\n"
        for i, opp in enumerate(opps, 1):
            msg += f"*{i}. [{opp['region']}] {opp['objet']}*\n💰 {opp['montant']} DH | 📈 ربح: {opp['benefice']} DH | {opp['concurrence']}\n"
        self.send_whatsapp(msg)
        self.log_msg("✅ التقرير تصيفط وتحفظ فـ قاعدة البيانات")

    def run(self):
        self.log_msg("🤖 AmarAgent v4.1 بدأ - الذاكرة لا تمسح")
        self.rapport_quotidien()

# --- 3. الواجهة ---
def run_schedule():
    while True: schedule.run_pending(); time.sleep(60)

init_db()
st.title("🇲🇦 AmarAgent v4.1 - الوكيل الذكي للصفقات")
st.markdown("#### 🟢 نسخة لا تقبل المسح | الذاكرة: SQLite | TVA + منافسة + PDF")

if 'log' not in st.session_state: st.session_state.log = ["جاهز"]

agent = AmarAgent()

col1, col2, col3 = st.columns(3)
if col1.button("🚀 تشغيل السكان الآن"): agent.run(); st.rerun()
if col2.button("📂 عرض الذاكرة"):
    data = get_all_opps()
    st.dataframe(pd.DataFrame(data, columns=["ID","التاريخ","الجهة","المدينة","النوع","الموضوع","المبلغ","HT","TVA","الربح","المنافسة","الحالة"]))
if col3.button("⏰ تفعيل 08:00 يوميا"):
    schedule.clear(); schedule.every().day.at("08:00").do(agent.run)
    threading.Thread(target=run_schedule, daemon=True).start()
    st.success("✅ مفعل - الذاكرة محفوظة")

st.text_area("📜 سجل النشاط", "\n".join(st.session_state.log), height=300)
