from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"], # حيت احنا خدامين بـ Groq
    base_url="https://api.groq.com/openai/v1"
)
