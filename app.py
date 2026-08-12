import streamlit as st
from supabase import create_client
import subprocess
import json
import requests
import schedule
import time
import threading
from datetime import datetime
import googlemaps
import pandas as pd

st.set_page_config(page_title="👑 Meta Tassaout - Super Agentic AI", layout="wide")
st.markdown("""<style>.main{background-color:#0e1117;color:#fff}.omega{background:linear-gradient(90deg,#FFD700,#FF0000);padding:10px;border-radius:8px;color:black;font-weight:bold}</style>""", unsafe_allow_html=True)

# 1. الإعدادات السيادية
SUPABASE_URL = "https://xjjriuohqvhdxfgsyepl.supabase.co"
SUPABASE_KEY = "sb_publishable_xNbvcCGrqDQyU8fAtEMF7w_FqDzwSVg"
GOOGLE_MAPS_API_KEY = "ضع_API_KEY_هنا"
WHATSAPP_TOKEN = "ضع_التوكن_الدائم_هنا"
WHATSAPP_PHONE_ID = "ضع_PHONE_NUMBER_ID_هنا"

@st.cache_resource
def init_supabase(): return create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = init_supabase()
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# 2. 🧠 العقل التنبؤي V12 + Meta Tassaout + Search Grounding
def predictive_brain_meta_tassaout():
    search_prompt = "أعطني آخر الأخبار الاستثمارية والعقارية في قلعة السراغنة ومراكش اليوم"
    try:
        search_result = subprocess.run(
            ["meta", "search", search_prompt],
            capture_output=True, text=True, timeout=30
        ).stdout
    except:
        search_result = "تغطية ميدانية مستمرة في جهة قلعة السراغنة ومراكش"

    ai_prompt = f"""
    أنت Meta Tassaout، الوكيل السيادي الفائق للرصد العقاري والاستثماري في المغرب.
    بناءً على البيانات: {search_result}
    أعطني فرصة استثمارية حصرياً في قلعة السراغنة أو مراكش بصيغة JSON مفاتيحها:
    {{"city": "...", "sector": "...", "prediction": "...", "opportunity": "...", "growth_percent": 25}}
    """
    try:
        result = subprocess.run(["meta", "generate", ai_prompt], capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        return f"👑 *Meta Tassaout - تنبيه سيادي*\n\n📈 *التنبؤ*: {data.get('prediction', 'ارتفاع إيجابي في السوق')}\n🎯 *الفرصة*: {data.get('opportunity', 'أراضي استراتيجية')} في {data.get('city', 'قلعة السراغنة')}\n📊 *النمو*: +{data.get('growth_percent', 20)}%\n📞 0691897126\n*العقل الذكي، الأرض الحقيقية*"
    except:
        return "👑 *Meta Tassaout*\n\n📈 *التنبؤ*: قطاع العقار والفلاحة يعرف طلباً متزايداً.\n🎯 *الفرصة*: أراضي سكنية وفلاحية بمواقع استراتيجية بقلعة السراغنة.\n📞 0691897126\n*العقل الذكي، الأرض الحقيقية*"

# 3. 🗺️ الطبقة الجغرافية Google Maps
def get_geo_intel(city, query="عقارات وأراضي"):
    try:
        places = gmaps.places(query=query + " " + city)
        results = []
        for place in places.get('results', [])[:5]:
            results.append({
                "name": place.get('name'),
                "address": place.get('formatted_address'),
                "rating": place.get('rating', 'N/A'),
                "location": place['geometry']['location']
            })
        return results
    except:
        return []

# 4. إرسال WhatsApp
def send_whatsapp(to_number, message):
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": message}}
    try:
        requests.post(url, headers=headers, json=data, timeout=10)
    except:
        pass

# 5. الوكيل الذاتي 24/24 (التجربة الميدانية: قلعة السراغنة حصرياً)
def autonomous_agent():
    st.toast("🤖 Meta Tassaout يمسح السوق...", icon="⚡")
    prediction = predictive_brain_meta_tassaout()
    
    supabase.table("instant_ads").insert({
        "title": f"[META-TASSAOUT] {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": prediction,
        "created_at": datetime.now().isoformat()
    }).execute()
    
    # استهداف قلعة السراغنة حصرياً في المرحلة الأولى
    leads = supabase.table("leads").select("phone").eq("city", "قلعة السراغنة").execute().data or []
    for lead in leads:
        send_whatsapp(lead['phone'], prediction)
        time.sleep(3)

def run_scheduler():
    schedule.every(30).minutes.do(autonomous_agent)
    while True:
        schedule.run_pending()
        time.sleep(60)

if 'scheduler_started' not in st.session_state:
    threading.Thread(target=run_scheduler, daemon=True).start()
    st.session_state.scheduler_started = True

# الواجهة الرئيسية السيادية
st.markdown('<div class="omega">👑 META TASSAOUT — SUPER MULTIDOMAINE AGENTIC AI (ONLINE 24/24)</div>', unsafe_allow_html=True)
st.title("Meta Tassaout - مركز القيادة والسيادة الرقمية")

tab1, tab2, tab3, tab4 = st.tabs(["🧠 العقل التنبؤي (MetaAI)", "🗺️ الرصد الجغرافي (Maps)", "🚀 الحملة الميدانية", "📊 السجلات"])

with tab1:
    st.header("التنبؤ اللحظي مدعوم بـ Search Grounding")
    if st.button("🚀 توليد تحليل سيادي الآن"):
        intel = predictive_brain_meta_tassaout()
        st.success("تم التوليد بنجاح بالعقل الذكي:")
        st.code(intel)

with tab2:
    st.header("المسح الجغرافي الميداني (قلعة السراغنة ومراكش)")
    city_choice = st.selectbox("اختر المدينة للمسح", ["قلعة السراغنة", "مراكش", "بني ملال", "الدار البيضاء"])
    if st.button("🔍 تنفيذ المسح المكاني"):
        geo_data = get_geo_intel(city_choice)
        if geo_data:
            st.map(pd.DataFrame([r['location'] for r in geo_data]))
            for r in geo_data:
                st.info(f"**{r['name']}**\n{r['address']} | ⭐ {r['rating']}")
        else:
            st.warning("تأكد من إدخال مفتاح Google Maps API الصحيح.")

with tab3:
    st.header("إدارة الحملات الميدانية (قلعة السراغنة حصرياً)")
    st.info("المرحلة التجريبية الأولى مركزة حصرياً على قلعة السراغنة لاختبار سرعة الاستجابة.")
    if st.button("⚡ إطلاق الحملة التجريبية يدوياً الآن"):
        autonomous_agent()
        st.success("تم إرسال الضربات الأولى للعملاء بنجاح!")

with tab4:
    st.header("سجل العمليات والسيادة")
    df = pd.DataFrame(supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(20).execute().data or [])
    if not df.empty:
        st.dataframe(df[['title', 'created_at']], use_container_width=True)
    else:
        st.info("الوكيل الذاتي يعمل في الخلفية...")
