import io
import time
import zipfile
import pandas as pd
import gdown
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
import requests
import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timezone

# إعداد الصفحة
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
        return ImageFont.truetype("Cairo-Bold.ttf", 40), ImageFont.truetype("Cairo-Bold.ttf", 28)
    except: 
        return ImageFont.load_default(), ImageFont.load_default()

supabase = init_supabase()
groq_client = init_groq()
font_big, font_small = load_ar_font()

BRAND_NAME = "وكالة تساوت للإنتاج الرقمي"
BRAND_PHONE = "+212691897126"

MASTER_SYSTEM_PROMPT = """أنت "وكيل تساوت للإنتاج الرقمي"... قدم "ثلاثية القيمة" في الختام."""

def run_super_agent(user_task: str):
    messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}, {"role": "user", "content": user_task}]
    for model_name in ["qwen/qwen3.8-27b", "openai/gpt-oss-120b"]:
        try:
            response = groq_client.chat.completions.create(model=model_name, messages=messages, temperature=0.6, max_tokens=2000)
            return response.choices[0].message.content
        except: 
            continue
    return "❌ تعذر الاتصال بنماذج النص."

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

def upload_image_to_supabase_storage(image_bytes, filename):
    try:
        path = f"tassaout_media/{int(time.time())}_{filename}"
        supabase.storage.from_("property-images").upload(path=path, file=image_bytes, file_options={"content-type": "image/jpeg", "upsert": True})
        return supabase.storage.from_("property-images").get_public_url(path)
    except Exception as e: 
        st.error(f"خطأ رفع الصورة: {e}")
        return None

def format_whatsapp_number(number): 
    return number.replace("+", "").replace(" ", "").replace("-", "")

def save_lead(phone, title, ad, img_url):
    try:
        supabase.table("leads").insert({
            "phone_number": format_whatsapp_number(phone),
            "property_title": title,
            "ad_content": ad[:500],
            "image_url": img_url,
            "status": "جديد",
            "source": "WhatsApp Send v10.5",
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        return True
    except Exception as e:
        st.error(f"خطأ حفظ Lead: {e}")
        return False

def send_whatsapp_media(image_url: str, caption: str, recipient_number: str, property_title: str):
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN): 
        return False, "بيانات واتساب ناقصة."
    recipient_number = format_whatsapp_number(recipient_number)
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {"messaging_product": "whatsapp", "to": recipient_number, "type": "image", "image": {"link": image_url, "caption": caption}}
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            save_lead(recipient_number, property_title, caption, image_url)
            return True, "تم الإرسال وحفظ الـ Lead بنجاح!"
        else:
            return False, f"خطأ واتساب: {response.text}"
    except Exception as e: 
        return False, f"خطأ شبكي: {e}"

# ========== القائمة الجانبية (Navigation) ==========
st.sidebar.title("📌 القائمة الرئيسية")
menu = st.sidebar.radio("اختر القسم:", [
    "🧠 وكيل تساوت الرقمي", 
    "🚀 توليد إعلان سريع", 
    "🔍 البحث والفلترة المتقدمة", 
    "📸 استوديو التصوير والمعاينة", 
    "👥 إدارة العملاء Leads", 
    "📊 الأرشيف السحابي"
])

if "last_ad" not in st.session_state: st.session_state["last_ad"] = ""
if "last_title" not in st.session_state: st.session_state["last_title"] = ""

# ==========================================
# 1. وكيل تساوت الرقمي
# ==========================================
if menu == "🧠 وكيل تساوت الرقمي":
    st.subheader("🧠 وكيل تساوت للإنتاج الرقمي")
    user_task = st.text_area("اطرح أي مهمة استراتيجية:", height=180)
    if st.button("⚡ تنفيذ المهمة", type="primary", use_container_width=True):
        if user_task:
            with st.spinner("جاري المعالجة..."):
                result = run_super_agent(user_task)
                st.session_state["last_ad"] = result
                st.markdown("### 📊 تقرير وكيل تساوت:")
                st.markdown(result)
                st.download_button("📄 تحميل التقرير", result, f"tassaout_report_{int(time.time())}.txt")

# ==========================================
# 2. توليد إعلان سريع
# ==========================================
elif menu == "🚀 توليد إعلان سريع":
    st.subheader("✨ إنتاج الإعلان + الربط التلقائي مع قاعدة البيانات")
    col1, col2 = st.columns(2)
    with col1: 
        title = st.text_input("عنوان المشروع", "شقق عصرية للبيع بقلعة السراغنة")
    with col2: 
        price = st.text_input("الثمن", "من 40 إلى 64 مليون سنتيم")
    details = st.text_area("تفاصيل", "الطابق الأول، مساحة من 70 إلى 120+ متر.")
    st.session_state["last_title"] = title

    if st.button("⚡ توليد الإعلان وحفظه", type="primary", use_container_width=True):
        prompt = f"اكتب إعلان تسويقي احترافي لبيع الشقق: {title}, {price}, {details}. اختمه برقم الهاتف {BRAND_PHONE}"
        with st.spinner("جاري الصياغة..."):
            ad_text = run_super_agent(prompt)
            st.session_state["last_ad"] = ad_text
        st.text_area("الإعلان الجاهز:", st.session_state["last_ad"], height=250)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📋 نسخ الإعلان", use_container_width=True):
                st.code(st.session_state["last_ad"], language="text")
                st.success("✅ حدد النص وأشر عليه بـ Ctrl+C للنسخ")
        with col_btn2: 
            st.download_button("📄 تحميل", st.session_state["last_ad"], "tassaout_ad.txt", use_container_width=True)

        try:
            supabase.table("instant_ads").insert({
                "category": "عقارات", 
                "city": "قلعة السراغنة",
                "content": title,
                "message": ad_text, 
                "price": 500000, 
                "source": "Tassaout-v10.5", 
                "created_at": datetime.now(timezone.utc).isoformat()
            }).execute()
            st.success("✅ تم الحفظ السحابي في instant_ads!")
        except Exception as e: 
            st.error(f"خطأ حفظ: {e}")

# ==========================================
# 3. البحث والفلترة المتقدمة (Supabase RPC)
# ==========================================
elif menu == "🔍 البحث والفلترة المتقدمة":
    st.subheader("🔍 محرك البحث والفلترة الذكي (قاعدة البيانات الفورية)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_query = st.text_input("🔍 بحث نصي", placeholder="ابحث عن عقار، خدمة...")
    with col2:
        category_filter = st.text_input("🏷️ التصنيف", placeholder="مثال: عقارات، سيارات...")
    with col3:
        city_filter = st.text_input("📍 المدينة", placeholder="مثال: قلعة السراغنة، مراكش...")
    with col4:
        max_price = st.number_input("💰 أقصى سعر (درهم)", min_value=0.0, value=0.0, step=1000.0)

    if st.button("بحث وتصفية متقدمة", type="primary"):
        params = {
            "query_text": search_query if search_query else None,
            "p_category": category_filter if category_filter else None,
            "p_city": city_filter if city_filter else None,
            "p_max_price": max_price if max_price > 0 else None
        }
        
        response = supabase.rpc("search_all_services", params).execute()
        ads = response.data
        
        if ads:
            st.success(f"تم العثور على {len(ads)} نتيجة مطابقة.")
            
            df = pd.DataFrame(ads)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 تحميل النتائج الحالية (CSV)",
                data=csv_data,
                file_name="sraghna_search_results.csv",
                mime="text/csv"
            )
            
            for ad in ads:
                with st.container():
                    st.markdown("---")
                    image_url = ad.get("image_url")
                    if image_url:
                        st.image(image_url, width=350)
                    
                    st.subheader(ad.get("content", "بدون عنوان"))
                    st.write(ad.get("message", ""))
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.info(f"📍 المدينة: {ad.get('city', 'غير محدد')}")
                    with col_b:
                        st.warning(f"🏷️ التصنيف: {ad.get('category', 'عام')}")
                    with col_c:
                        price_val = ad.get('price')
                        st.success(f"💰 السعر: {price_val if price_val else 'غير متوفر'} درهم")
                        
                    phone = ad.get("phone", BRAND_PHONE)
                    if phone:
                        whatsapp_link = f"https://wa.me/{format_whatsapp_number(phone)}?text=مرحباً، أنا مهتم بإعلانكم: {ad.get('content', '')}"
                        st.markdown(f"🟢 [تواصل عبر الواتساب مباشرة]({whatsapp_link})", unsafe_allow_html=True)
                        
                    st.caption(f"📅 تاريخ النشر: {ad.get('created_at', '')}")
        else:
            st.warning("لم يتم العثور على أي نتائج تطابق بحثك.")

# ==========================================
# 4. استوديو التصوير والمعاينة
# ==========================================
elif menu == "📸 استوديو التصوير والمعاينة":
    st.subheader("📸 استوديو تساوت الميداني وإرسال الوسائط")
    if st.session_state["last_ad"]:
        st.info(f"📌 سيتم استخدام آخر إعلان مولد: {st.session_state['last_title']}")

    tab_cam, tab_up = st.tabs(["📷 كاميرا مباشرة", "📁 رفع متعدد"])
    processed_items = []
    
    with tab_cam:
        camera_file = st.camera_input("التقط صورة")
        if camera_file:
            cam_bytes = camera_file.getvalue()
            processed_cam_bytes = add_watermark(cam_bytes)
            pub_cam_url = upload_image_to_supabase_storage(processed_cam_bytes, "mobile_capture.jpg")
            processed_items.append({"orig_name": "mobile_capture.jpg", "bytes": processed_cam_bytes, "url": pub_cam_url})
            
    with tab_up:
        uploaded_files = st.file_uploader("اختر الصور", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files:
            for f in uploaded_files:
                f_bytes = f.getvalue()
                processed_bytes = add_watermark(f_bytes)
                pub_url = upload_image_to_supabase_storage(processed_bytes, f.name)
                processed_items.append({"orig_name": f.name, "bytes": processed_bytes, "url": pub_url})

    if processed_items: 
        st.session_state["results_gallery"] = processed_items

    if "results_gallery" in st.session_state and st.session_state["results_gallery"]:
        st.markdown("---")
        st.subheader("📤 الإرسال الفوري عبر WhatsApp API")
        recipient_phone = st.text_input("رقم المستلم (مثال: 212600000000)", value="212")
        default_caption = st.session_state["last_ad"] if st.session_state["last_ad"] else f"🏡 عرض من {BRAND_NAME}\n{BRAND_PHONE}"
        wa_caption = st.text_area("نص الواتساب المصاحب", value=default_caption, height=150)

        for idx, item in enumerate(st.session_state["results_gallery"]):
            col_img, col_btn = st.columns([2, 1])
            with col_img: 
                st.image(item["bytes"], caption=f"صورة {idx+1}")
            with col_btn:
                if st.button(f"📲 إرسال الصورة {idx+1} + حفظ Lead", key=f"wa_btn_{idx}"):
                    if item["url"]:
                        with st.spinner("جاري الإرسال عبر واتساب..."):
                            success, msg = send_whatsapp_media(item["url"], wa_caption, recipient_phone, st.session_state["last_title"])
                            if success:
                                st.success(msg)
                            else:
                                st.error(msg)
                    else: 
                        st.error("رابط الصورة غير متوفر.")

# ==========================================
# 5. إدارة العملاء Leads
# ==========================================
elif menu == "👥 إدارة العملاء Leads":
    st.subheader("👥 قمع المبيعات: إدارة العملاء المحتملين (Leads)")
    try:
        leads_data = supabase.table("leads").select("*").order("created_at", desc=True).execute()
        if leads_data.data:
            df = pd.DataFrame(leads_data.data)
            st.metric("إجمالي الـ Leads المسجلة", len(df))

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                status_filter = st.selectbox("فلترة حسب الحالة", ["الكل"] + df["status"].unique().tolist())
            with col_f2:
                search_query_leads = st.text_input("بحث برقم الهاتف أو المحتوى", placeholder="أدخل رقم الهاتف...")

            if status_filter != "الكل": 
                df = df[df["status"] == status_filter]
            
            if search_query_leads:
                df = df[df["phone_number"].str.contains(search_query_leads, na=False) | df["ad_content"].str.contains(search_query_leads, na=False)]

            st.write(f"النتائج المعروضة: {len(df)}")

            for idx, row in df.iterrows():
                with st.expander(f"📞 {row['phone_number']} | المشروع: {row.get('property_title', 'عام')} | الحالة: {row['status']}"):
                    col_info, col_action = st.columns([2, 1])
                    with col_info:
                        st.write(f"**التاريخ:** {row['created_at']}")
                        st.write(f"**المصدر:** {row['source']}")
                        st.write(f"**محتوى الإعلان:** {row['ad_content']}")
                        if row.get('image_url'):
                            st.image(row['image_url'], width=200)
                    with col_action:
                        statuses = ["جديد", "تم التواصل", "معاينة", "مهتم", "تم البيع", "بارد"]
                        current_index = statuses.index(row['status']) if row['status'] in statuses else 0
                        new_status = st.selectbox("تحديث الحالة", statuses, index=current_index, key=f"status_select_{row['id']}")
                        
                        if st.button("💾 حفظ التحديث", key=f"update_btn_{row['id']}"):
                            if new_status == row['status']:
                                st.info("ℹ️ لم تقم بأي تغيير على الحالة الحالية.")
                            else:
                                try:
                                    supabase.table("leads").update({
                                        "status": new_status, 
                                        "last_contact_at": datetime.now(timezone.utc).isoformat()
                                    }).eq("id", row['id']).execute()
                                    st.success("✅ تم تحديث حالة الـ Lead بنجاح!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"خطأ في التحديث: {e}")
        else: 
            st.info("لا توجد Leads بعد. ابدأ بالإرسال الفوري من الاستوديو.")
    except Exception as e: 
        st.error(f"خطأ جلب Leads: {e}")

# ==========================================
# 6. الأرشيف السحابي
# ==========================================
elif menu == "📊 الأرشيف السحابي":
    st.subheader("📊 أرشيف Supabase (جدول instant_ads)")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(100).execute()
        if ads_data.data: 
            st.dataframe(pd.DataFrame(ads_data.data), use_container_width=True)
            st.metric("إجمالي السجلات المعروضة", len(ads_data.data))
        else: 
            st.info("لا توجد سجلات في الأرشيف حالياً.")
    except Exception as e: 
        st.error(f"خطأ جلب الأرشيف: {e}")
