import streamlit as st
from supabase import create_client
import google.generativeai as genai
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Tassaout Reality AI", page_icon="🏛️", layout="wide")

# ====== تحميل المفاتيح ======
s = st.secrets
supabase = create_client(s["SUPABASE_URL"], s["SUPABASE_KEY"])
genai.configure(api_key=s["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

WHATSAPP_URL = f"https://graph.facebook.com/{s['WHATSAPP_API_VERSION']}/{s['WHATSAPP_PHONE_NUMBER_ID']}/messages"
WHATSAPP_HEADERS = {"Authorization": f"Bearer {s['WHATSAPP_ACCESS_TOKEN']}", "Content-Type": "application/json"}

st.title("🏛️ Tassaout Reality AI")
st.subheader("وكيل عقاري رقمي متعدد المجالات | Agent Immobilier Super Multidomaine")

# ====== دوال الوكيل ======
def generate_listing(property_data):
    """توليد وصف العقار بالعربية والفرنسية بالـ Gemini"""
    prompt = f"""
    أنت وكيل عقاري محترف في مراكش. اكتب وصف تسويقي جذاب للعقار التالي باللغتين العربية الفصحى والفرنسية.
    البيانات: {property_data}
    أضف في النهاية: APPROUVÉ PAR AMEUR | Tassaout Vision Verified © 2026
    """
    response = model.generate_content(prompt)
    return response.text

def save_to_supabase(property_data):
    """حفظ العقار في Supabase"""
    data = {
        "created_at": datetime.now().isoformat(),
        "title_ar": property_data["title_ar"],
        "title_fr": property_data["title_fr"],
        "prix": property_data["prix"],
        "region": property_data["region"],
        "description": property_data["description"]
    }
    supabase.table("properties").insert(data).execute()
    return True

def send_whatsapp(to_number, message):
    """إرسال رسالة WhatsApp"""
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    res = requests.post(WHATSAPP_URL, headers=WHATSAPP_HEADERS, json=payload)
    return res.status_code == 200

# ====== الواجهة ======
tab1, tab2, tab3 = st.tabs(["➕ إضافة عقار", "📊 قاعدة البيانات", "💬 اختبار WhatsApp"])

with tab1:
    st.markdown("### إضافة عقار جديد - الوكيل سيولد الوصف تلقائيا")
    with st.form("add_property"):
        c1, c2 = st.columns(2)
        with c1:
            title_ar = st.text_input("عنوان العقار AR", "فيلا فاخرة بتاساوت")
            region = st.selectbox("المنطقة", ["Marrakech", "El Haouz", "Tassaout"])
        with c2:
            title_fr = st.text_input("Titre FR", "Villa de luxe à Tassaout")
            prix = st.number_input("السعر MAD", 0, 10000000, 3500000)
        
        details = st.text_area("تفاصيل إضافية", "3 غرف، 2 حمام، حديقة، 200م²")
        
        if st.form_submit_button("🚀 نشر بالوكيل الذكي", type="primary"):
            property_data = {"title_ar": title_ar, "title_fr": title_fr, "prix": prix, "region": region, "details": details}
            
            with st.spinner("الوكيل يولد الوصف..."):
                description = generate_listing(property_data)
                property_data["description"] = description
                save_to_supabase(property_data)
            
            st.success("✅ تم النشر بنجاح")
            st.text_area("الوصف المولد", description, height=200)

with tab2:
    st.markdown("### العقارات المسجلة")
    data = supabase.table("properties").select("*").execute()
    st.dataframe(data.data)

with tab3:
    st.markdown("### اختبار إرسال WhatsApp")
    phone = st.text_input("رقم العميل", "2126")
    msg = st.text_area("الرسالة", "مرحبا، لدينا عقار جديد بتاساوت. هل تود الزيارة؟")
    if st.button("إرسال"):
        if send_whatsapp(phone, msg):
            st.success("✅ تم الإرسال")
        else:
            st.error("❌ فشل الإرسال")

st.markdown("---")
st.caption("#D4AF37 #800020 | APPROUVÉ PAR AMEUR")
