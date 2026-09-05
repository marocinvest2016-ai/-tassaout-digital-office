import streamlit as st
from openai import OpenAI
import requests

# 1. إعدادات الصفحة - لازم تكون اللولة
st.set_page_config(page_title="DANA OMEGA BRAIN", page_icon="🧠", layout="wide")

# 2. الاتصال بـ Groq بأمان
@st.cache_resource
def get_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error("❌ خطأ فادح: GROQ_API_KEY غير موجود فـ Streamlit Secrets")
        st.info("سير لـ Settings > Secrets وزيد:
