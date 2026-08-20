import streamlit as st
from supabase import create_client, Client
import urllib.parse
from datetime import datetime

# إعدادات النظام السيادي
st.set_page_config(page_title="OMEGA OS - V2.1 Sovereign", layout="wide")

# إعداد Supabase
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("👑 OMEGA OS - Sovereign Edition V2.1")

# دالة رابط الواتساب المباشر
def get_whatsapp_link(phone_number, message):
    encoded_msg = urllib.parse.quote(message)
    clean_number = "212" + phone_number[1:]
    return f"https://wa.me/{clean_number}?text={encoded_msg}"

# القائمة الجانبية
menu = st.sidebar.selectbox("الوحدة السيادية", [
    "رصد الميدان", 
    "مصنع الإعلانات العقارية 📢", 
    "مصنع الخدمات الرقمية 💻",
    "الأرشيف والتقارير"
])

# ==========================================
# الوحدة 1: مصنع الإعلانات العقارية
# ==========================================
if menu == "مصنع الإعلانات العقارية 📢":
    st.header("📢 مصنع صياغة الإعلانات (عقار/معدات)")
    cat_list = ["عقار فلاحي", "عقار تجاري", "عقار صناعي", "عقار سكني", "عقار مهني وخدماتي", "عقار استثماري", "معدات واليات"]
    p_type = st.selectbox("نوع العقار:", cat_list)
    loc = st.text_input("الموقع:")
    price = st.text_input("السعر:")
    features = st.text_area("المميزات:")
    
    if st.button("توليد + أرشفة + نشر 🚀"):
        ad_text = f"👑 إعلان حصري - {p_type}\n\nفرصة مميزة في {loc}.\n🔹 التصنيف: {p_type}\n🔹 السعر: {price}\n\nالمميزات:\n{features}\n\nللتواصل: 0691897126\nSraghna Media & Tassaout"
        st.code(ad_text, language="text")
        
        wa_link = get_whatsapp_link("0691897126", ad_text)
        st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
        
        supabase.table("reports").insert({
            "project_name": p_type, 
            "report_content": ad_text, 
            "report_type": "إعلان عقاري",
            "created_at": datetime.now().isoformat()
        }).execute()
        st.success("تم التوليد والأرشفة والنشر بنجاح!")

# ==========================================
# الوحدة 2: مصنع الخدمات الرقمية
# ==========================================
elif menu == "مصنع الخدمات الرقمية 💻":
    st.header("💻 مصنع إعلانات الخدمات الرقمية")
    dig_services = ["تصميم هوية بصرية", "إدارة حملات إعلانية", "إدارة منصات التواصل", "برمجة وأتمتة"]
    selected_service = st.selectbox("نوع الخدمة:", dig_services)
    target = st.text_input("الجمهور المستهدف:")
    details = st.text_area("تفاصيل العرض:")
    
    if st.button("توليد + أرشفة + نشر 🚀"):
        digital_ad = f"🚀 عرض خاص: {selected_service}\n\nهل ترغب في تطوير {target}؟\nنقدم لك حلولاً رقمية مبتكرة.\n\nتفاصيل العرض:\n{details}\n\n📞 تواصل معنا: 0691897126\nDANA Digital Market"
        st.code(digital_ad, language="text")
        
        wa_link = get_whatsapp_link("0691897126", digital_ad)
        st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
        
        supabase.table("reports").insert({
            "project_name": selected_service, 
            "report_content": digital_ad, 
            "report_type": "إعلان رقمي",
            "created_at": datetime.now().isoformat()
        }).execute()
        st.success("تم التوليد والأرشفة والنشر بنجاح!")

# ==========================================
# الوحدة 3: الأرشيف
# ==========================================
elif menu == "الأرشيف والتقارير":
    st.header("📁 الأرشيف السيادي")
    data = supabase.table("reports").select("*").order("created_at", desc=True).execute().data
    if data:
        for r in data:
            with st.expander(f"📌 {r.get('report_type')} - {r.get('project_name')} - {str(r.get('created_at'))[:10]}"):
                st.code(r.get('report_content'), language="text")
                wa_link = get_whatsapp_link("0691897126", r.get('report_content'))
                st.link_button("📲 إعادة النشر عبر واتساب", wa_link)
    else:
        st.info("لا توجد تقارير مسجلة في الأرشيف حالياً.")
