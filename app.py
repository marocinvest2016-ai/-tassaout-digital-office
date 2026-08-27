import io
import time
import zipfile
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from google import genai
from google.genai import types
import requests
import streamlit as st
from supabase import create_client, Client

# ==========================================
# 1. إعدادات الصفحة والأسرار والتكوين الأساسي
# ==========================================
st.set_page_config(
    page_title="خدمات السراغنة للتسويق الرقمي",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "").strip()

raw_gemini_key = st.secrets.get("GEMINI_API_KEY", "").strip()
GEMINI_API_KEY = raw_gemini_key.encode("ascii", "ignore").decode("ascii")

WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "").strip()
WHATSAPP_ACCESS_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "").strip()
WHATSAPP_BUSINESS_NUMBER = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "").strip()
WHATSAPP_API_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0").strip()
WHATSAPP_LINK = f"https://wa.me/{WHATSAPP_BUSINESS_NUMBER}" if WHATSAPP_BUSINESS_NUMBER else "#"

@st.cache_resource
def init_supabase() -> Client | None:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ بيانات الاتصال بـ Supabase غير مكتملة في secrets.toml.")
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"❌ فشل الاتصال بـ Supabase: {e}")
        return None

@st.cache_resource
def init_gemini() -> genai.Client | None:
    if not GEMINI_API_KEY:
        st.error("⚠️ مفتاح GEMINI_API_KEY غير متاح أو يحتوي على رموز غير صالحة.")
        return None
    try:
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"❌ فشل تهيئة عميل Gemini: {e}")
        return None

supabase = init_supabase()
gemini_client = init_gemini()

BRAND_NAME = "خدمات السراغنة للتسويق الرقمي"
BRAND_PHONE = "+212691897126"

SYSTEM_MARKETING_OS = f"""
أنت "المساعد الذكي لـ خدمات السراغنة للتسويق الرقمي".
خبير متخصص في التسويق الإلكتروني، كتابة النصوص الإعلانية (Copywriting)، وتحليل الصور وتطوير البوستر الإعلاني لكافة القطاعات والمشاريع.

القواعد والأسلوب:
1. صغ الإعلانات والنصوص بلغة عربية احترافية أو دارجة مغربية تسويقية جذابة حسب الطلب.
2. اختم كل رد تسويقي بـ:
📲 تواصل معنا عبر الواتساب: {WHATSAPP_LINK} 
📢 خدمات السراغنة للتسويق الرقمي - شريكك للنجاح والتوسع
"""

SECTOR_TEMPLATES = {
    "منتجات تجارية": "خلفية استوديو تصوير منتجات فاخرة، إضاءة احترافية سينمائية، إبراز تفاصيل المنتوج، تصميم إعلاني جذاب.",
    "عقارات وديكور": "واجهة عقار فاخرة وقت الغروب، إضاءة دافئة، مسبح محاط بالنخيل، تصميم هندسي مودرن عالي الجودة.",
    "أطباق ومأكولات": "طبق طعام شهي على طاولة خشبية فاخرة، بخار خفيف يتصاعد، إضاءة مطعم دافئة، زوايا تصوير احترافية.",
    "سيارات": "سيارة رياضية في معرض حديث، إضاءة ليد نيون أنيقة، انعكاسات ناعمة على الهيكل، مظهر رياضي وفخم.",
    "خدمات ومحلات": "محل تجاري عصري ومنظم، إضاءة ترحيبية دافئة، إبراز اسم المحل والخدمات بشكل احترافي ناصع."
}

# ==========================================
# 2. الدوال المساعدة
# ==========================================
def format_arabic_text(text: str) -> str:
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    except Exception:
        return text

def add_watermark(image_bytes, text1=BRAND_NAME, text2=BRAND_PHONE):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    try:
        font_big = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font_big = font_small = ImageFont.load_default()
    
    w, h = img.size
    draw.rectangle([0, h - 100, w, h], fill=(0, 0, 0, 150))
    
    t1_formatted = format_arabic_text(text1)
    t2_formatted = format_arabic_text(text2)
    
    draw.text((20, h - 90), t1_formatted, font=font_big, fill=(255, 255, 255, 255))
    draw.text((20, h - 50), t2_formatted, font=font_small, fill=(255, 255, 0, 255))
    
    buf = io.BytesIO()
    Image.alpha_composite(img, txt).convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()

def create_zip_file(images_list):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i, item in enumerate(images_list):
            zip_file.writestr(f"poster_{i+1}_{item['orig_name']}", item['bytes'])
    zip_buffer.seek(0)
    return zip_buffer

def upload_bytes_to_supabase(image_bytes, filename, mime_type="image/jpeg"):
    if not supabase:
        st.error("⚠️ اتصال Supabase غير متاح.")
        return None
    try:
        path = f"marketing/{filename}"
        supabase.storage.from_("property-images").upload(
            path=path, file=image_bytes, file_options={"content-type": mime_type, "upsert": True}
        )
        return supabase.storage.from_("property-images").get_public_url(path)
    except Exception as e:
        st.error(f"خطأ رفع الصورة: {e}")
        return None

def send_whatsapp_media(image_url: str, caption: str, recipient_number: str):
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN):
        st.warning("⚠️ بيانات الواتساب غير مكتملة")
        return False
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "image",
        "image": {"link": image_url, "caption": caption}
    }
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.status_code == 200
    except Exception as e:
        st.error(f"خطأ في الاتصال بالواتساب: {e}")
        return False

def process_single_image(image_file, sector, user_prompt):
    if not gemini_client:
        st.error("⚠️ عميل Gemini غير متصل.")
        return None, "خطأ اتصال"
    try:
        img_bytes = image_file.getvalue()
        image_part = types.Part.from_bytes(data=img_bytes, mime_type=image_file.type)
        analysis_query = f"القطاع: {sector}. الطلب: {user_prompt}. حلل الصورة وأنشئ وصف إنجليزي لتصميم بوستر إعلاني احترافي."
        res_desc = gemini_client.models.generate_content(model="gemini-2.0-flash", contents=[image_part, analysis_query])
        
        imagen_prompt = f"Commercial banner for {sector}, {res_desc.text}, photorealistic 8k, professional advertising"
        gen_res = gemini_client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=imagen_prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="1:1", output_mime_type="image/jpeg")
        )
        watermarked_bytes = add_watermark(gen_res.generated_images[0].image.image_bytes)
        return watermarked_bytes, res_desc.text
    except Exception as e:
        st.error(f"فشل معالجة الصورة ({image_file.name}): {e}")
        return None, str(e)

def save_to_supabase_logs(sector, message, image_count, content=""):
    if not supabase:
        return
    try:
        supabase.table("instant_ads").insert({
            "sector": sector,
            "message": message,
            "content": content,
            "image_count": image_count,
            "source": f"Sraghna-Marketing-{sector}",
            "status": "completed"
        }).execute()
    except Exception as e:
        st.error(f"خطأ حفظ السجل: {e}")

# ==========================================
# 3. واجهة المستخدم
# ==========================================
st.title("📢 خدمات السراغنة للتسويق الرقمي")
st.caption("المنصة الذكية لصناعة الإعلانات والبوسترات الرقمية لكافة القطاعات والمشاريع")

menu = st.sidebar.radio("📌 القائمة الرئيسية", ["🚀 مولد الإعلانات الشامل", "📸 استوديو التصاميم", "📊 أرشيف الحملات والإحصائيات"])

# --- القسم 1: مولد الإعلانات ---
if menu == "🚀 مولد الإعلانات الشامل":
    st.subheader("📝 إنشاء نص إعلاني وحملة تسويقية متكاملة")
    col_sec1, col_sec2 = st.columns(2)
    with col_sec1:
        sector_text = st.selectbox("اختر قطاع المشروع:", list(SECTOR_TEMPLATES.keys()) + ["خدمات عامة", "أخرى"])
    with col_sec2:
        target_platform = st.multiselect("المنصات المستهدفة للنشر:", ["واتساب", "فيسبوك", "إنستغرام", "تيك توك"], default=["واتساب", "فيسبوك"])

    project_details = st.text_area("أدخل تفاصيل المشروع أو المنتج (الوصف، السعر، المكان، أهم الميزات):", height=130)

    if st.button("✨ توليد الحملة الإعلانية", type="primary"):
        if not project_details:
            st.warning("يرجى كتابة تفاصيل المشروع أولاً.")
        elif not gemini_client:
            st.error("⚠️ لم يتم الاتصال بخدمة Gemini. تحقق من API Key.")
        else:
            with st.status("🧠 الذكاء الاصطناعي يصيغ الحملة الإعلانية...", expanded=True) as status:
                prompt_input = f"المجال: {sector_text}\nالتفاصيل: {project_details}\nالمنصات: {', '.join(target_platform)}\nأنتج نصاً إعلانياً جذاباً مع منشورات جاهزة للنشر وهاشتاغات مناسبة."
                try:
                    res = gemini_client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt_input,
                        config=types.GenerateContentConfig(system_instruction=SYSTEM_MARKETING_OS, temperature=0.3)
                    )
                    final_ad = res.text
                    save_to_supabase_logs(sector=sector_text, message=project_details, image_count=0, content=final_ad)
                    status.update(label="✅ تم إنشاء الحملة بنجاح!", state="complete")

                    st.subheader("📜 النص الإعلاني المقترح:")
                    st.markdown(final_ad)
                    st.link_button("📲 مشاركة عبر الواتساب", WHATSAPP_LINK, type="primary")
                except Exception as e:
                    status.update(label="❌ حدث خطأ أثناء التوليد", state="error")
                    st.error(f"تفاصيل الخطأ: {e}")

# --- القسم 2: الاستوديو ---
elif menu == "📸 استوديو التصاميم":
    st.subheader("📸 معالجة دفعية مع القوالب الجاهزة")
    col_left, col_right = st.columns([1, 1])
    with col_left:
        sector_img = st.selectbox("نوع المشروع:", list(SECTOR_TEMPLATES.keys()))
        prompt_img = st.text_area("التعديلات المطلوب تنفيذها:", value=SECTOR_TEMPLATES[sector_img], height=120)
        recipient_number = st.text_input("رقم واتساب العميل (مع رمز الدولة):", placeholder="+2126XXXXXXXX")
        uploaded_files = st.file_uploader("ارفع الصور (حد أقصى 10)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files and len(uploaded_files) > 10:
            st.warning("تم اختيار أكثر من 10 صور. سيتم معالجة أول 10 فقط.")
            uploaded_files = uploaded_files[:10]
        btn_process = st.button("🚀 معالجة وتوليد جميع الصور", type="primary")

    with col_right:
        st.subheader("🖼️ معرض النتائج")
        if btn_process:
            if not uploaded_files:
                st.warning("⚠️ ارفع صورة واحدة على الأقل.")
            else:
                st.session_state["results_gallery"] = []
                keys_to_delete = [k for k in st.session_state.keys() if k.startswith("url_")]
                for k in keys_to_delete:
                    del st.session_state[k]

                progress_bar = st.progress(0)
                successful_count = 0
                for idx, file in enumerate(uploaded_files):
                    with st.spinner(f"معالجة {file.name} ({idx+1}/{len(uploaded_files)})..."):
                        gen_bytes, desc = process_single_image(file, sector_img, prompt_img)
                        if gen_bytes:
                            st.session_state["results_gallery"].append({"orig_name": file.name, "bytes": gen_bytes, "desc": desc})
                            successful_count += 1
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                if successful_count > 0:
                    save_to_supabase_logs(sector=sector_img, message=prompt_img, image_count=successful_count)
                    st.success(f"🎉 تم توليد {successful_count} صور مع العلامة المائية")

        if "results_gallery" in st.session_state and st.session_state["results_gallery"]:
            zip_data = create_zip_file(st.session_state["results_gallery"])
            st.download_button("📦 تحميل جميع الصور في ملف ZIP واحد", zip_data, "posters_sraghna.zip", "application/zip")
            for index, item in enumerate(st.session_state["results_gallery"]):
                with st.expander(f"الصورة #{index+1} ({item['orig_name']})", expanded=True):
                    st.image(item["bytes"], use_container_width=True)
                    c1, c2 = st.columns(2)
                    if c1.button(f"☁️ حفظ #{index+1}", key=f"save_{index}"):
                        url = upload_bytes_to_supabase(item["bytes"], f"ad_{int(time.time())}_{index}.jpg")
                        if url:
                            st.session_state[f"url_{index}"] = url
                            st.success("تم الحفظ في السحابة!")
                    if c2.button(f"📲 إرسال #{index+1}", key=f"send_{index}"):
                        if not recipient_number:
                            st.error("أدخل رقم واتساب العميل أولاً")
                        else:
                            url = st.session_state.get(f"url_{index}") or upload_bytes_to_supabase(item["bytes"], f"ad_{int(time.time())}_{index}.jpg")
                            if url:
                                if send_whatsapp_media(url, f"📢 {BRAND_NAME}\n{item['desc'][:80]}...", recipient_number):
                                    st.success("تم الإرسال بنجاح!")
                                else:
                                    st.error("فشل الإرسال عبر الواتساب API.")
                            else:
                                st.error("فشل رفع الصورة للخدمة السحابية.")

# --- القسم 3: الأرشيف والإحصائيات ---
elif menu == "📊 أرشيف الحملات والإحصائيات":
    st.subheader("📊 لوحة التحكم والإحصائيات")
    if not supabase:
        st.error("⚠️ لم يتم الاتصال بـ Supabase.")
    else:
        try:
            ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(100).execute()
            if ads_data.data:
                df = pd.DataFrame(ads_data.data)
                col1, col2, col3 = st.columns(3)
                col1.metric("إجمالي الحملات", len(df))
                img_sum = df['image_count'].sum() if 'image_count' in df.columns else 0
                col2.metric("إجمالي الصور", int(img_sum) if pd.notnull(img_sum) else 0)
                top_sector = df['sector'].mode()[0] if ('sector' in df.columns and not df['sector'].dropna().empty) else "-"
                col3.metric("أكثر قطاع نشاطاً", top_sector)

                st.markdown("---")
                if 'sector' in df.columns:
                    sector_list = ["الكل"] + [s for s in df['sector'].dropna().unique()]
                    sector_filter = st.selectbox("فلترة حسب القطاع:", sector_list)
                    if sector_filter != "الكل":
                        df = df[df['sector'] == sector_filter]

                cols_to_display = [c for c in ['created_at', 'sector', 'image_count', 'status', 'source'] if c in df.columns]
                st.dataframe(df[cols_to_display], use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 تصدير CSV", csv, "archive_sraghna.csv", "text/csv")
            else:
                st.info("لا توجد سجلات بعد.")
        except Exception as e:
            st.error(f"خطأ قراءة الأرشيف: {e}")
