import os, streamlit as st, sqlite3, pandas as pd
from datetime import datetime
from fpdf import FPDF
from supabase import create_client

st.set_page_config(page_title="AmarAgent v4.2", page_icon="🇲🇦", layout="wide")

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
    c.execute("INSERT INTO opportunites VALUES (NULL,?,?,?,?,?,?,?)",
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
        self.log_msg("🔍 بدأ السكان...")
        opps = [
            {"region": "Souss-Massa", "ville": "Agadir", "type": "BC", "objet": "Achat Peinture", "montant": 52000},
            {"region": "Marrakech-Safi", "ville": "Marrakech", "type": "BC", "objet": "Fournitures Bureau", "montant": 45000}
        ]
        for opp in opps:
            ht = opp['montant'] / 1.20
            opp['ht'] = round(ht, 2); opp['tva'] = round(opp['montant'] - ht, 2)
            opp['benefice'] = round(ht * 0.14, 2)
            opp['concurrence'] = "🟢 ضعيفة" if opp['montant'] < 100000 else "🟡 متوسطة"
            opp['date_ajout'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_opp(opp)
            try:
                supabase.table("opportunites").insert(opp).execute()
                self.log_msg(f"✅ تم الحفظ: {opp['objet']}")
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
        
        # هذا هو السطر المصحح
        nom_fichier = f"data/Dossier_{opp['ville']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        pdf.output(nom_fichier); self.log_msg(f"✅ PDF جاهز: {nom_fichier}"); return nom_fichier

    def run(self):
        opps = self.scanner()
        for opp in opps:
            pdf_path = self.generer_pdf(opp)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"📄 تنزيل PDF: {opp['ville']}",
                    data=f,
                    file_name=pdf_path.split('/')[-1],
                    mime="application/pdf"
                )
        self.log_msg("✅ انتهى")

init_db()
st.title("🇲🇦 AmarAgent v4.2 - الوكيل الذكي للصفقات")
st.markdown("#### 🟢 SQLite + Supabase + PDF")

if 'log' not in st.session_state: st.session_state.log = ["جاهز للعمل"]
agent = AmarAgent()

col1, col2 = st.columns(2)
if col1.button("🚀 تشغيل السكان الآن"): 
    agent.run()
    st.rerun()
    
if col2.button("📂 عرض الذاكرة"):
    data = get_all_opps()
    if data: 
        df = pd.DataFrame(data, columns=["ID","التاريخ","الجهة","المدينة","النوع","الموضوع","المبلغ","HT","TVA","الربح","المنافسة","الحالة"])
        st.dataframe(df, use_container_width=True)
    else: 
        st.info("لا توجد بيانات بعد")

st.text_area("📜 سجل النشاط", "\n".join(st.session_state.log), height=250)
