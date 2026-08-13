import streamlit as st
from supabase import create_client
import schedule, time, threading, random, json, os
from datetime import datetime

st.set_page_config(page_title="👑 Meta Tassaout - Sovereign Free AI", layout="wide")

# ================== 1. الإعدادات السيادية ==================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
CTA_OFFICIEL = "212691897126"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
CITIES = ["قلعة السراغنة", "مراكش", "بني ملال", "الدار البيضاء", "أكادير", "طاطا"]
SECTORS = ["العقار", "الفلاحة", "الاستثمار", "التجارة", "مواد البناء"]

# ================== 2. 🧠 العقل المحلي ==================
def local_ai_generate(prompt):
    sector = random.choice(SECTORS)
    city = random.choice(CITIES)
    opportunities = [
        f"فرصة استثمارية ذهبية في قطاع {sector} بمدينة {city} مع عوائد عالية.",
        f"أرض عقارية متميزة صالحة للبناء والتطوير بقلعة السراغنة وضواحيها.",
        f"كمية كبيرة من مواد البناء متوفرة الآن للتوصيل لـ {city}"
    ]
    predictions = [
        "السوق نشط جداً ومؤشرات النمو تصاعدية.",
        "الطلب مرتفع والفرصة محدودة الوقت، سارع بالحجز.",
        "استثمار آمن بفضل الديناميكية الاقتصادية المحلية."
    ]
    return json.dumps({
        "sector": sector, "city": city,
        "opportunity": random.choice(opportunities),
        "prediction": random.choice(predictions)
    }, ensure_ascii=False)

def super_brain():
    ai_json = local_ai_generate("")
    try: data = json.loads(ai_json)
    except: data = {"sector": "عام", "city": "المغرب", "opportunity": "فرصة جديدة", "prediction": "السوق نشط"}

    return f"""👑 *Meta Tassaout - تنبيه سيادي*
🏙️ *المدينة*: {data['city']} | 📊 *القطاع*: {data['sector']}
🎯 *الفرصة*: {data['opportunity']}
📈 *التحليل*: {data['prediction']}
📞 للطلب: {CTA_OFFICIEL}
*العقل الذكي، الأرض الحقيقية*"""

def send_whatsapp_reply(phone, message):
    st.info(f"[محاكاة] إرسال إلى {phone}")

def autonomous_agent():
    opportunity = super_brain()
    supabase.table("instant_ads").insert({"content": opportunity, "created_at": datetime.now().isoformat()}).execute()
    leads = supabase.table("leads").select("phone").execute().data or []
    for lead in leads[:20]:
        send_whatsapp_reply(lead['phone'], opportunity)
        time.sleep(1)

def run_scheduler():
    schedule.every(30).minutes.do(autonomous_agent)
    while True: 
        schedule.run_pending()
        time.sleep(60)

# ================== 3. تشغيل الجدولة فقط ==================
if 'services_started' not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    st.session_state.services_started = True

# ================== 4. الواجهة ==================
st.title("👑 Meta Tassaout - Free Sovereign AI")
col1, col2 = st.columns(2)
col1.metric("Scheduler", "🟢 ON")
col2.metric("Local Brain", "🟢 ON")

st.warning("⚠️ الـ Webhook ديال WhatsApp خاصو يترفع فـ Render منفصل. هنا غير المحاكي.")

st.divider()
if st.button("🚀 تشغيل ضربة سيادية الآن", use_container_width=True):
    with st.spinner("العقل السيادي يولد الفرصة..."):
        result = super_brain()
        st.code(result, language="markdown")
        supabase.table("instant_ads").insert({"content": result, "created_at": datetime.now().isoformat()}).execute()
        st.success("تم الحفظ في Supabase بنجاح!")
