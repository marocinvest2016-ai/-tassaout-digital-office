import io
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import streamlit as st
from openai import OpenAI
from supabase import create_client, Client

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="منصة التسويق العقاري والواتساب الذكية",
    page_icon="🏡",
    layout="wide"
)

# ==========================================
# 2. جلب الإعدادات من Secrets
# ==========================================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "").strip()
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "").strip()

WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "").strip()
WHATSAPP_ACCESS_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "").strip()
WHATSAPP_BUSINESS_NUMBER = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "").strip()
WHATSAPP_API_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0").strip()

# ==========================================
# 3. تهيئة العملاء (Groq & Supabase)
# ==========================================
@st.cache_resource
def init_groq() -> OpenAI | None:
    if not GROQ_API_KEY:
        st.error("⚠️ مفتاح GROQ_API_KEY غير متاح.")
        return None
    try:
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY
        )
    except Exception as e:
        st.error(f"❌ فشل تهيئة عميل Groq: {e}")
        return None

@st.cache_resource
def init_supabase() -> Client | None:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.warning("⚠️ بيانات الاتصال بـ Supabase غير مكتملة.")
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"❌ فشل الاتصال بـ Supabase: {e}")
        return None

groq_client = init_groq()
supabase_client = init_supabase()

# ==========================================
# 4. دوال معالجة النص والواتساب
# ==========================================
def reshape_arabic(text: str) -> str:
    """إعادة تشكيل النص العربي للعرض في الصور."""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def add_watermark(image: Image.Image, watermark_text: str) -> Image.Image:
    """إضافة علامة مائية عريضة في أسفل الصورة."""
    img_copy = image.copy().convert("RGB")
    draw = ImageDraw.Draw(img_copy)
    w, h = img_copy.size
    
    font_path = "Amiri-Regular.ttf" if os.path.exists("Amiri-Regular.ttf") else "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, int(h * 0.04))
    except Exception:
        font = ImageFont.load_default()

    reshaped_txt = reshape_arabic(watermark_text)
    
    bbox = draw.textbbox((0, 0), reshaped_txt, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    overlay = Image.new("RGBA", img_copy.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    rect_h = text_h + 20
    overlay_draw.rectangle([(0, h - rect_h), (w, h)], fill=(0, 0, 0, 160))
    
    img_copy = Image.alpha_composite(img_copy.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img_copy)
    
    draw.text(((w - text_w) / 2, h - rect_h + 10), reshaped_txt, fill=(255, 255, 255), font=font)
    return img_copy

def send_whatsapp_message(recipient_number: str, text_message: str) -> dict:
    """إرسال رسالة عبر WhatsApp Cloud API."""
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": text_message
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ==========================================
# 5. الواجهة الرئيسية
# ==========================================
st.title("🏡 المنصة المتكاملة للتسويق العقاري والواتساب")
st.markdown("---")

menu = st.sidebar.radio(
    "القائمة الرئيسية",
    ["إنشاء وتوليد إعلان", "إرسال عبر WhatsApp", "سجل Supabase"]
)

if menu == "إنشاء وتوليد إعلان":
    st.header("✨ إنتاج النص والعلامة المائية")
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("عنوان العقار", "شقة للبيع بالسرغينة")
        price = st.text_input("الثمن", "400,000 درهم")
        details = st.text_area("التفاصيل", "شقة مشمسة، 3 غرف، صالون ومطبخ.")
    
    with col2:
        watermark = st.text_input("العلامة المائية", "السراغنة عقار")
        file = st.file_uploader("رفع صورة العقار", type=["jpg", "png", "jpeg"])

    if st.button("🚀 توليد الإعلان"):
        if groq_client:
            prompt = f"اكتب إعلان عقاري جذاب بناء على: العنوان: {title}، السعر: {price}، التفاصيل: {details}"
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = res.choices[0].message.content
            st.session_state["last_ad"] = generated_text
            st.success("تم التوليد بنجاح!")
            st.text_area("النص الناتج:", generated_text, height=200)

        if file:
            img = Image.open(file)
            marked_img = add_watermark(img, watermark)
            st.image(marked_img, caption="الصورة مع العلامة المائية", width=400)

elif menu == "إرسال عبر WhatsApp":
    st.header("📲 إرسال الإعلانات عبر واتساب")
    
    target_phone = st.text_input("رقم المستلم (مع الترميز الدولي دون +)", WHATSAPP_BUSINESS_NUMBER)
    message_content = st.text_area("محتوى الرسالة", value=st.session_state.get("last_ad", ""))
    
    if st.button("📤 إرسال الآن"):
        if not WHATSAPP_ACCESS_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
            st.error("بيانات WhatsApp Cloud API غير مكتملة في Secrets.")
        else:
            with st.spinner("جاري الإرسال عبر WhatsApp Cloud API..."):
                res = send_whatsapp_message(target_phone, message_content)
                if "messages" in res:
                    st.success(f"تم إرسال الرسالة بنجاح! ID الرسالة: {res['messages'][0]['id']}")
                else:
                    st.error(f"فشل الإرسال: {res}")

elif menu == "سجل Supabase":
    st.header("🗄️ الربط مع قاعدة البيانات Supabase")
    if supabase_client:
        st.success("الأتصال بـ Supabase قائم ومستقر.")
    else:
        st.warning("لم يتم الاتصال بـ Supabase بعد. تحقق من المتغيرات في Secrets.")
