import streamlit as st
import requests

def call_meta_ai(prompt, agent_name):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("META_API_KEY", "")
    
    if not api_key:
        return "❌ خطأ: مفتاح META_API_KEY غير موجود في إعدادات Secrets."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    domaine = st.session_state.get('domaine', 'العقار والتسويق الرقمي')
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system", 
                "content": f"You are {agent_name}, an expert AI agent specialized in {domaine} powered by Meta Llama. Respond professionally in Moroccan Arabic Darija and clear Arabic, utilizing bullet points and emojis."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال: {e}"

def send_whatsapp_alert(message):
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')
        
        if not all([phone_id, access_token, target_number]):
            return
            
        url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": message}
        }
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass

class OmegaAgent:
    def __init__(self, domaine="العقار"):
        st.session_state.domaine = domaine
        self.domaine = domaine

    def ceo(self, task):
        return call_meta_ai(f"ضع خطة استراتيجية تسويقية دقيقة بناءً على هذا الطلب: {task}", "Meta CEO")

    def cto(self, task):
        return call_meta_ai(f"اقترح استراتيجية تقنية واستهداف إعلاني دقيق بناءً على هذا الطلب: {task}", "Meta CTO")

    def coo(self, task):
        return call_meta_ai(f"ضع خطة تنفيذية، ميزانية، وجدولة زمنية بناءً على هذا الطلب: {task}", "Meta COO")

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة: {plan}. اكتب إعلانات فيسبوك احترافية ومنظمة بالأيقونات والكلمات المفتاحية والهاشتاقات باللهجة المغربية واللغة العربية مع رقم الواتساب: {whatsapp_num}"
        ad = call_meta_ai(prompt, "Meta Copywriter")
        send_whatsapp_alert(f"👑 OMEGA AGENTIC v3.0 - إعلان جديد:\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين صيغة هذا الإعلان وجعله أكثر إقناعاً مع خلق شعور بالاستعجال (FOMO) لزيادة المبيعات: {ad}"
        return call_meta_ai(prompt, "Meta Closer")
