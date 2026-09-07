from datetime import datetime
import io, tempfile, requests
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="OMEGA SOA", page_icon="👑", layout="centered")

# ===== 1. تهيئة FIREBASE - نفس المشروع ديال JS =====
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred, {
            'storageBucket': "gen-lang-client-0604383893.appspot.com" # نفس bucket
        })
    return firestore.client(), storage.bucket()

db, bucket = init_firebase()

# ===== 2. دوال Groq =====
def call_super_ai(prompt, agent_name, domain):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system_prompt = f"You are {agent_name} for '{domain}'. Respond in Moroccan Darija + العربية. Bullets + tables + emojis."
    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role":"system","content":system_prompt},{"role":"user","content":prompt}], "temperature": 0.75}
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=90)
    return res.json()["choices"][0]["message"]["content"]

# ===== 3. OMEGA SOA + FIRESTORE =====
class OMEGA_SOA:
    def execute_mission(self, task, domain, images):
        brain_output = call_super_ai(f"ضع خطة شاملة لمشروع {domain}: {task}. SWOT + خطة 90 يوم", "Super CEO", domain)
        full_report = f"# OMEGA REPORT\n{brain_output}"
        pdf_bytes = self._generate_pdf(full_report)

        # 1. الرفع لـ Firebase Storage
        storage_path = f"omega_plans/{datetime.now().strftime('%Y%m%d_%H%M')}_Offer.pdf"
        blob = bucket.blob(storage_path)
        blob.upload_from_string(pdf_bytes, content_type='application/pdf')
        storage_link = f"https://storage.googleapis.com/{bucket.name}/{storage_path}"

        # 2. الحفظ فـ Firestore - نفس collection ديال JS
        doc_ref = db.collection("omega_plans").document()
        doc_ref.set({
            "userId": "soa_admin", # ولا خليه فاضي
            "plan": {"title": task, "advice": brain_output},
            "pdf_url": storage_link,
            "createdAt": datetime.now(),
        })

        return {"summary": full_report, "pdf_bytes": pdf_bytes, "storage_link": storage_link}

    def _generate_pdf(self, text):
        buffer = io.BytesIO(); c = canvas.Canvas(buffer, pagesize=letter); c.setFont("Helvetica", 9); y = 750
        for line in text.encode('latin-1', 'replace').decode('latin-1').split("\n"):
            c.drawString(50, y, line[:100]); y -= 14;
            if y < 50: c.showPage(); y = 750
        c.save(); buffer.seek(0); return buffer.getvalue()

# ===== 4. الواجهة =====
omega = OMEGA_SOA()
st.title("👑 OMEGA SOA + FIREBASE")
domain = st.selectbox("المجال", ["العقار", "التجارة"])
task = st.text_area("وصف المهمة", placeholder="فيلا 220م R+1 القلعة")

if st.button("🚀 شغّل الوكيل الكامل", type="primary"):
    if task:
        with st.spinner("الوكيل يخدم: Groq + Firebase..."):
            res = omega.execute_mission(task, domain, None)
            st.success("✅ تم الحفظ فـ Firestore")
            st.text_area("الملخص", res["summary"], height=300)
            st.markdown(f"📁 [رابط PDF]({res['storage_link']})")
            st.download_button("📄 تحميل PDF", res["pdf_bytes"], "OMEGA.pdf")
