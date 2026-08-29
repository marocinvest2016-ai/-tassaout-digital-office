import io
import time
import pandas as pd
import gdown
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timezone
from urllib.parse import quote

# إعداد الصفحة
st.set_page_config(page_title="وكيل تساوت الرقمي - الهندسة والتصميم", page_icon="🏗️", layout="wide")

# ========== الأسرار (Secrets) ==========
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

@st.cache_resource
def init_supabase(): 
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_resource
def init_groq(): 
    return Groq(api_key=GROQ_API_KEY)

@st.cache_resource
def load_ar_font():
    try:
        url = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Bold.ttf"
        gdown.download(url, "Cairo-Bold.ttf", quiet=True)
        return ImageFont.truetype("Cairo-Bold.ttf", 40), ImageFont.truetype("Cairo-Bold.ttf", 28)
    except: 
        return ImageFont.load_default(), ImageFont.load_default()

supabase = init_supabase()
groq_client = init_groq()
font_big, font_small = load_ar_font()

BRAND_NAME = "وكالة تساوت للإنتاج الرقمي والهندسة"
BRAND_PHONE = "+212691897126"

MASTER_SYSTEM_PROMPT = """أنت "وكيل تساوت للإنتاج الرقمي والهندسة"... خبير في صياغة الإعلانات الهندسية، المعمارية، والديكور الداخلي والصناعي."""

def run_super_agent(user_task: str):
    messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}, {"role": "user", "content": user_task}]
    for model_name in ["qwen/qwen3.8-27b", "openai/gpt-oss-120b"]:
        try:
            response = groq_client.chat.completions.create(model=model_name, messages=messages, temperature=0.6, max_tokens=2000)
            return response.choices[0].message.content
        except: 
            continue
    return "❌ تعذر الاتصال بنماذج النص الذكية."

def add_watermark(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    w, h = img.size
    draw.rectangle([0, h - 100, w, h], fill=(0, 0, 0, 180))
    draw.text((20, h - 90), BRAND_NAME, font=font_big, fill=(255, 255, 255, 255))
    draw.text((20, h - 50), BRAND_PHONE, font=font_small, fill=(255, 255, 0, 255))
    buf = io.BytesIO()
    Image.alpha_composite(img, txt).convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# ========== القائمة الجانبية (Navigation) ==========
st.sidebar.title("📌 القائمة الرئيسية")
menu = st.sidebar.radio("اختر القسم:", [
    "🧠 وكيل تساوت الرقمي", 
    "🏗️ توليد إعلان هندسي سريع", 
    "📸 استوديو التصميم والعلامة المائية", 
    "📊 الأرشيف السحابي"
])

if "last_ad" not in st.session_state: st.session_state["last_ad"] = ""
if "last_title" not in st.session_state: st.session_state["last_title"] = ""

# ==========================================
# 1. وكيل تساوت الرقمي
# ==========================================
if menu == "🧠 وكيل تساوت الرقمي":
    st.subheader("🧠 وكيل تساوت للإنتاج الرقمي والهندسة")
    user_task = st.text_area("اطرح أي مهمة استراتيجية أو استشارة هندسية وتسويقية:", height=180)
    if st.button("⚡ تنفيذ المهمة", type="primary", use_container_width=True):
        if user_task:
            with st.spinner("جاري المعالجة..."):
                result = run_super_agent(user_task)
                st.session_state["last_ad"] = result
                st.markdown("### 📊 تقرير وكيل تساوت:")
                st.markdown(result)
                st.download_button("📄 تحميل التقرير", result, f"tassaout_report_{int(time.time())}.txt")

# ==========================================
# 2. توليد إعلان هندسي سريع (مع الحفظ في Supabase)
# ==========================================
elif menu == "🏗️ توليد إعلان هندسي سريع":
    st.subheader("✨ توليد إعلان هندسي ومعماري + الحفظ التلقائي في السحاب")
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        service_type = st.selectbox(
            "اختر المجال الهندسي:",
            [
                "الهندسة المعمارية والتصميم الداخلي (الديكور)",
                "الهندسة المدنية والإنشائية",
                "الهندسة الصناعية والميكانيكية",
                "الاستشارات الهندسية والرفع التبوغرافي"
            ]
        )
    with col_opt2:
        city = st.text_input("المدينة / الموقع", "قلعة السراغنة / مراكش")

    title = st.text_input("عنوان المشروع", "تصميم هندسي متكامل لفيلا عصرية")
    price = st.text_input("التكلفة أو الميزانية (اختياري)", "حسب طلب العميل والمساحة")
    details = st.text_area("تفاصيل المشروع والمميزات:", "تصميم 3D احترافي، استغلال ذكي للمساحات، إشراف تقني ودقيق.")
    
    st.session_state["last_title"] = title

    if st.button("⚡ توليد الإعلان وحفظه في القاعدة", type="primary", use_container_width=True):
        prompt = f"اكتب إعلان تسويقي احترافي لمكتب هندسي في مجال {service_type}: المشروع {title}, الموقع {city}, التفاصيل {details}. اختمه برقم الهاتف {BRAND_PHONE}"
        with st.spinner("جاري صياغة الإعلان بالذكاء الاصطناعي..."):
            ad_text = run_super_agent(prompt)
            st.session_state["last_ad"] = ad_text
            
        st.text_area("الإعلان الجاهز:", st.session_state["last_ad"], height=250)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📋 نسخ الإعلان", use_container_width=True):
                st.code(st.session_state["last_ad"], language="text")
                st.success("✅ تم العرض، حدد النص للنسخ")
        with col_btn2: 
            st.download_button("📄 تحميل الإعلان", st.session_state["last_ad"], "tassaout_engineering_ad.txt", use_container_width=True)

        # تجهيز رابط الواتساب المباشر
        whatsapp_url = f"https://wa.me/?text={quote(st.session_state['last_ad'])}"
        st.markdown(f"### 📲 [مشاركة الإعلان مباشرة عبر الواتساب]({whatsapp_url})")

        # الحفظ التلقائي في جدول instant_ads في Supabase
        try:
            supabase.table("instant_ads").insert({
                "category": service_type, 
                "city": city,
                "content": title,
                "message": ad_text, 
                "price": 0, 
                "source": "Tassaout-Engineering-v10.7", 
                "created_at": datetime.now(timezone.utc).isoformat()
            }).execute()
            st.success("✅ تم حفظ الإعلان هندسياً وسحابياً في جدول instant_ads بنجاح!")
        except Exception as e: 
            st.error(f"خطأ في الحفظ السحابي: {e}")

# ==========================================
# 3. استوديو التصميم والعلامة المائية (تحميل يدوي)
# ==========================================
elif menu == "📸 استوديو التصميم والعلامة المائية":
    st.subheader("📸 استوديو تساوت الهندسي - إضافة العلامة المائية لمخططات وتصاميم 3D")
    if st.session_state["last_ad"]:
        st.info(f"📌 آخر مشروع مسجل: {st.session_state['last_title']}")

    uploaded_files = st.file_uploader("اختر صور التصاميم أو المخططات من الهاتف (رفع متعدد)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown("---")
        st.subheader("🖼️ المعاينة والتحميل اليدوي للصور المعالجة")
        
        for idx, f in enumerate(uploaded_files):
            f_bytes = f.getvalue()
            processed_bytes = add_watermark(f_bytes)
            
            col_img, col_dl = st.columns([2, 1])
            with col_img:
                st.image(processed_bytes, caption=f"تصميم معالج {idx+1}", width=350)
            with col_dl:
                st.download_button(
                    label=f"📥 تحميل التصميم {idx+1}",
                    data=processed_bytes,
                    file_name=f"tassaout_design_{idx+1}.jpg",
                    mime="image/jpeg",
                    key=f"dl_img_{idx}"
                )

# ==========================================
# 4. الأرشيف السحابي
# ==========================================
elif menu == "📊 الأرشيف السحابي":
    st.subheader("📊 الأرشيف السحابي للمشاريع الهندسية (جدول instant_ads)")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(100).execute()
        if ads_data.data: 
            st.dataframe(pd.DataFrame(ads_data.data), use_container_width=True)
            st.metric("إجمالي المشاريع والأرشيف", len(ads_data.data))
        else: 
            st.info("لا توجد سجلات في الأرشيف حالياً.")
    except Exception as e: 
        st.error(f"خطأ جلب الأرشيف: {e}")
