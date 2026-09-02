import streamlit as st
import requests

def call_meta_ai(prompt, agent_name):
    url = "https://api.meta.ai/v1/responses"
    headers = {
        "Authorization": f"Bearer {st.secrets['META_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "muse-spark-1.2",
        "input": prompt,
        "agent": agent_name
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return f"خطأ في الاتصال بـ Meta: {e}"

    # نجربو كل صيغ الرد
    if 'response' in data and data['response']:
        return data['response'][0]['content'][0]['text']
    elif 'output' in data and data['output']:
        return data['output'][0]['content'][0]['text']
    elif 'choices' in data and data['choices']:
        return data['choices'][0]['message']['content']
    else:
        return f"رد غير متوقع من Meta: {data}"

class OmegaAgent:
    def __init__(self, domaine):
        self.domaine = domaine

    def ceo(self, task):
        return call_meta_ai(f"Goal: {task}. Create 3-step marketing plan for {self.domaine}. Respond in Arabic.", "Meta CEO")

    def cto(self, task):
        return call_meta_ai(f"Goal: {task}. Create technical strategy for {self.domaine}. Respond in Arabic.", "Meta CTO")

    def coo(self, task):
        return call_meta_ai(f"Goal: {task}. Create execution plan for {self.domaine}. Respond in Arabic.", "Meta COO")
