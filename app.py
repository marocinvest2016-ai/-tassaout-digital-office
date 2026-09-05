import streamlit as st
from duckduckgo_search import DDGS
import pandas as pd
import re

st.set_page_config(page_title="DANA K9 EXECUTOR", layout="wide")
st.title("🐕 DANA K9 EXECUTOR")
st.markdown("**القاعدة**: عطي الأمر و أنا ننفد. ما كنسولش.")

# صندوق الأوامر
command = st.text_area("🎯 عطي الأمر:",
    placeholder="أمثلة:\n1. قلب على أراضي للبيع في قلعة السراغنة\n2. جيب لي شركات لوجستيك في الدار البيضاء")

col1, col2, col3 = st.columns(3)
with col1:
    do_phone = st.checkbox("استخرج الأرقام", value=True)
with col2:
    do_price = st.checkbox("استخرج الأثمنة", value=True)
with col3:
    do_excel = st.checkbox("صدر Excel", value=True)

def parse_command(cmd):
    return f"{cmd} المغرب ثمن هاتف اتصال"

def get_data(query, do_phone, do_price):
    results = []
    with st.spinner("🐕 DANA K9 كيصيد دابا..."): # <-- هنا كانت المشكلة، زدت :
        with DDGS() as ddgs:
            res = ddgs.text(query, region="ma-ma", max_results=20)
            for i, r in enumerate(res):
                text = r['title'] + " " + r['body']

                phone = "غير متوفر"
                if do_phone:
                    phones = re.findall(r'(\+212[67]\d{8}|0
