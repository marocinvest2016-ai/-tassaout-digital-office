import streamlit as st
from supabase import create_client
import time, requests
from datetime import datetime
from bs4 import BeautifulSoup
from fpdf import FPDF

# إعداد الصفحة
st.set_page_config(page_title="👑 Meta Tassaout - الوكيل السيادي", layout="wide")

# ====== 1. السيكريتس ======
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    WHATSAPP_TOKEN = st.secrets.get("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID = st.secrets.get("WHATSAPP_PHONE_ID", "")
    ADMIN_PHONE = st.secrets.get("ADMIN_PHONE", "212691897126")
except:
    st.error("⚠️ عَمّر السيكريتس فـ Settings > Secrets")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ====== 2. وظائف النظام ======
def envoyer_au_admin(msg):
    if not WHATSAPP_TOKEN: return
    try:
        phone = ADMIN_PHONE.replace("+", "").replace(" ", "")
        url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        data = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": msg}}
        requests.post(url, headers=headers, json=data, timeout=20)
    except Exception as e: print(f"خطأ واتساب: {e}")

def robot_cherche_partout():
    nouvelles_alerts = 0
    try:
        r = requests.get("https://www.marchespublics.gov.ma/pmmp/recherche/recherAvis.do", params={"mode": "rechercheSimple", "motsCles": "اسمنت بناء توريد"}, timeout=15)
        soup = BeautifulSoup(r.content, 'lxml')
        for row in soup.find_all("tr", class_="ligneResultat")[:5]:
            cols = row.find_all("td")
            if len(cols) >= 5:
                titre = cols[2].text.strip(); acheteur = cols[3].text.strip(); delai = cols[4].text.strip()
                check = supabase.table("instant_ads").select("id").eq("content", titre).execute().data
                if not check:
                    alert = {"content": titre, "message": f"🏛️ *فرصة جديدة*\n📋 {titre}\n🏢 {acheteur}\n⏳ {delai}\n📍 {acheteur}", "source": acheteur, "created_at": datetime.now().isoformat()}
                    supabase.table("instant_ads").insert(alert).execute()
                    envoyer_au_admin(alert['message'])
                    nouvelles_alerts += 1
    except Exception as e: st.error(f"خطأ: {e}")
    return nouvelles_alerts

# ====== 3. الواجهة الرئيسية ======
st.title("👑 Meta Tassaout - المكتب السيادي")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 مسح شامل الآن", use_container_width=True, type="primary"):
        with st.spinner("العنكبوت كيقلب..."):
            count = robot_cherche_partout()
            st.success(f"✅ تم العثور وتخزين {count} فرص جديدة") if count > 0 else st.info("لا توجد فرص جديدة")
with col2:
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(200, 10, "BC - SRAGHNA DIGITAL", ln=1, align='C')
    st.download_button("🧾 تحميل BC PDF", bytes(pdf.output()), "BC.pdf", "application/pdf", use_container_width=True)

st.divider()

# ====== 4. 🧠 الوكيل التفاعلي ======
st.subheader("🤖 تواصل مع الوكيل الذكي")
user_query = st.text_input("أمر للوكيل", placeholder="مثال: اعطيني صفقات جهة مراكش او قلعة السراغنة")

if st.button("تنفيد الأمر", use_container_width=True):
    if user_query:
        with st.spinner("الوكيل كيبحث..."):
            villes = ["بني ملال", "مراكش", "قلعة السراغنة", "أكادير", "الدار البيضاء", "الرباط", "طنجة", "فاس"]
            city_keyword = next((v for v in villes if v in user_query), None)

            if city_keyword:
                results = supabase.table("instant_ads").select("*").ilike("message", f"%{city_keyword}%").order("created_at", desc=True).limit(10).execute().data
                if results:
                    st.success(f"لقيت ليك {len(results)} صفقة في {city_keyword}:")
                    for res in results:
                        with st.container(border=True):
                            st.markdown(res['message'])
                            if st.button("📲 صيفطها ليا فواتساب", key=res['id']):
                                envoyer_au_admin(res['message'])
                                st.toast("تم الارسال")
                else:
                    st.warning(f"ما لقيت حتى صفقة في {city_keyword} حالياً.")
            else:
                st.error("الوكيل ما عرفش المنطقة. جرب: مراكش، بني ملال، قلعة السراغنة")

st.divider()
st.subheader("📊 اخر 10 فرص مخزنة")
try:
    ads = supabase.table("instant_ads").select("message").order("created_at", desc=True).limit(10).execute().data
    if ads: [st.code(ad['message']) for ad in ads]
except: st.info("مازال ما كاين والو")
