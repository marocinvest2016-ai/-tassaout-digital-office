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
    headers = {
