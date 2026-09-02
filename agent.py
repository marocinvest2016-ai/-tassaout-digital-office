import streamlit as st
import requests

def call_meta_ai(prompt, agent_name):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['META_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": f"You are {agent_name} from Meta AI. Expert in {st.session_state.domaine}. Respond in Moroccan Arabic Darija with bullet points and emojis."},
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
    url = f"https://graph.facebook.com/{st.secrets['WHATSAPP_API_VERSION']}/{st.secrets['WHATSAPP_PHONE_NUMBER_ID']}/messages"
    headers = { # <-- كان هنا القوس ناقص
        "Authorization": f"Bearer {st.secrets['WHATSAPP_ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": st.secrets['WHATSAPP_BUSINESS_NUMBER'],
        "type": "text",
        "text": {"body": message}
    }
    try: requests.post(url, headers=headers, json=payload, timeout=10)
    except: pass

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
        ad = call_meta_ai(f"Based on this plan: {plan}. Write 3 powerful Facebook ads in Arabic with strong CTA + WhatsApp: {st.secrets['WHATSAPP_BUSINESS_NUMBER']}", "Meta Copywriter")
        send_whatsapp_meta(f"👑 OMEGA AGENT - Meta AI\nإعلان جديد:\n\n{ad}")
        return ad

    def closer(self, ad): # <-- زدنا هادي باش يخدم app.py
        final = call_meta_ai(f"Take this ad: {ad}. Make it more aggressive with FOMO and urgency. Add 2 emojis max.", "Meta Closer")
        return final
