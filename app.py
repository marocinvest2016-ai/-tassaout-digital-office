import os, streamlit as st, sqlite3, pandas as pd
from datetime import datetime
from fpdf import FPDF
from supabase import create_client

# 1. الإعدادات الأساسية
st.set_page_config(page_title="AmarAgent v4.2", page_icon="🇲🇦", layout="wide")
NOM_ENTREPRISE = st.secrets.get("NOM_ENTREPRISE", "Sraghna Digital Market")
ICE = st.secrets.get("ICE", "غير محدد")
RC = st.secrets.get("RC", "غير محدد")
DB_NAME = "amar_agent_memory.db"
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# 2. إدارة قاعدة البيانات المحلية
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS opportunites (id INTEGER PRIMARY KEY, date_ajout TEXT, region TEXT, ville TEXT, type TEXT, objet TEXT, montant REAL, ht REAL, tva REAL, benefice REAL, concurrence TEXT, statut TEXT)''')
    conn.commit(); conn.close()
init_db()

def save_opp(opp):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("INSERT INTO opportunites VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)", (opp['date_ajout'], opp['region'], opp['ville'], opp['type'], opp['objet'], opp['montant'], opp['ht'], opp['tva'], opp['benefice'], opp['concurrence'], "جديد"))
    conn.commit(); conn.close()

def get_all_opps():
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT * FROM opportunites ORDER BY date_ajout DESC")
    data = c.fetchall(); conn.close(); return data

# 3. محرك AmarAgent
class AmarAgent:
    def log_msg(self, msg):
        if 'log' not in st.session_state: st.session_state.log = []
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def scanner(self):
        self.log_msg("🔍 بدء مسح الصفقات (محاكاة)...")
        opps = [
            {"region": "Marrakech-Safi", "ville": "El Kelaa", "type": "BC", "objet": "Fourniture Materiaux", "montant": 145000},
            {"region": "Beni Mellal", "ville": "Beni Mellal", "type": "BC", "objet": "Travaux Amenagement", "montant": 85000}
        ]
        for opp in opps:
            opp['ht'] = round(opp['montant'] / 1.2, 2); opp['tva'] = round(opp['montant'] - opp['ht'], 2)
            opp['benefice'] = round(opp['ht'] * 0.14, 2); opp['concurrence'] = "ضعيفة"
            opp['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_opp(opp)
            try: supabase.table("opportunites").insert(opp).execute()
            except: pass
        self.log_msg("✅ تم جلب الفرص بنجاح.")

    def generer_pdf(self, opp):
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "DOSSIER DE SOUMISSION", 0, 1, 'C')
        pdf.ln(10); pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Objet: {opp[5]} | Montant: {opp[6]} DH", 0, 1)
        if not os.path.exists("data"): os.makedirs("data")
        file_path = f"data/Soumission_{opp[0]}.pdf"
        pdf.output(file_path); return file_path

# 4. الواجهة (UI)
st.title(f"🚀 {NOM_ENTREPRISE} - لوحة التحكم")
agent = AmarAgent()
if st.button("🔄 بدء الرصد الفوري"):
    agent.scanner()
    st.rerun()

data = get_all_opps()
if data:
    df = pd.DataFrame(data, columns=['ID', 'Date', 'Region', 'Ville', 'Type', 'Objet', 'TTC', 'HT', 'TVA', 'Gain', 'Conc', 'Statut'])
    st.dataframe(df)
    sel_id = st.selectbox("اختر ID لتوليد الملف:", df['ID'].tolist())
    if st.button("📄 إنشاء ملف التقديم"):
        file = agent.generer_pdf(df[df['ID'] == sel_id].values[0])
        st.success("تم!")
        with open(file, "rb") as f: st.download_button("تحميل الملف", f, file_name="Dossier.pdf")
