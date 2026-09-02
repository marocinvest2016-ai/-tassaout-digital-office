# ==============================================================================
# app.py - OMEGA AGENTIC SUPER AI with Groq & WhatsApp Integration
# SEAU: TASSAOUT VISION VERIFIED © 2026 | BORDEAUX #800020 & GOLD #D4AF37
# ==============================================================================

import streamlit as st
from groq import Groq
import requests
import json

st.set_page_config(page_title="OMEGA AGENTIC AI", page_icon="👑", layout="wide")
st.markdown('<h1 style="text-align:center;color:#800020;">👑 OMEGA AGENTIC SUPER AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#D4AF37;">Multi-Domaine + WHATSAPP AUTO | TASSAOUT & ATIS</p>', unsafe_allow_html=True)
st.markdown("---")

# قراءة المفاتيح من Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
WHATSAPP_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

# تهيئة عميل Groq
if not GROQ_API_KEY:
    st.error("⚠️ تنبيه: مفتاح GROQ_API_KEY غير موجود في إعدادات الأسرار (Secrets).")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

def call_agent(role, task):
    """دالة ذكية تتنقل بين النماذج تلقائياً لضمان عدم توقف التطبيق نهائياً"""
    system_prompt = f"You are {role}. Expert for TASSAOUT & ATIS in Morocco. Respond in Moroccan Arabic with professional emojis."
    
    # قائمة النماذج المرتبة حسب الأولوية للاحتياط التلقائي
    models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    for model_name in models_to_try:
        try:
            res = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": task}],
                temperature=0.7, 
                max_tokens=1000
            )
            return res.choices[0].message.content
        except Exception:
            continue # الانتقال تلقائياً للنموذج الموالي في حال حدوث أي خطأ
            
    return f"⚠️ خطأ في الاتصال بـ Groq API للوكيل {role}. تحقق من المفتاح."

def send_whatsapp(to_number, message):
    """دالة إرسال الواتساب عبر Meta Cloud API"""
    url = f"https://graph.facebook.com/{WHATSAPP_VERSION}/{WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return True, res.json()
        else:
            return False, res.json()
    except Exception as e:
        return False, str(e)

# القائمة الجانبية للواجهة
st.sidebar.markdown("### 🏛️ إعدادات محطة القيادة")
domaine = st.sidebar.selectbox("اختر المجال الرئيسي:", ["🏭 العقار", "🏗️ الهندسة والبناء", "🌐 التجارة الرقمية", "📚 التعليم", "🏥 الخدمات"])
send_to = st.sidebar.text_input("رقم الواتساب للإرسال:", value="212691897126", help="بدون علامة +. مثال: 212691897126")
st.sidebar.markdown("---")
st.sidebar.info("📞 الهاتف: +212691897126\n📧 marocinvest2012@gmail.com")

# الواجهة الرئيسية
st.markdown(f"### 🎯 المجال النشط: {domaine}")
user_task = st.text_area("أعطي المهمة للوكيل الذكي:", placeholder="مثال: تسويق وبيع شقق ممتازة بقلعة السراغنة مع توفير الدعم")

if st.button("⚡ فعل وكلاء OMEGA + إرسال واتساب"):
    if user_task.strip() == "":
        st.warning("المرجو إدخال تفاصيل المهمة أولاً.")
    else:
        with st.spinner("🤖 جاري تشغيل خلية الوكلاء الذكيين (CEO + Researcher + Copywriter)..."):

            # 1. المدير يخطط
            plan = call_agent("CEO Agent", f"Goal: {user_task}. Domaine: {domaine}. Create 3-step professional execution plan.")
            st.subheader("🧠 خطة المدير التنفيذي (CEO)")
            st.write(plan)

            # 2. الباحث يحلل السوق
            research = call_agent("Market Researcher", f"Based on plan: {plan}. Research and analyze target market for: {user_task}")
            st.subheader("🔍 تقرير استخبارات السوق")
            st.write(research)

            # 3. الكاتب يصيغ الإعلان النهائي
            ad_prompt = f"""Based on research: {research}. Write a powerful, attractive marketing ad with clear CTA in Moroccan Arabic. 
            Include contact info: الهاتف: +212691897126 | البريد: marocinvest2012@gmail.com"""
            ad = call_agent("Marketing Copywriter", ad_prompt)
            st.subheader("📢 الإعلان التسويقي النهائي")
            st.success(ad)

            # 4. إرسال واتساب تلقائي
            st.subheader("📲 تقرير إرسال واتساب التلقائي")
            if WHATSAPP_TOKEN and WHATSAPP_PHONE_ID:
                success, response = send_whatsapp(send_to, ad)
                if success:
                    st.success(f"✅ تم إرسال الإعلان بنجاح إلى الرقم: {send_to}")
                else:
                    st.error(f"❌ خطأ في إرسال الواتساب (تأكد من تجديد التوكن في Meta Secrets). التفاصيل: `{response}`")
            else:
                st.warning("⚠️ لم يتم ضبط رموز توكن واتساب في الأسرار (Secrets).")

            st.markdown("---")
            st.markdown("🌿 **[TASSAOUT & ATIS AGENTIC VERIFIED]** | ameur signature tassaout ai © 2026")

# تذييل الصفحة
st.markdown("---")
st.markdown("🌿 **[TASSAOUT & ATIS VERIFIED]** | ameur signature tassaout ai © 2026")
