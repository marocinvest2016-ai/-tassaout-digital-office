import streamlit as st
from duckduckgo_search import DDGS
import pandas as pd
import re

st.set_page_config(page_title="DANA K9 EXECUTOR", layout="wide")
st.title("🐕 DANA K9 EXECUTOR")
st.markdown("**القاعدة**: عطي الأمر و أنا ننفد.")

command = st.text_area("🎯 عطي الأمر:",
    placeholder="مثال: قلب على أراضي للبيع في قلعة السراغنة")

col1, col2, col3 = st.columns(3)
with col1:
    do_phone = st.checkbox("استخرج الأرقام", value=True)
with col2:
    do_price = st.checkbox("استخرج الأثمنة", value=True)
with col3:
    do_excel = st.checkbox("صدر Excel", value=True)

PHONE_REGEX = r'(\+212[67]\d{8}|0[67]\d{8})'
PRICE_REGEX = r'(\d+[\s,]?\d*)\s*(درهم|dh|MAD)'

def parse_command(cmd):
    return f"{cmd} المغرب ثمن هاتف"

def get_data(query, do_phone, do_price):
    results = []
    with st.spinner("🐕 DANA K9 كيصيد دابا..."):
        with DDGS() as ddgs:
            res = ddgs.text(query, region="ma-ma", max_results=20)
            for i, r in enumerate(res):
                text = r['title'] + " " + r['body']

                phone = "غير متوفر"
                if do_phone:
                    phones = re.findall(PHONE_REGEX, text)
                    if phones: phone = phones[0]

                price = "غير محدد"
                if do_price:
                    prices = re.findall(PRICE_REGEX, text)
                    if prices: price = f"{prices[0][0]} {prices[0][1]}"

                results.append({
                    "م": i+1,
                    "النتيجة": r['title'],
                    "الوصف": r['body'][:180] + "...",
                    "الثمن": price,
                    "الهاتف": phone,
                    "الرابط": r['href']
                })
    return results

if st.button("🚀 نفد الأمر الآن"):
    if command:
        query = parse_command(command)
        data = get_data(query, do_phone, do_price)

        if data:
            df = pd.DataFrame(data)
