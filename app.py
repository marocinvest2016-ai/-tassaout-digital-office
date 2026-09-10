import streamlit as st
import requests
import json

st.set_page_config(page_title="Tassaout Omega AI - Multi-Domain", page_icon="👑", layout="wide")

def call_ai_engine(prompt, agent_role, domain_field):
    """محرك موحد ومستقر كليا لا يتأثر بتغيير الموديلات"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في الـ Secrets."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_role}, an elite multi-domain expert in '{domain_field}'. "
        f"Provide professional, highly structured, and actionable business strategies. "
        f"Respond clearly in Moroccan Arabic Darija mixed with professional Modern Standard Arabic, using bullet points, emojis, and clear executive formatting."
    )

    payload = {
        "model": "llama3-8b-8192",  # الموديل الثابت والمستقر الكلاسيكي الذي لا يتغير
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"❌ خطأ من الخادم (كود {res.status_code}): {res.text}"
    except Exception as e:
        return f"❌ خطأ في الاتصال: {e}"

def push_to_whatsapp(message_text):
    """إرسال النتيجة المباشرة إلى الواتساب بضغطة زر"""
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

        if not all([phone_id, access_token, target_number]):
            return False, "معلومات واتساب ناقصة في الـ Secrets"

        url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": message_text[:4096]}
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        return r.status_code == 200, r.text
    except Exception as err:
        return False, str(err)

# ===== واجهة المستخدم المتكاملة =====
st.title("👑 Tassaout Omega - Multi-Domain Agentic System")
st.caption("نظام ذكي متكامل لإدارة المشاريع، العقار، والتجارة وإرسال التقارير للواتساب فوراً")

# إعدادات المجال والمهمة
col1, col2 = st.columns(2)
with col1:
    domain = st.text_input("مجال النشاط / القطاع", value="العقار وتجزئة الأراضي بقلعة السراغنة")
with col2:
    agent_type = st.selectbox("اختر الوكيل الذكي", [
        "CEO (الاستراتيجية والتخطيط الشامل)",
        "CTO (البنية التقنية والحلول الرقمية)",
        "COO (إدارة العمليات والجدولة)",
        "Copywriter & Closer (صياغة الإعلانات والمبيعات)"
    ])

task_input = st.text_area("أدخل تفاصيل المهمة أو المشروع:", placeholder="مثال: تسويق بقع أرضية تجارية واستقطاب المستثمرين...")

if st.button("🚀 تنفيذ المهمة وتوليد الاستراتيجية"):
    if not task_input.strip():
        st.warning("المرجو إدخال وصف المهمة أولاً.")
    else:
        with st.spinner("جاري معالجة المهمة بالذكاء الاصطناعي..."):
            # توجيه المهمة حسب الوكيل المختار
            role_name = agent_type.split(" ")[0]
            result = call_ai_engine(task_input, role_name, domain)
            
            st.session_state['last_result'] = result
            st.success("تم توليد النتيجة بنجاح!")
            st.markdown(result)

# زر إرسال سريع للواتساب إذا كانت هناك نتيجة جاهزة
if 'last_result' in st.session_state:
    st.markdown("---")
    if st.button("📱 إرسال هذه النتيجة فوراً إلى واتساب الأعمال"):
        with st.spinner("جاري الإرسال عبر WhatsApp API..."):
            success, info = push_to_whatsapp(f"👑 *Tassaout Omega Report*\n*المجال:* {domain}\n\n{st.session_state['last_result']}")
            if success:
                st.success("تم إرسال التقرير إلى الواتساب بنجاح!")
            else:
                st.error(f"فشل الإرسال: {info}")
