import os, streamlit as st, sqlite3, pandas as pd
from datetime import datetime
from fpdf import FPDF
from supabase import create_client

st.set_page_config(page_title="AmarAgent v4.2", page_icon="🇲🇦", layout="wide")

# قرا من st.secrets
NOM_ENTREPRISE = st.secrets["NOM_ENTREPRISE"]
ICE = st.secrets["ICE"]
RC = st.secrets["RC"]
DB_NAME = "amar_agent_memory.db"

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS opportunites
                 (id INTEGER PRIMARY KEY, date_ajout TEXT, region TEXT, ville TEXT, type TEXT, objet TEXT,
                 montant REAL, ht REAL, tva REAL, benefice REAL, concurrence TEXT, statut TEXT)''')
    conn.commit(); conn.close()

def save_opp(opp):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    # صلحنا هنا: 12 عمود = 12 قيمة
    c.execute("INSERT INTO opportunites VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)",
              (opp['date_ajout'], opp['region'], opp['ville'], opp['type'], opp['objet'],
               opp['montant'], opp['ht'], opp['tva'], opp['benefice'], opp['concurrence'], "جديد"))
    conn.commit(); conn.close()

def get_all_opps():
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT * FROM opportunites ORDER BY date_ajout DESC")
    data = c.fetchall(); conn.close(); return data

class AmarAgent:
    def __init__(self):
        self.nom = NOM_ENTREPRISE
        self.ice = ICE; self.rc = RC
        self.log = []
        if not os.path.exists("data"): os.makedirs("data")

    def log_msg(self, msg):
        full_msg = f"[{datetime.now().strftime('%H:%M')}] {msg}"
        self.log.append(full_msg); st.session_state.log.append(full_msg)

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
            opp['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_opp(opp)
            try:
                supabase.table("opportunites").insert(opp).execute()
                self.log_msg(f"✅ تم الحفظ في Supabase: {opp['objet']}")
            except Exception as e:
                self.log_msg(f"⚠️ خطأ Supabase: {e}")
        return opps

    def generer_pdf(self, opp):
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "DOSSIER DE SOUMISSION", 0, 1, 'C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Entreprise: {self.nom}", 0, 1)
        pdf.cell(0, 10, f"ICE: {self.ice} | RC: {self.rc}", 0, 1)
        pdf.cell(0, 10, f"Objet: {opp['objet']} - {opp['ville']}", 0, 1)
        pdf.cell(0, 10, f"Montant TTC: {opp['montant']} MAD", 0, 1)
        pdf.cell(0, 10, f"Benefice Estime: {opp['benefice']} MAD", 0, 1)
        nom_fichier = f"data/Dossier_{opp['ville
