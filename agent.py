import requests
import streamlit as st

def call_meta_ai(task, role="Expert Agent"):
    """هادي كتهضر مباشرة مع Meta AI Muse Spark 1.2"""
    META_KEY = st.secrets["MODEL_API_KEY"] # مفتاح Meta

    url = "https://api.meta.ai/v1/responses" # API ديال Meta
    headers = {"Authorization": f"Bearer {META_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "muse-spark-1.2", # موديل Meta
        "input": [
            {"role": "system", "content": [{"type": "input_text", "text": f"You are {role} from Meta AI. Respond in Moroccan Arabic. For TASSAOUT & ATIS"}]},
            {"role": "user", "content": [{"type": "input_text", "text": task}]}
        ]
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()['response'][0]['content'][0]['text']

class OmegaAgent:
    def __init__(self, domaine):
        self.domaine = domaine

    def ceo(self, task):
        return call_meta_ai(f"Goal: {task}. Create 3-step marketing plan for {self.domaine}", "Meta CEO Agent")

    def copywriter(self, plan):
        return call_meta_ai(f"Based on plan: {plan}. Write powerful ad in Moroccan Arabic for {self.domaine}. Add phone +212691897126", "Meta Marketing Agent")

    def closer(self, ad):
        return call_meta_ai(f"Take this ad: {ad}. Add strong CTA and 3 hashtags for {self.domaine}", "Meta Sales Agent")
