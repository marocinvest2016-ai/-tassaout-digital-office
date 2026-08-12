import streamlit as st
from supabase import create_client
import subprocess, requests, schedule, time, threading, random, json, os, re
from datetime import datetime
from flask import Flask, request, jsonify

st.set_page_config(page_title="👑 Meta Tassaout - Super AI", layout="wide")

# ================== 1. الإعدادات السيادية ==================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
META_TOKEN = os.getenv("META_TOKEN")
VERIFY_TOKEN = "meta_tassaout_secure_token"
CTA_OFFICIEL = "212691897126"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
CITIES = ["قلعة السراغنة", "مراكش", "بني ملال", "الدار البيضاء"]
SECTORS = ["العقار", "الفلاحة", "الاستثمار", "التجارة"]

# تسجيل meta cli مرة وحدة فقط
if 'meta_logged' not in st.session_state:
    if META_TOKEN:
        subprocess.run(["meta", "login", "--token", META_TOKEN], capture_output=True)
    st.session_state.meta_logged = True

# ================== 2. 🧠 العقل + الوكيل ==================
def meta_generate(prompt):
    result = subprocess.run(["meta", "generate", prompt], capture_output=True, text=True, timeout=90)
    # تنظيف الـ JSON من أي نص زائد
    clean = re.search(r'\{.*\}', result.stdout, re.DOTALL)
    return clean.group(0) if clean else result.stdout.strip()

def meta_search(query):
    return subprocess.run(["meta", "search", query], capture_output=True, text=True, timeout=40).stdout.strip()

def super_brain():
    sector, city = random.choice(SECTORS), random.choice(CITIES)
    search_data = meta_search(f"آخر أخبار {sector} في {city} المغرب 2026")
    prompt = f"""أنت Meta Tassaout. "العقل الذكي، الأرض الحقيقية". البيانات: {search_data}.
    أعطني فرصة استثمارية واحدة في قطاع {sector} بمدينة {city}.
    رد JSON فقط بهذا الشكل: {{"sector": "...", "city": "...", "opportunity": "...", "prediction": "..."}}"""

    ai_json = meta_generate(prompt)
    try: data = json.loads(ai_json)
    except: data = {"sector": sector, "city": city, "opportunity": f"فرصة جديدة في {sector}", "prediction": "السوق نشط حاليا"}

    return f"""👑 *Meta Tassaout - تنبيه سيادي*
🏙️ *المدينة*: {data['city']} | 📊 *القطاع*: {data['sector']}
🎯 *الفرصة*: {data['opportunity']}
📈 *التحليل*: {data['prediction']}
📞 {CTA_OFFICIEL}
*العقل الذكي، الأرض الحقيقية*"""

def send_whatsapp_reply(phone, message):
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": message}}
    try: requests.post(url, headers=headers, json=payload, timeout=30)
    except Exception as e: st.error(f"خطأ الإرسال: {e}")

def autonomous_agent():
    opportunity = super_brain()
    supabase.table("instant_ads").insert({"content": opportunity, "created_at": datetime.now().isoformat()}).execute()
    leads = supabase.table("leads").select("phone").execute().data or []
    for lead in leads[:50]:
        send_whatsapp_reply(lead['phone'], opportunity)
        time.sleep(5)

def run_scheduler():
    schedule.every(30).minutes.do(autonomous_agent)
    while True: schedule.run_pending(); time.sleep(60)

# ================== 3. 🕸️ WEBHOOK FLASK ==================
app_webhook = Flask(__name__)

@app_webhook.route("/webhook", methods=["GET"])
def verify_webhook():
    mode, token, challenge = request.args.get("hub.mode"), request.args.get("hub.verify_token"), request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

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

                        prompt = f"أنت Meta Tassaout وكيل عقاري من قلعة السراغنة. العميل قال: {msg_body}. رد عليه بالدارجة المغربية قصير جدا، احترافي، وختمه برقم {CTA_OFFICIEL}. لا تذكر أنك AI."
                        reply_text = meta_generate(prompt)
                        send_whatsapp_reply(sender_phone, reply_text)
            return jsonify({"status": "EVENT_RECEIVED"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"status": "OK"}), 200

# تشغيل Flask + Scheduler مع Streamlit
if 'services_started' not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    threading.Thread(target=lambda: app_webhook.run(host='0.0.0.0', port=5000), daemon=True).start()
    st.session_state.services_started = True

# ================== 4. الواجهة ==================
st.title("👑 Meta Tassaout - Super Multidomaine Agentic AI")
col1, col2, col3 = st.columns(3)
col1.metric("Webhook", "🟢 ON")
col2.metric("Scheduler", "🟢 ON")
col3.metric("Muse Spark", "🟢 ON")

if st.button("🚀 تشغيل ضربة سيادية الآن", width='stretch'):
    with st.spinner("Muse Spark يفكر ويبحث..."):
        st.code(super_brain())
