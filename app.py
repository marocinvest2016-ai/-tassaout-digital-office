import io
import time
import zipfile
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
import requests
import streamlit as st
from supabase import create_client

# ==========================================
# 1. إعدادات الصفحة والأسرار
# ==========================================
st.set_page_config(page_title="خدمات السراغنة للتسويق الرقمي والتجاري", page_icon="🏡", layout="wide")

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

# ==========================================
# 2. الوكيل الأعظم - Super Agent v7.1
# ==========================================
MASTER_SYSTEM_PROMPT = """
أنت "الوكيل الأعظم لخدمات السراغنة". أنت ذكاء اصطناعي فائق متعدد التخصصات.
لديك خبرة عميقة في:
1. الدعم الفني: هندسة، برمجة، تحليل بيانات
2. الدعم الجمالي: تصوير، ديكور، تصميم إعلانات وتسويق
3. الدعم الفكري: استراتيجيات أعمال، صياغة محتوى تجاري
4. الدعم القانوني والعدلي: محامي، عدل، صياغة العقود المغربية والعقارية

القاعدة الذهبية: حلل طلب المستخدم بدقة، وقم بتغطية كافة الجوانب المطلوبة (سواء كانت هندسية، قانونية، تسويقية أو تصويرية) في إجابة واحدة متكاملة ومنظمة.
أجب دائماً باللغة العربية الفصحى بأسلوب احترافي، مباشر، ومرتب.
"""

def save_agent_chat(task, answer):
    """حفظ محادثات الوكيل الأعظم في قاعدة البيانات"""
    try:
        supabase.table("agent_logs").insert({
            "task": task, 
            "answer": answer, 
            "source": "SuperAgent-v7.1"
        }).execute()
    except Exception:
        pass

# ==========================================
# 3. دوال المعالجة والواتساب
# ==========================================
def add_watermark(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    
    # دعم الخط العربي Cairo إذا توفر، وإلا الافتراضي
    try:
        font_big = ImageFont.truetype("Cairo-Bold.ttf", 45)
        font_small = ImageFont.truetype("Cairo-Bold.ttf", 32)
    except:
        try:
            font_big = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 28)
        except:
            font_big = font_small = ImageFont.load_default()
            
    w, h = img.size
    draw.rectangle([0, h - 100, w, h], fill=(0, 0, 0, 150))
    draw.text((20, h - 90), BRAND_NAME, font=font_big, fill=(255, 255, 255, 255))
    draw.text((20, h - 45), BRAND_PHONE, font=font_small, fill=(255, 255, 0, 255))
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

def upload_bytes_to_supabase(image_bytes, filename):
    try:
        path = f"marketing/{filename}"
        supabase.storage.from_("property-images").upload(path=path, file=image_bytes, file_options={"content-type": "image/jpeg", "upsert": True})
        return supabase.storage.from_("property-images").get_public_url(path)
    except Exception as e:
        st.error(f"خطأ رفع الصورة: {e}")
        return None

def send_whatsapp_media(image_url: str, caption: str, recipient_number: str):
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN):
        st.warning("⚠️ بيانات الواتساب غير مكتملة")
        return False
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {"messaging_product": "whatsapp", "to": recipient_number, "type": "image", "image": {"link": image_url, "caption": caption}}
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    return requests.post(url, headers=headers, json=payload).status_code == 200

def send_whatsapp_text(text: str, recipient_number: str):
    if not (WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN):
        return False
    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    payload = {"messaging_product": "whatsapp", "to": recipient_number, "type": "text", "text": {"body": text}}
    headers = {"Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    return requests.post(url, headers=headers, json=payload).status_code == 200

def save_to_supabase_logs(sector, message, image_count):
    try:
        supabase.table("instant_ads").insert({"sector": sector, "message": message, "image_count": image_count, "source": "Sraghna-Platform-v7.1"}).execute()
    except Exception as e:
        st.error(f"خطأ حفظ السجل: {e}")

# ==========================================
# 4. واجهة المستخدم الرئيسية
# ==========================================
st.title("🏡 المنصة المتكاملة للتسويق العقاري والواتساب")
menu = st.sidebar.radio("📌 القائمة الرئيسية", ["🤖 الوكيل الأعظم", "🚀 توليد إعلان سريع", "📸 استوديو الصور", "📊 الأرشيف"])

# --- 1. الوكيل الأعظم (Super Agent v7.1) ---
if menu == "🤖 الوكيل الأعظم":
    st.subheader("🧠 الوكيل الأعظم - عقل ذكي واحد لكل التخصصات")

    with st.expander("⚙️ لوحة تحكم الوكيل - التعليمات المتقدمة", expanded=True):
        st.info("هنا يمكنك توجيه الوكيل واختيار النمط أو تقمص الشخصية قبل طرح السؤال")

        col1, col2 = st.columns(2)
        with col1:
            agent_mode = st.selectbox(
                "1. اختر نمط الوكيل:",
                ["عام وشامل", "مهندس فقط", "محامي وعدل فقط", "مسوق عقاري فقط", "مصمم ديكور فقط", "شخصية مخصصة"]
            )
        with col2:
            if agent_mode == "شخصية مخصصة":
                custom_persona = st.text_input("اكتب الشخصية:", "Zaha Hadid")
            else:
                custom_persona = ""

        custom_instructions = st.text_area(
            "2. تعليمات إضافية للوكيل:",
            placeholder="مثال: ركز على الجانب الاستثماري، أعطي أرقام وتكلفة تقريبية...",
            height=80
        )

    base_prompt = MASTER_SYSTEM_PROMPT
    mode_prompts = {
        "عام وشامل": "كن شاملاً وغطي كل الجوانب.",
        "مهندس فقط": "تجاهل باقي التخصصات. ركز فقط على الهندسة والتصميم والتكلفة.",
        "محامي وعدل فقط": "تجاهل باقي التخصصات. ركز فقط على الجانب القانوني والشرعي والعقود.",
        "مسوق عقاري فقط": "تجاهل باقي التخصصات. ركز فقط على التسويق والإعلانات وسيكولوجية البيع.",
        "مصمم ديكور فقط": "تجاهل باقي التخصصات. ركز فقط على الديكور والألوان وتوزيع الأثاث."
    }

    dynamic_prompt = base_prompt + "\n\n" + mode_prompts.get(agent_mode, "")
    if custom_persona:
        dynamic_prompt += f"\n\nمهم جداً: تقمص شخصية {custom_persona} بأسلوبها وطريقتها."
    if custom_instructions:
        dynamic_prompt += f"\n\nتعليمات إضافية: {custom_instructions}"

    st.markdown("---")
    st.markdown("**أمثلة سريعة:**")
    cols = st.columns(3)
    with cols[0]:
        if st.button("🏗️ هندسة + 🎨 تصميم"):
            st.session_state.q = "صمم لي واجهة فيلا مودرن بمساحة 300م في مراكش مع رؤية إضاءة ليلية."
    with cols[1]:
        if st.button("⚖️ قانون + 📢 تسويق"):
            st.session_state.q = "ما هي أهم الشروط لعقد بيع بقعة أرضية؟ وأعطني خطة تسويقية لبيعها بسرعة."
    with cols[2]:
        if st.button("🏡 استثمار شامل"):
            st.session_state.q = "عندي أرض تجارية بقلعة السراغنة أريد استغلالها: اعطني تصوراً معمارياً، البنود القانونية، وخطة تسويق."

    user_task = st.text_area("اطرح أي سؤال أو مهمة متكاملة:", value=st.session_state.get("q", ""), height=150)
    client_whatsapp = st.text_input("رقم واتساب لإرسال التقرير (اختياري)", placeholder="+2126XXXXXXXX")

    if st.button("⚡ استشر الوكيل الأعظم", type="primary", use_container_width=True):
        if user_task:
            with st.spinner("الوكيل الأعظم يحلل ويستعد لتقديم التقرير الشامل..."):
                messages = [
                    {"role": "system", "content": dynamic_prompt},
                    {"role": "user", "content": user_task}
                ]
                try:
                    response = groq_client.chat.completions.create(
                        model="llama-3.1-70b-versatile", messages=messages, temperature=0.6, max_tokens=1500
                    )
                    result = response.choices[0].message.content
                except Exception as e:
                    result = f"حدث خطأ: {e}"

                save_agent_chat(user_task, result)

                st.markdown("### 📊 تقرير الوكيل الأعظم:")
                st.markdown(result)
                st.download_button("📄 تحميل التقرير (TXT)", result, "super_agent_report.txt")

                if client_whatsapp:
                    if send_whatsapp_text(result[:4096], client_whatsapp):
                        st.success("تم إرسال التقرير بنجاح عبر الواتساب!")
                    else:
                        st.error("فشل إرسال التقرير عبر الواتساب.")
        else:
            st.warning("الرجاء كتابة السؤال أو المهمة أولاً.")

# --- 2. توليد الإعلان السريع ---
elif menu == "🚀 توليد إعلان سريع":
    st.subheader("✨ إنتاج النص الإعلاني المباشر")
    title = st.text_input("عنوان العقار", "شقة للبيع بالسرغينة")
    price = st.text_input("الثمن", "400,000 درهم")
    details = st.text_area("التفاصيل", "شقة مشمسة، 3 غرف، صالون ومطبخ.")
    if st.button("⚡ توليد الإعلان", type="primary"):
        prompt = f"اكتب إعلان تسويقي تجاري وجذاب لعقار: العنوان: {title}, الثمن: {price}, التفاصيل: {details}"
        messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
        try:
            response = groq_client.chat.completions.create(model="llama-3.1-70b-versatile", messages=messages, temperature=0.6, max_tokens=1000)
            ad_text = response.choices[0].message.content
        except Exception as e:
            ad_text = f"خطأ: {e}"
        st.text_area("الإعلان الجاهز:", ad_text, height=200)

# --- 3. استوديو الصور ---
elif menu == "📸 استوديو الصور":
    st.subheader("🖼️ معالجة دفعية وإضافة العلامة المائية")
    uploaded_files = st.file_uploader("ارفع صور العقار", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    recipient_number = st.text_input("رقم واتساب العميل لإرسال الصور", placeholder="+2126XXXXXXXX")
    if st.button("🚀 معالجة الصور"):
        if uploaded_files:
            st.session_state["results_gallery"] = []
            for file in uploaded_files:
                gen_bytes = add_watermark(file.getvalue())
                st.session_state["results_gallery"].append({"orig_name": file.name, "bytes": gen_bytes})
            save_to_supabase_logs("عقارات", "معالجة صور دفعية", len(uploaded_files))
            st.success(f"تمت معالجة {len(uploaded_files)} صور بنجاح")

            zip_data = create_zip_file(st.session_state["results_gallery"])
            st.download_button("📦 تحميل الكل (ZIP)", zip_data, "posters.zip")

            for i, item in enumerate(st.session_state["results_gallery"]):
                st.image(item["bytes"], caption=f"صورة {i+1}")
                if st.button(f"📲 إرسال الصورة {i+1}", key=f"send_{i}"):
                    url = upload_bytes_to_supabase(item["bytes"], f"ad_{int(time.time())}_{i}.jpg")
                    if send_whatsapp_media(url, f"📢 {BRAND_NAME}", recipient_number):
                        st.success("تم الإرسال بنجاح عبر الواتساب")
        else:
            st.warning("الرجاء رفع صورة واحدة على الأقل")

# --- 4. الأرشيف ---
elif menu == "📊 الأرشيف":
    st.subheader("📊 أرشيف العمليات والسجلات")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).limit(50).execute()
        if ads_data.data:
            df = pd.DataFrame(ads_data.data)
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 تحميل الأرشيف CSV", df.to_csv(index=False).encode('utf-8'), "archive.csv", mime="text/csv")
        else:
            st.info("لا توجد سجلات مسجلة بعد.")
    except Exception as e:
        st.error(f"خطأ في جلب الأرشيف: {e}")
