import streamlit as st
from google import genai
import requests
import datetime

# إعداد العميل باستخدام حزمة google-genai الحديثة
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def dana_whatsapp_agent(prompt_text):
    """
    دالة وكيل الذكاء الاصطناعي باستخدام google-genai الحديثة
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text,
        )
        return response.text
    except Exception as e:
        return f"عذراً، حدث خطأ في معالجة الطلب عبر نموذج الذكاء الاصطناعي: {str(e)}"

def send_whatsapp_message(phone_number, message):
    """
    دالة إرسال رسائل واتساب
    """
    try:
        pass
    except Exception as e:
        print(f"Error sending WhatsApp: {e}")
