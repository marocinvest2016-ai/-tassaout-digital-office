import streamlit as st
import requests
import google.generativeai as genai
import os

# ==========================================
# 🚀 1. نظام وكلاء OMEGA (عبر Groq / Meta Llama API)
# ==========================================

def call_meta_ai(prompt, agent_name):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets.get('META_API_KEY', '')}",
        "Content-Type": "application/json"
    }
    
    domaine = st.session_state.get('domaine', 'General Business')
    payload = {
        "model": "meta-llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": f"You are {agent_name} from Meta AI. Expert in {domaine}. Respond in Moroccan Arabic Darija with bullet points and emojis."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 1500
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ من Meta AI: {e}"

def send_whatsapp_meta(message):
    try:
        url = f"https://graph.facebook.com/{st.secrets['WHATSAPP_API_VERSION']}/{st.secrets['WHATSAPP_PHONE_NUMBER_ID']}/messages"
        headers = {
            "Authorization": f"Bearer {st.secrets['WHATSAPP_ACCESS_TOKEN']}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": st.secrets['WHATSAPP_BUSINESS_NUMBER'],
            "type": "text",
            "text": {"body": message}
        }
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass

class OmegaAgent:
    def __init__(self, domaine):
        st.session_state.domaine = domaine
        self.domaine = domaine

    def ceo(self, task):
        return call_meta_ai(f"Create 3-step marketing plan for: {task}", "Meta CEO")

    def cto(self, task):
        return call_meta_ai(f"Create technical strategy + Facebook ads targeting for: {task}", "Meta CTO")

    def coo(self, task):
        return call_meta_ai(f"Create execution plan + budget + timeline for: {task}", "Meta COO")

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        ad = call_meta_ai(f"Based on this plan: {plan}. Write 3 powerful Facebook ads in Arabic with strong CTA + WhatsApp: {whatsapp_num}", "Meta Copywriter")
        send_whatsapp_meta(f"👑 OMEGA AGENT - Meta AI\nإعلان جديد:\n\n{ad}")
        return ad

    def closer(self, ad):
        final = call_meta_ai(f"Take this ad: {ad}. Make it more aggressive with FOMO and urgency. Add 2 emojis max.", "Meta Closer")
        return final


# ==========================================
# 🧠 2. محرك DANA الأساسي (عبر Google Gemini)
# ==========================================

def dana_whatsapp_agent(prompt: str) -> str:
    """
    محرك الذكاء الاصطناعي المركزي لمعالجة الأوامر والنصوص والملفات 
    وإرجاع النتيجة بالأسلوب الاستراتيجي المطلوب.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "⚠️ عذراً يا سيدي، لم يتم استلام أي رد من النظام الأساسي."
            
    except Exception as e:
        return f"❌ حدث خطأ في محرك DANA الأساسي: {str(e)}"

def send_whatsapp_message(phone_number: str, message: str):
    """
    دالة محاكاة وتجهيز إرسال الرسائل عبر واتساب.
    """
    pass
