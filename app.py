import streamlit as st
from supabase import create_client
import schedule, time, threading, random, json, os
from datetime import datetime
from flask import Flask, request, jsonify

st.set_page_config(page_title="👑 Meta Tassaout - Sovereign Free AI", layout="wide")

# ================== 1. الإعدادات السيادية المحلية ==================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CTA_OFFICIEL = "212691897126"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
CITIES = ["قلعة السراغنة", "مراكش", "بني ملال", "الدار البيضاء"]
SECTORS = ["العقار", "الفلاحة", "الاستثمار", "التجارة"]

# ================== 2. 🧠 العقل المحلي المباشر ==================
def local_ai_generate(prompt):
    # مولد ذكي محلي بالكامل بدون الحاجة لأي API خارجي أو توكن
    sector = random.choice(SECTORS)
    city = random.choice(CITIES)
    opportunities = [
        f"فرصة استثمارية ذهبية في قطاع {sector} بمدينة {city} مع عوائد عالية.",
        f"أرض عقارية متميزة صالحة للبناء والتطوير بقلعة السراغنة وضواحيها.",
        f"مشروع تجاري ناشط ومطلوب بشدة في سوق {city} حالياً."
    ]
    predictions = [
        "السوق نشط جداً ومؤشرات النمو تصاعدية خلال هذه الفترة.",
        "الطلب مرتفع والفرصة محدودة الوقت، سارع بالحجز.",
        "استثمار آمن ومضمون بفضل الديناميكية الاقتصادية المحلية."
    ]
    return json.dumps({
        "sector": sector,
        "city": city,
        "opportunity": random.choice(opportunities),
        "prediction": random.choice(predictions)
    }, ensure_ascii=False)

def super_brain():
    sector, city = random.choice(SECTORS), random.choice(CITIES)
    ai_json = local_ai_generate(f"فرصة في {sector} بـ {city}")
    try: 
        data = json.loads(ai_json)
    except: 
        data = {"sector": sector, "city": city, "opportunity": f"فرصة جديدة في {sector}", "prediction": "السوق نشط حاليا"}

    return f"""👑 *Meta Tassaout - تنبيه سيادي*
🏙️ *المدينة*: {data['city']} | 📊 *القطاع*: {data['sector']}
🎯 *الفرصة*: {data['opportunity']}
📈 *التحليل*: {data['prediction']}
📞 {CTA_OFFICIEL}
*العقل الذكي، الأرض الحقيقية*"""

def send_whatsapp_reply(phone, message):
    # محاكاة الإرسال أو الربط المباشر الداخلي
    print(f"Sending to {phone}: {message}")

def autonomous_agent():
    opportunity = super_brain()
    supabase.table("instant_ads").insert({"content": opportunity, "created_at": datetime.now().isoformat()}).execute()
    leads = supabase.table("leads").select("phone").execute().data or []
    for lead in leads[:50]:
        send_whatsapp_reply(lead['phone'], opportunity)
        time.sleep(2)

def run_scheduler():
    schedule.every(30).minutes.do(autonomous_agent)
    while True: 
        schedule.run_pending()
        time.sleep(60)

# ================== 3. 🕸️ WEBHOOK FLASK ==================
app_webhook = Flask(__name__)

@app_webhook.route("/webhook", methods=["GET"])
def verify_webhook():
    return "OK", 200

@app_webhook.route("/webhook", methods=["POST"])
def handle_whatsapp_message():
    body = request.get_json()
    try:
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    messages = change.get("value", {}).get("messages", [])
                    if messages:
                        msg = messages[0]
                        sender_phone = msg.get("from")
                        msg_body = msg.get("text", {}).get("body", "")

                        supabase.table("inbox").insert({"phone": sender_phone, "message": msg_body, "timestamp": datetime.now().isoformat()}).execute()
                        
                        reply_text = f"أهلاً بك في مكتب تساوت الرقمي. تم استلام رسالتك: '{msg_body}'. تواصل معنا مباشرة على الرقم: {CTA_OFFICIEL}"
                        send_whatsapp_reply(sender_phone, reply_text)
            return jsonify({"status": "EVENT_RECEIVED"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"status": "OK"}), 200

# تشغيل الخدمات بالتوازي
if 'services_started' not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    threading.Thread(target=lambda: app_webhook.run(host='0.0.0.0', port=5000), daemon=True).start()
    st.session_state.services_started = True

# ================== 4. الواجهة ==================
st.title("👑 Meta Tassaout - Free Sovereign AI")
col1, col2, col3 = st.columns(3)
col1.metric("Webhook", "🟢 ON")
col2.metric("Scheduler", "🟢 ON")
col3.metric("Local Brain", "🟢 ON")

if st.button("🚀 تشغيل ضربة سيادية الآن", use_container_width=True):
    with st.spinner("العقل السيادي يولد الفرصة..."):
        st.code(super_brain())
