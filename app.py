import io
import time
import zipfile
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
import requests
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="خدمات السراغنة للتسويق الرقمي", page_icon="🏡", layout="wide")

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_ACCESS_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_API_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

@st.cache_resource
def init_supabase(): return create_client(SUPABASE_URL, SUPABASE_KEY)
@st.cache_resource
def init_groq(): return Groq(api_key=GROQ_API_KEY)

supabase = init_supabase()
groq_client = init_groq()

BRAND_NAME = "السراغنة عقار"
BRAND_PHONE = "+212691897126"

MASTER_SYSTEM_PROMPT = """
أنت "الوكيل الأعظم لخدمات السراغنة". أنت ذكاء اصطناعي فائق متعدد التخصصات.
لديك خبرة عميقة في: 1. الدعم الفني 2. الدعم الجمالي 3. الدعم الفكري 4. الدعم القانوني والعدلي
القاعدة الذهبية: حلل طلب المستخدم بدقة، وقم بتغطية كافة الجوانب المطلوبة في إجابة واحدة متكاملة ومنظمة.
إذا طلب المستخدم أن تتقمص شخصية معينة مثل "Zaha Hadid" فقم بذلك فوراً.
أجب دائماً باللغة العربية الفصحى بأسلوب احترافي، مباشر، ومرتب.
"""

def run_super_agent(user_task: str):
    messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}, {"role": "user", "content": user_task}]
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages, temperature=0.6, max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ في الوكيل الأعظم: {e}"

def add_watermark(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    try: font_big = ImageFont.truetype("arial.ttf", 40); font_small = ImageFont.truetype("arial.ttf", 28)
    except: font_big = font_small = ImageFont.load_default()
    w, h = img.size
    draw.rectangle([0, h - 100, w, h], fill=(0, 0, 0, 150))
    draw.text((20, h - 90), BRAND_NAME, font=font_big, fill=(255, 255, 255, 255))
    draw.text((20, h - 50), BRAND_PHONE, font=font_small, fill=(255, 255, 0, 255))
    buf = io.BytesIO(); Image.alpha_composite(img, txt).convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()

def create_zip_file(images_list):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i, item in enumerate(images_list): zip_file.writestr(f"poster_{i+1}_{item['orig_name']}", item['bytes'])
    zip_buffer.seek(0); return zip_buffer

def upload_bytes_to_supabase(image_bytes, filename):
    try:
        path = f"marketing/{filename}"
        supabase.storage.from_("property-images").upload(path=path, file=image_bytes, file_options={"content-type": "image/jpeg", "upsert": True})
        return supabase.storage.from_("property-images").get_public_url(path)
    except Exception as e: st.error(f"خطأ رفع الصورة: {e}"); return None

def send_whatsapp_media(image_url: str, caption: str, recipient_number: str):
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN): st.warning("⚠️ بيانات الواتساب غير مكتملة"); return False
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {"messaging_product": "whatsapp", "to": recipient_number, "type": "image", "image": {"link": image_url, "caption": caption}}
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}"}
    return requests.post(url, headers=headers, json=payload).status_code == 200

def save_to_supabase_logs(sector, message, image_count):
    try: supabase.table("instant_ads").insert({"sector": sector, "message": message, "image_count": image_count, "source": "Sraghna-Platform-v7.2"}).execute()
    except Exception as e: st.error(f"خطأ حفظ السجل: {e}")

st.title("🏡 المنصة المتكاملة للتسويق العقاري والواتساب")
menu = st.sidebar.radio("📌 القائمة الرئيسية", ["🤖 الوكيل الأعظم", "🚀 توليد إعلان سريع", "📸 استوديو الصور", "📊 الأرشيف"])

if menu == "🤖 الوكيل الأعظم":
    st.subheader("🧠 الوكيل الأعظم - v7.2")
    user_task = st.text_area("اطرح أي سؤال أو مهمة متكاملة:", height=180)
    if st.button("⚡ استشر الوكيل الأعظم", type="primary", use_container_width=True):
        if user_task:
            with st.spinner("الوكيل الأعظم يحلل..."):
                result = run_super_agent(user_task)
                st.markdown("### 📊 تقرير الوكيل الأعظم:")
                st.markdown(result)
                st.download_button("📄 تحميل التقرير", result, "report.txt")
        else: st.warning("الرجاء كتابة السؤال أولاً.")

elif menu == "🚀 توليد إعلان سريع":
    st.subheader("✨ إنتاج النص الإعلاني المباشر")
    title = st.text_input("عنوان العقار", "شقة للبيع بالسرغينة")
    price = st.text_input("الثمن", "400,000 درهم")
    details = st.text_area("التفاصيل", "شقة مشمسة، 3 غرف، صالون ومطبخ.")
    if st.button("⚡ توليد الإعلان", type="primary"):
        ad_text = run_super_agent(f"اكتب إعلان تسويقي جذاب لعقار: {title}, {price}, {details}")
        st.text_area("الإعلان الجاهز:", ad_text, height=200)

elif menu == "📸 استوديو الصور":
    st.subheader("🖼️ معالجة دفعية")
    uploaded_files = st.file_uploader("ارفع صور العقار", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if st.button("🚀 معالجة الصور"):
        if uploaded_files:
            st.session_state["results_gallery"] = [{"orig_name": f.name, "bytes": add_watermark(f.getvalue())} for f in uploaded_files]
            st.success(f"تمت معالجة {len(uploaded_files)} صور")
            st.download_button("📦 تحميل الكل ZIP", create_zip_file(st.session_state["results_gallery"]), "posters.zip")
            for i, item in enumerate(st.session_state["results_gallery"]): st.image(item["bytes"], caption=f"صورة {i+1}")
        else: st.warning("الرجاء رفع صورة")

elif menu == "📊 الأرشيف":
    st.subheader("📊 أرشيف العمليات")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(50).execute()
        if ads_data.data: st.dataframe(pd.DataFrame(ads_data.data), use_container_width=True)
        else: st.info("لا توجد سجلات")
    except Exception as e: st.error(f"خطأ: {e}")
