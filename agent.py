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
        data = res.json()
    except Exception as e:
        return f"خطأ في الاتصال بـ Meta: {e}"

    # حماية من KeyError - نجربو كل الاحتمالات
    try:
        return data['response'][0]['content'][0]['text']
    except KeyError:
        try:
            return data['output'][0]['content'][0]['text']
        except KeyError:
            try:
                return data['choices'][0]['message']['content']
            except KeyError:
                return f"خطأ من Meta: {data}"

class CEO:
    def __init__(self, domaine):
        self.domaine = domaine

    def plan(self, task):
        prompt = f"Goal: {task}. Create 3-step marketing plan for {self.domaine}. Respond in Arabic."
        return call_meta_ai(prompt, "Meta CEO Agent")

class CTO:
    def __init__(self, domaine):
        self.domaine = domaine

    def strategy(self, task):
        prompt = f"Goal: {task}. Create technical strategy for {self.domaine}. Respond in Arabic."
        return call_meta_ai(prompt, "Meta CTO Agent")

class COO:
    def __init__(self, domaine):
        self.domaine = domaine

    def execute(self, task):
        prompt = f"Goal: {task}. Create execution plan for {self.domaine}. Respond in Arabic."
        return call_meta_ai(prompt, "Meta COO Agent")
