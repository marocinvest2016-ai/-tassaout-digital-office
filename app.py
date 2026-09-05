import streamlit as st
from duckduckgo_search import DDGS
import pandas as pd
import re

st.set_page_config(page_title="DANA K9 EXECUTOR", layout="wide")
st.title("🐕 DANA K9 EXECUTOR")
st.markdown("**قاعدة**: عطي الأمر و أنا ننفد. ما كنسولش علاش.")

# صندوق الأوامر
command = st.text_area("🎯 عطي الأمر:",
    placeholder="أمثلة:\n1. قلب على أراضي للبيع في قلعة السراغنة\n2. جيب لي شركات لوجستيك في الدار البيضاء\n3. صيد لي مهندسين معماريين في مراكش")

col1, col2, col3 = st.columns(3)
with col1:
    extract_phone = st.checkbox("استخرج الأرقام", value=True)
with col2:
    extract_price = st.checkbox("استخرج الأثمنة", value=True)
with col3:
    export_excel = st.checkbox("صدر Excel", value=True)

def parse_command(cmd):
    # الكلب كيفهم الأمر بوحدو
    return f"{cmd} المغرب ثمن هاتف اتصال"

def get_data(query):
    results = []
    with DDGS() as ddgs:
        res = ddgs.text(query, region="ma-ma", max_results=20)
        for i, r in enumerate(res):
            text = r['title'] + " " + r['body']
            phone = re.findall(r'(\+212[67]\d{8}|0[67]\d{8})', text)[0] if extract_phone and re.findall(r'(\+212[67]\d{8}|0[67]\d{8})', text) else "غير متوفر"
            price = re.findall(r'(\d+[\s,]?\d*)\s*(درهم|dh)', text)[0][0] if extract_price and re.findall(r'(\d+[\s,]?\d*)\s*(درهم|dh)', text) else "غير محدد"

            results.append({
                "م": i+1,
                "النتيجة": r['title'],
                "الوصف": r['body'][:180],
                "الثمن": price,
                "الهاتف": phone,
                "الرابط": r['href']
            })
    return results

if st.button("🚀 نفد الأمر الآن"):
    if command:
        with st.spinner
