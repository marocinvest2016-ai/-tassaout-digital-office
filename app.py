import os, streamlit as st, requests, sqlite3, schedule, time, threading, pandas as pd
from datetime import datetime
from fpdf import FPDF
from tenacity import retry, stop_after_attempt, wait_fixed
from supabase import create_client

# ===== 1. الإعدادات =====
st.set_page_config(page_title="AmarAgent v4.2", page_icon="🇲🇦", layout="wide")

# قرا من st.secrets
WHATSAPP_TOKEN = st.secrets["WHATSAPP_TOKEN"]
WHATSAPP_PHONE_ID = st.secrets["WHATSAPP_PHONE_ID"]
MY_PHONE = st.secrets["MY_PHONE"]
DB_NAME = "amar_agent_memory.db"

# ربط Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ===== 2. قاعدة البيانات SQLite =====
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS opportunites
                 (id INTEGER PRIMARY KEY, date_ajout TEXT, region TEXT, ville TEXT, type TEXT, objet TEXT,
                 montant REAL, ht REAL, tva REAL, benefice REAL, concurrence TEXT, statut TEXT)''')
    conn.commit(); conn.close()

def save_opp(opp):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("INSERT INTO opportunites VALUES (NULL,?,?,?,?,?,?,?)",
              (datetime.now().strftime('%Y-%m-%d %H:%M'), opp['region'], opp['ville'], opp['type'], opp['objet'],
               opp['montant'], opp['ht'], opp['tva'], opp['benefice'], opp['concurrence'], "جديد"))
    conn.commit(); conn.close()

def get_all_opps():
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT * FROM opportunites ORDER BY date_ajout DESC")
    data = c.fetchall(); conn.close(); return data

# ===== 3. الوكيل الذكي =====
class AmarAgent:
    def __init__(self):
        self.nom = st.secrets["NOM_ENTREPRISE"]
        self.ice = st.secrets["ICE"]; self.rc = st.secrets["RC"]
        self.log = []
        if not os.path.exists("data"): os.makedirs("data")

    def log_msg(self, msg):
        full_msg = f"[{datetime.now().strftime('%H:%M')}] {msg}"
        self.log.append(full_msg); st.session_state.log.append(full_msg)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def send_whatsapp(self, message_text):
        url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages" # v20 أحدث
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": MY_PHONE, "type": "text", "text": {"body": message_text[:4096]}}
        return requests.post(url, headers=headers, json=data, timeout=30).json()

    def ask_meta_ai(self, prompt):
        url = "https://api.meta.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {st.secrets['MODEL_API_KEY']}", "Content-Type": "application/json"}
        data = {"model": "muse-spark", "messages": [
            {"role": "system", "content": f"انت عامر، مساعد ديجيتال ديال {self.nom}. جاوب بالدارجة المغربية وباختصار"},
            {"role": "user", "content": prompt}
        ]}
        r = requests.post(url, headers=headers, json=data, timeout=60)
        return r.json()["choices"][0]["message"]["content"]

    def scanner(self):
        self.log_msg("🔍 السكان فـ 12 جهة + حفظ دائم...")
        opps = []
        opps.append({"region": "Souss-Massa", "ville": "Agadir", "type": "BC", "objet": "Achat Peinture", "montant": 52000})
        opps.append({"region": "Marrakech-Safi", "ville": "Marrakech", "type": "BC", "objet": "Fournitures Bureau", "montant": 45000})

        for opp in opps:
            ht = opp['montant'] / 1.20
            opp['ht'] = round(ht, 2); opp['tva'] = round(opp['montant'] - ht, 2)
            opp['benefice'] = round(ht * 0.14, 2)
            opp['concurrence'] = "🟢 ضعيفة" if opp['montant'] < 100000 else "🟡 متوسطة"
            opp['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M') # زدتها باش Supabase يقبل
            save_opp(opp)
            supabase.table("opportunites").insert(opp).execute() # حفظ فـ السحابة
        return opps

    def generer_pdf(self, opp):
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "DOSSIER DE SOUMISSION", 0, 1, 'C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Entreprise: {self.nom}", 0, 1)
        pdf.cell(0, 10, f"ICE: {self.ice} | RC: {self.rc}", 0, 1)
        nom_fichier = f"data/Dossier_{opp['ville']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        pdf.output(nom_fichier); self.log_msg(f"✅ PDF محفوظ: {nom_fichier}"); return nom_fichier

    def run(self): # زدت هاد الدالة باش الزر يخدم
        self.rapport_quotidien()

    def rapport_quotidien(self):
        opps = self.scanner()
        prompt = f"كتب لي تقرير واتساب بالدارجة على هاد الفرص: {opps}. خليه قصير وفيه الربح المتوقع"
        msg = self.ask_meta_ai(prompt)
        self.send_whatsapp(msg)
        self.log_msg("✅ التقرير تصيفط بـ Meta AI + WhatsApp")

# ===== 4. الواجهة =====
def run_schedule():
    while True: schedule.run_pending(); time.sleep(60)

init_db()
st.title("🇲🇦 AmarAgent v4.2 - الوكيل الذكي للصفقات")
st.markdown("#### 🟢 SQLite + Supabase + Meta AI + WhatsApp")

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
    st.success("✅ مفعل")

st.text_area("📜 سجل النشاط", "\n".join(st.session_state.log), height=300)

st.divider()
st.subheader("🤖 دردشة مع عامر")
prompt = st.text_area("شنو بغيتي عامر يدير؟", "كتب لي رسالة باش نطلب من الكليان يخلص")
if st.button("صيفط فـ الواتساب"):
    jawab = agent.ask_meta_ai(prompt)
    st.write(jawab)
    agent.send_whatsapp(jawab)
