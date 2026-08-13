import streamlit as st
from supabase import create_client
import schedule, time, threading, requests
from datetime import datetime
from bs4 import BeautifulSoup
from fpdf import FPDF

st.set_page_config(page_title="👑 Meta Tassaout - الوكيل السيادي", layout="wide")

# ====== 1. السيكريتس - غير Supabase ======
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except:
    st.error("⚠️ عَمّر SUPABASE_URL و SUPABASE_KEY فـ Settings > Secrets")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ====== 2. الإعدادات اليدوية للواتساب ======
with st.sidebar:
    st.header("⚙️ إعدادات الواتساب")
    WHATSAPP_TOKEN = st.text_input("Token الواتساب", type="password", placeholder="EAAxxx")
    WHATSAPP_PHONE_ID = st.text_input("Phone ID", placeholder="123456789")
    ADMIN_PHONE = st.text_input("نمرتك", value="212691897126")
    st.success("عمرهم مرة وحدة")

# ====== 3. وظائف النظام ======
def envoyer_au_admin(msg):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        st.toast("⚠️ عمر Token و Phone ID فالسايدبار")
        return
    try:
        phone = ADMIN_PHONE.replace("+", "").replace(" ", "")
        url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": msg}}
        requests.post(url, headers=headers, json=data, timeout=20)
    except Exception as e: st.error(f"خطأ واتساب: {e}")

def robot_cherche_partout():
    nouvelles_alerts = 0
    try:
        r = requests.get("https://www.marchespublics.gov.ma/pmmp/recherche/recherAvis.do", params={"mode": "rechercheSimple", "motsCles": "اسمنت بناء توريد"}, timeout=20)
        soup = BeautifulSoup(r.content, 'lxml')
        for row in soup.find_all("tr", class_="ligneResultat")[:5]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                titre = cols[2].text.strip(); acheteur = cols[3].text.strip(); delai = cols[4].text.strip()
                check = supabase.table("instant_ads").select("id").eq("content", titre).execute().data
                if not check:
                    message = f"🏛️ *فرصة جديدة تلقائية*\n📋 {titre}\n🏢 {acheteur}\n⏳ {delai}"
                    supabase.table("instant_ads").insert({"content": titre, "message": message, "source": acheteur}).execute()
                    envoyer_au_admin(message)
                    nouvelles_alerts += 1
    except Exception as e: st.error(f"خطأ: {e}")
    return nouvelles_alerts

# ====== 4. المجدول التلقائي كل ساعة ======
def tache_autonome(): robot_cherche_partout()

if 'scheduler_started' not in st.session_state:
    schedule.every(1).hours.do(tache_autonome)
    threading.Thread(target=lambda: [schedule.run_pending() or time.sleep(60) for _ in iter(int, 1)], daemon=True).start()
    st.session_state.scheduler_started = True

# ====== 5. الواجهة ======
st.title("👑 Meta Tassaout - المكتب السيادي")
st.metric("الحالة", "🟢 مراقبة تلقائية كل ساعة")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 مسح يدوي الآن", use_container_width=True, type="primary"):
        with st.spinner("العنكبوت كيقلب..."):
            count = robot_cherche_partout()
            if count > 0: st.success(f"✅ تم تخزين {count} فرص جديدة")
            else: st.info("لا توجد فرص جديدة")
with col2:
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(200, 10, "BC - SRAGHNA DIGITAL", ln=1, align='C')
    st.download_button("🧾 تحميل BC PDF", bytes(pdf.output()), "BC.pdf", use_container_width=True)

st.divider()
st.subheader("🤖 الوكيل الذكي")
user_query = st.text_input("أمر للوكيل", placeholder="اعطيني صفقات مراكش")
if st.button("تنفيد الأمر"):
    villes = ["بني ملال", "مراكش", "قلعة السراغنة", "أكادير", "الدار البيضاء", "الرباط"]
    city = next((v for v in villes if v in user_query), None)
    if city:
        res = supabase.table("instant_ads").select("*").ilike("message", f"%{city}%").order("created_at", desc=True).limit(5).execute().data
        if res:
            for r in res:
                with st.container(border=True):
                    st.markdown(r['message'])
                    if st.button("📲 صيفطها ليا", key=r['id']): envoyer_au_admin(r['message'])
        else: st.warning(f"ما كاين والو في {city}")
