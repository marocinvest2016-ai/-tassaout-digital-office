import requests
import streamlit as st

def call_meta_ai(task, role="Expert Agent"):
    """دالة وحدة كتهضر مع MUSE-SPARK 1.2"""
    META_KEY = st.secrets["MODEL_API_KEY"]

    url = "https://api.meta.ai/v1/responses"
    headers = {"Authorization": f"Bearer {META_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "muse-spark-1.2",
        "input": [
            {"role": "system", "content": [{"type": "input_text", "text": f"You are {role}. Respond in Moroccan Arabic with emojis. For TASSAOUT & ATIS"}]},
            {"role": "user", "content": [{"type": "input_text", "text": task}]}
        ]
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()['response'][0]['content'][0]['text']

class OmegaAgent:
    def __init__(self, domaine):
        self.domaine = domaine

    def ceo(self, task):
        return call_meta_ai(f"Goal: {task}. Create 3-step marketing plan for {self.domaine}", "CEO Agent")

    def copywriter(self, plan):
        return call_meta_ai(f"Based on plan: {plan}. Write powerful ad in Moroccan Arabic for {self
