import streamlit as st
import requests

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق متعدد المجالات"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("META_API_KEY", "")
    
    if not api_key:
        return "❌ خطأ: مفتاح META_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Meta Llama. "
        f"Analyze the user request deeply and provide professional, highly tailored, actionable strategies, "
        f"marketing plans, or technical steps. Respond in Moroccan Arabic Darija and clear Arabic, utilizing professional formatting, bullet points, and emojis."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.75,
        "max_tokens": 1500
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {e}"

def send_whatsapp_alert(message):
    """إرسال إشعار مباشر عبر واتساب"""
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

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        return call_super_ai(f"ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}", "Super CEO Agent", self.domain)

    def cto(self, task):
        return call_super_ai(f"اقترح الاستراتيجية التقنية، أدوات التشغيل، واستهداف الجمهور الرقمي لـ: {task}", "Super CTO Agent", self.domain)

    def coo(self, task):
        return call_super_ai(f"ضع خطة تنفيذية، إدارة الموارد، وجدولة زمنية دقيقة لـ: {task}", "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = f"بناءً على هذه الخطة الاستراتيجية: {plan}. اكتب 3 إعلانات تسويقية جذابة ومنظمة بالأيقونات والكلمات المفتاحية والهاشتاقات باللهجة المغربية والعربية الفصحى مع دعوة للاتصال برقم الواتساب: {whatsapp_num}"
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        send_whatsapp_alert(f"👑 OMEGA SUPER AGENTIC v4.0\nمهمة جديدة في مجال: {self.domain}\n\n{ad}")
        return ad

    def closer(self, ad):
        prompt = f"قم بتحسين نص هذا الإعلان وإضافة محفزات الاستعجال (FOMO) لزيادة المبيعات ومعدل التحويل: {ad}"
        return call_super_ai(prompt, "Super Closer Agent", self.domain)
