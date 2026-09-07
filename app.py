from datetime import datetime
import io, os, tempfile, requests
import streamlit as st
import googlemaps, gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="OMEGA SOA", page_icon="👑", layout="centered")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# ===== 1. دوال Groq + WhatsApp كما هي =====
def get_available_groq_model(api_key):
    #... نفس الكود ديالك
    return "llama-3.3-70b-versatile"

def call_super_ai(prompt, agent_name, domain):
    #... نفس الكود ديالك
    api_key = st.secrets.get("GROQ_API_KEY", "")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system_prompt = f"You are {agent_name} for '{domain}'. Respond in Moroccan Darija + العربية. Bullets + tables + emojis."
    payload = {"model": get_available_groq_model(api_key), "messages": [{"role":"system","content":system_prompt},{"role":"user","content":prompt}], "temperature": 0.75}
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=90)
    return res.json()["choices"][0]["message"]["content"]

# ===== 2. الخلفية السيادية OMEGA_SOA =====
class OMEGA_SOA:
    def __init__(self):
        try:
            creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=SCOPES)
            self.gsheet = gspread.authorize(creds); self.drive = build("drive", "v3", credentials=creds)
        except: self.gsheet, self.drive = None, None
        try: self.maps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_API_KEY"])
        except: self.maps = None

    def execute_mission(self, task, domain, images):
        brain_output = call_super_ai(f"ضع خطة شاملة لمشروع {domain}: {task}. SWOT + خطة 90 يوم", "Super CEO", domain)
        location = "El Kelaa des Sraghna, Morocco" if "قلعة" in task else "Marrakech, Morocco"
        formatted_address = location
        if self.maps:
            try: formatted_address = self.maps.geocode(location)[0]['formatted_address']
            except: pass
        maps_link = f"https://maps.google.com/?q={location}"
        full_report = f"# OMEGA REPORT\n{brain_output}\n\n📍 {formatted_address}"

        drive_link = "غير متاح"
        if self.drive:
            folder = self.drive.files().create(body={"name":f"OMEGA_{datetime.now().strftime('%Y%m%d')}", "mimeType":"application/vnd.google-apps.folder"}, fields="id").execute()
            folder_id = folder['id']
            self._upload_to_drive(self._generate_pdf(full_report), "Offer.pdf", folder_id, "application/pdf")
            for img in images or []: self._upload_to_drive(img.getvalue(), img.name, folder_id, img.type)
            drive_link = f"https://drive.google.com/drive/folders/{folder_id}"

        sheet_link = "غير متاح"
        if self.gsheet:
            sheet = self.gsheet.open("OMEGA_CRM").sheet1
            sheet.append_row([str(datetime.now()), task, domain, location, drive_link, "جديد"])
            sheet_link = f"https://docs.google.com/spreadsheets/d/{sheet.spreadsheet.id}"

        return {"summary": full_report, "pdf_bytes": self._generate_pdf(full_report), "maps_link": maps_link, "drive_link": drive_link, "sheet_link": sheet_link}

    def _generate_pdf(self, text):
        buffer = io.BytesIO(); c = canvas.Canvas(buffer, pagesize=letter); c.setFont("Helvetica", 9); y = 750
        for line in text.encode('latin-1', 'replace').decode('latin-1').split("\n"): # حل مشكل العربي
            c.drawString(50, y, line[:100]); y -= 14;
            if y < 50: c.showPage(); y = 750
        c.save(); buffer.seek(0); return buffer.getvalue()
    def _upload_to_drive(self, content, name, folder_id, mimetype): self.drive.files().create(body={"name": name, "parents": [folder_id]}, media_body=MediaIoBaseUpload(io.BytesIO(content), mimetype=mimetype)).execute()

# ===== 3. الواجهة النظيفة النهائية =====
tab1, tab2 = st.tabs(["👑 OMEGA SOA", "🎙️ تفريغ صوتي"])

with tab1:
    st.title("👑 OMEGA SOA - المعمل السيادي")
    st.caption("اكتب. ارفع. انقر. الباقي على الوكيل")

    domain = st.selectbox("المجال", ["العقار", "التجارة", "المطاعم", "التعليم", "الصحة"])
    task = st.text_area("وصف المهمة", placeholder="فيلا 220م R+1 القلعة", height=120)
    imgs = st.file_uploader("🖼️ صور مرجعية", accept_multiple_files=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 شغّل الوكيل الكامل", type="primary", use_container_width=True):
            if task:
                with st.spinner("الوكيل يخدم: Groq + Drive + Sheet + Maps..."):
                    res = OMEGA_SOA().execute_mission(task, domain, imgs)
                    st.success("تمت المهمة")
                    st.write(res["summary"][:1000])
                    st.markdown(f"📍 [الخريطة]({res['maps_link']}) | 📁 [Drive]({res['drive_link']}) | 📊 [CRM]({res['sheet_link']})")
                    st.download_button("📄 PDF", res["pdf_bytes"], "OMEGA.pdf")
    with col2:
        wa_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER","")
        st.link_button("📲 واتساب", f"https://wa.me/{wa_num}", use_container_width=True)

with tab2:
    st.title("🎙️ تفريغ صوتي Whisper V3")
    client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
    audio = st.file_uploader("ارفع صوت/فيديو")
    if audio and st.button("🚀 فرّغ"):
        with tempfile.NamedTemporaryFile(delete=False) as tmp: tmp.write(audio.getvalue())
        text = client.audio.transcriptions.create(file=(audio.name, open(tmp.name,"rb")), model="whisper-large-v3", language="ar").text
        st.text_area("النص", text, height=200)
        if st.button("🚀 شغّل الوكيل على هذا النص"): st.session_state['t_area'] = text; st.rerun()
