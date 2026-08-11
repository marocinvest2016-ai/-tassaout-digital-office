import os
import streamlit as st
from google import genai

# جلب المفتاح سواء كان مخزناً باسم GEMINI_API_KEY أو GOOGLE_API_KEY
api_key = (
    st.secrets.get("GEMINI_API_KEY")
    or st.secrets.get("GOOGLE_API_KEY")
    or os.environ.get("GEMINI_API_KEY")
    or os.environ.get("GOOGLE_API_KEY")
)

# تهيئة العميل باستخدام المفتاح المُكتشف
client = genai.Client(api_key=api_key)
