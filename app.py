import io
import time
import zipfile
import pandas as pd
import gdown
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
import requests
import streamlit as st
from supabase import create_client
from datetime import datetime

st.set_page_config(page_title="وكالة تساوت للإنتاج الرقمي", page_icon="⚙️", layout="wide")

# ========== الأسرار (Secrets) ==========
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_ACCESS_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_API_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

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
        font_big = ImageFont.truetype("Cairo-Bold.ttf", 40)
        font_small = ImageFont.truetype("Cairo-Bold.ttf", 28)
        return font_big, font_small
    except Exception:
        return ImageFont.load_default(), ImageFont.load_default()

supabase = init_supabase()
groq_client = init_groq()
font_big, font_small = load_ar_font()

BRAND_NAME = "وكالة تساوت للإنتاج الرقمي"
BRAND_PHONE = "+212691897126"

MASTER_SYSTEM_PROMPT = """
أنت "وكيل تساوت للإنتاج الرقمي" (Tassaout Digital Production Agent).
أنت ذكاء اصطناعي استراتيجي، متعدد التخصصات، وعميق المعرفة، تعمل كشريك تنفيذي وفكري لعامر.

مجالات اختصاصك وهوياتك المتعددة:
1. الجانب الميداني والتجاري: العقار (الفلاحي، الصناعي، المهني، الاستثماري)، توريد مواد البناء والصفقات العمومية، الهندسة الصناعية والميكانيكية، والآليات الفلاحية.
2. الجانب التقني والجمالي: الهندسة الرقمية، التصميم ثلاثي الأبعاد، الديكور الداخلي، والنقد البصري.
3. الجانب الفكري، الثقافي، والأدبي: متشبّع بالتراث العربي الكبير وبالآداب العالمية الكبرى. تتقن الفلسفة، السياسة، التحليل الاستراتيجي، والإعلام الرقمي.
4. القدرة التراكمية: تتعلم من كل مدخل، صورة، أو مقال لتطوير أدائك ورفع جودة محتواك باستمرار.

القاعدة الذهبية: حلل طلب المستخدم بدقة، وتقمص القبعة المناسبة فوراً.
أجب دائماً باللغة العربية الفصحى بأسلوب رصين، بليغ، واحترافي خالٍ من السطحية.

في ختام كل إجابة استراتيجية، قدمها وفق "ثلاثية القيمة":
1. **الجانب التقني/التنفيذي**: خطوات التطبيق العملي.
2. **الجانب الاستثماري/الاقتصادي**: الجدوى والعائد المتوقع.
3. **الجانب الاستراتيجي/الفلسفي**: الأثر بعيد المدى والمنطق الكامن.
"""

def run_super_agent(user_task: str):
    messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}, {"role": "user", "content": user_task}]
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # <--- تم التصحيح إلى الموديل المستقر والمضمون
            messages=messages, temperature=0.6, max_tokens=1800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"حدث خطأ في وكيل تساوت: {e}"

def add_watermark(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    w, h = img.size
    draw.rectangle([0, h - 100, w, h], fill=(0, 0, 0, 160))
    draw.text((20, h - 90), BRAND_NAME, font=font_big, fill=(255, 255, 255, 255))
    draw.text((20, h - 50), BRAND_PHONE, font=font_small, fill=(255, 255, 0, 255))
    buf = io.BytesIO(); Image.alpha_composite(img, txt).convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()

def upload_image_to_supabase_storage(image_bytes, filename):
    try:
        path = f"tassaout_media/{int(time.time())}_{filename}"
        supabase.storage.from_("property-images").upload(
            path=path, file=image_bytes, file_options={"content-type": "image/jpeg", "upsert": True}
        )
        return supabase.storage.from_("property-images").get_public_url(path)
    except Exception as e:
        st.error(f"خطأ رفع الصورة لسحاب Supabase: {e}")
        return None

def send_whatsapp_media(image_url: str, caption: str, recipient_number: str):
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN):
        return False, "بيانات ربط واتساب ناقصة في الأسرار (Secrets)."
    
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True, "تم الإرسال بنجاح عبر الواتساب!"
        else:
            return False, f"خطأ من واجهة الواتساب: {response.text}"
    except Exception as e:
        return False, f"خطأ شبكي أثناء الإرسال: {e}"

def create_zip_file(images_list):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i, item in enumerate(images_list):
            zip_file.writestr(f"tassaout_poster_{i+1}_{item['orig_name']}", item['bytes'])
    zip_buffer.seek(0); return zip_buffer

# ========== الواجهة التفاعلية v7.5.3 ==========
st.title("⚙️ وكالة تساوت للإنتاج الرقمي")
st.caption("النظام المستقل المدمج بالأتمتة والواتساب - v7.5.3")
menu = st.sidebar.radio("📌 القائمة الرئيسية", ["🧠 وكيل تساوت الرقمي", "🚀 توليد إعلان سريع", "📸 استوديو التصوير الميداني", "📊 الأرشيف السحابي"])

if menu == "🧠 وكيل تساوت الرقمي":
    st.subheader("🧠 وكيل تساوت للإنتاج الرقمي - v7.5.3")
    user_task = st.text_area("اطرح أي مهمة (عقار، مواد بناء، مقال فكري، تحليل، أو نص أدبي):", height=180, placeholder="مثال: حلل لي جدوى استثمار فيرمة سقوية بقلعة السراغنة...")
    if st.button("⚡ تنفيذ المهمة عبر الوكيل", type="primary", use_container_width=True):
        if user_task:
            with st.spinner("وكيل تساوت يحلل وينتج وفق ثلاثية القيمة..."):
                result = run_super_agent(user_task)
                st.markdown("### 📊 تقرير ومخرجات وكيل تساوت:")
                st.markdown(result)
                st.download_button("📄 تحميل المخرجات", result, f"tassaout_report_{int(time.time())}.txt")
        else: st.warning("الرجاء كتابة المهمة أو السؤال أولاً.")

elif menu == "🚀 توليد إعلان سريع":
    st.subheader("✨ إنتاج النص الإعلاني والتجاري مع الحفظ السحابي")
    col1, col2 = st.columns(2)
    with col1: title = st.text_input("عنوان المشروع أو العقار", "أرض فلاحية سقوية بقلعة السراغنة")
    with col2: price = st.text_input("الثمن أو التفاصيل التجارية", "عرض خاص للمستثمرين")
    details = st.text_area("تفاصيل إضافية", "مجهزة بالكامل، مناسبة للاستثمار الفلاحي الفوري.")

    if st.button("⚡ توليد الإعلان الميداني", type="primary", use_container_width=True):
        prompt = f"اكتب إعلان تسويقي احترافي لعقار/خدمة: {title}, {price}, {details}. أضف معلومات الاتصال والهاشتاغات الخاصة بوكالة تساوت."
        ad_text = run_super_agent(prompt)
        st.text_area("الإعلان الجاهز للنشر:", ad_text, height=250)

        try:
            supabase.table("instant_ads").insert({
                "sector": "عقارات وديكور",
                "message": f"إعلان: {title}",
                "content": ad_text,
                "client_phone": BRAND_PHONE,
                "status": "completed",
                "source": "Tassaout-DigitalProduction",
                "image_count": 0,
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("✅ تم حفظ الإعلان وتحديث أرشيف Supabase سحابياً")
        except Exception as e:
            st.error(f"خطأ في الحفظ السحابي: {e}")

elif menu == "📸 استوديو التصوير الميداني":
    st.subheader("📸 التقاط، معالجة، وإرسال مباشر عبر الواتساب")
    
    tab_cam, tab_up = st.tabs(["📷 التقاط بالكاميرا المباشرة", "📁 رفع صور متعددة"])
    
    captured_image = None
    uploaded_files = None
    
    with tab_cam:
        camera_file = st.camera_input("التقط صورة ميدانية للعقار أو الورش")
        if camera_file:
            captured_image = camera_file.getvalue()
            
    with tab_up:
        uploaded_files = st.file_uploader("أو رفع مجموعة صور", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if st.button("🚀 تطبيق العلامة وحفظها في Supabase", type="primary"):
        processed_items = []
        
        if captured_image:
            processed_bytes = add_watermark(captured_image)
            pub_url = upload_image_to_supabase_storage(processed_bytes, "camera_capture.jpg")
            processed_items.append({"orig_name": "camera_capture.jpg", "bytes": processed_bytes, "url": pub_url})
            
        if uploaded_files:
            for f in uploaded_files:
                f_bytes = f.getvalue()
                processed_bytes = add_watermark(f_bytes)
                pub_url = upload_image_to_supabase_storage(processed_bytes, f.name)
                processed_items.append({"orig_name": f.name, "bytes": processed_bytes, "url": pub_url})
                
        if processed_items:
            st.success(f"تمت معالجة وحفظ {len(processed_items)} صورة سحابياً بنجاح!")
            st.session_state["results_gallery"] = processed_items
            st.download_button("📦 تحميل الكل ZIP", create_zip_file(processed_items), "tassaout_posters.zip")
        else: 
            st.warning("الرجاء التقاط صورة أو رفع صور للمعالجة أولاً.")

    if "results_gallery" in st.session_state and st.session_state["results_gallery"]:
        st.markdown("---")
        st.subheader("📤 الإرسال الفوري عبر WhatsApp API")
        
        recipient_phone = st.text_input("رقم الهاتف المستلم (بالصيغة الدولية مع الرمز، مثال: 2126XXXXXXXX)", value="212")
        wa_caption = st.text_area("نص التوضيح (Caption) المرافق للصورة على الواتساب", value="🏡 عرض حصري من وكالة تساوت للإنتاج الرقمي:\nللتواصل والاستعلام: +212691897126")

        for idx, item in enumerate(st.session_state["results_gallery"]):
            col_img, col_btn = st.columns([2, 1])
            with col_img:
                st.image(item["bytes"], caption=f"صورة رقم {idx+1}")
                if item["url"]:
                    st.code(item["url"], language="text")
            with col_btn:
                if st.button(f"📲 إرسال الصورة {idx+1} للواتساب", key=f"wa_btn_{idx}DATA"):
                    if item["url"]:
                        with st.spinner("جاري الإرسال عبر خوادم واتساب..."):
                            success, msg = send_whatsapp_media(item["url"], wa_caption, recipient_phone)
                            if success:
                                st.success(msg)
                            else:
                                st.error(msg)
                    else:
                        st.error("رابط الصورة السحابي غير متوفر.")

elif menu == "📊 الأرشيف السحابي":
    st.subheader("📊 أرشيف السجلات والبيانات من Supabase")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(100).execute()
        if ads_data.data:
            df = pd.DataFrame(ads_data.data)
            st.dataframe(df, use_container_width=True)
            st.metric("إجمالي السجلات السحابية", len(df))
        else: st.info("لا توجد سجلات مسجلة حالياً في Supabase")
    except Exception as e: st.error(f"خطأ في جلب الأرشيف: {e}")
