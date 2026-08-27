import io
import time
from google import genai
from google.genai import types
import requests
import streamlit as st
from supabase import create_client

# ==========================================
# 1. التهيئة والأسرار (Secrets)
# ==========================================
st.set_page_config(
    page_title="استوديو المصور #15 - Bernard Claude",
    page_icon="📸",
    layout="wide",
)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_ACCESS_TOKEN = st.secrets.get("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_BUSINESS_NUMBER = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
WHATSAPP_API_VERSION = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

# تهيئة عميل Supabase وعميل Gemini
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================
# 2. الدوال المساعدة (Helper Functions)
# ==========================================
def fetch_properties():
  """جلب قائمة العقارات من جدول properties في Supabase."""
  try:
    response = (
        supabase.table("properties")
        .select("id, title, location, price")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data if response.data else []
  except Exception as e:
    st.error(f"خطأ في جلب العقارات: {e}")
    return []


def upload_bytes_to_supabase(image_bytes, filename, mime_type="image/jpeg"):
  """رفع صورة إلى Supabase Storage و إرجاع الرابط العام."""
  try:
    path = f"generated/{filename}"
    supabase.storage.from_("property-images").upload(
        path=path,
        file=image_bytes,
        file_options={"content-type": mime_type, "upsert": "true"},
    )
    public_url = supabase.storage.from_("property-images").get_public_url(
        path
    )
    return public_url
  except Exception as e:
    st.error(f"خطأ أثناء رفع الصورة إلى Supabase: {e}")
    return None


def update_property_image_in_db(property_id, image_url):
  """تحديث رابط الصورة في جدول properties."""
  try:
    supabase.table("properties").update({"image_url": image_url}).eq(
        "id", property_id
    ).execute()
    return True
  except Exception as e:
    st.error(f"خطأ أثناء تحديث بيانات العقار: {e}")
    return False


def generate_enhanced_prompt(image_bytes, mime_type, user_prompt):
  """1.

  تحليل الصورة الأصلية والبرومبت باستخدام Gemini 2.0 Flash لتوليد وصف دقيق.
  """
  image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

  analysis_prompt = f"""
    أنت مصمم معاري ومصور عقارات محترف. 
    قم بتحليل هذه الصورة وتطوير الوصف التالي لإعادة توليد صورة عقارية فاخرة وعالية الجودة:
    الطلب المطلوب: {user_prompt}
    
    اكتب وصفاً باللغة الإنجليزية مخصصاً لنظام التوليد Imagen يصف المشهد، الإضاءة، الأثاث، الديكور والبيئة المحيطة بدقة عالية.
    """

  response = gemini_client.models.generate_content(
      model="gemini-2.0-flash", contents=[image_part, analysis_prompt]
  )
  return response.text


def generate_imagen_photo(enhanced_description):
  """2.

  توليد صورة جديدة باستخدام Imagen 3.
  """
  prompt_for_imagen = f"Professional real estate photography, high-end interior and architectural design, 8k resolution, photorealistic, {enhanced_description}"

  result = gemini_client.models.generate_images(
      model="imagen-3.0-generate-002",
      prompt=prompt_for_imagen,
      config=types.GenerateImagesConfig(
          number_of_images=1,
          aspect_ratio="4:3",
          output_mime_type="image/jpeg",
      ),
  )
  return result.generated_images[0].image.image_bytes


def send_whatsapp_image(image_url, caption):
  """إرسال الصورة عبر WhatsApp Business API."""
  if not (
      WHATSAPP_PHONE_NUMBER_ID
      and WHATSAPP_ACCESS_TOKEN
      and WHATSAPP_BUSINESS_NUMBER
  ):
    st.warning("بيانات WhatsApp API غير مكتملة في `.streamlit/secrets.toml`")
    return False

  url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
  payload = {
      "messaging_product": "whatsapp",
      "to": WHATSAPP_BUSINESS_NUMBER,
      "type": "image",
      "image": {"link": image_url, "caption": caption},
  }
  headers = {
      "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
      "Content-Type": "application/json",
  }

  res = requests.post(url, headers=headers, json=payload)
  return res.status_code == 200


# ==========================================
# 3. واجهة المستخدم (Streamlit Interface)
# ==========================================
st.title("📸 استوديو المصور #15 - Bernard Claude AI Studio")
st.markdown("تعديل وتحسين الصور العقارية باستخدام **Gemini 2.0 & Imagen 3**")

col_input, col_output = st.columns([1, 1])

with col_input:
  st.subheader("1. اختار العقار ورفع الصورة")

  # 1. اختيار العقار من Supabase
  properties_list = fetch_properties()
  selected_property_id = None
  selected_property_title = ""

  if properties_list:
    prop_options = {
        f"{p.get('title', 'بدون عنوان')} - [{p.get('location', '')}] ({p.get('price', '')} DH)": p[
            "id"
        ]
        for p in properties_list
    }
    selected_option = st.selectbox(
        "اختر العقار المرتبط (اختياري):", ["-- بدون ربط --"] + list(prop_options.keys())
    )
    if selected_option != "-- بدون ربط --":
      selected_property_id = prop_options[selected_option]
      selected_property_title = selected_option
  else:
    st.info("لم يتم العثور على عقارات في جدول properties أو الجدول فارغ.")

  # 2. رفع الصورة
  uploaded_file = st.file_uploader(
      "ارفع صورة العقار الأصلية", type=["jpg", "jpeg", "png"]
  )

  # 3. إدخال البرومبت
  user_prompt = st.text_area(
      "أدخل التعديلات المطلوبة (مثال: اجعل الواجهة وقت الغروب مع إضاءة دافئة ومسبح محاط بالنخيل)",
      height=120,
  )

  btn_generate = st.button("🚀 توليد الصورة الذكية", type="primary")

with col_output:
  st.subheader("2. المعاينة والنتائج")

  if btn_generate:
    if not uploaded_file or not user_prompt:
      st.warning("⚠️ يرجى رفع صورة وإدخال البرومبت أولاً.")
    else:
      img_bytes = uploaded_file.getvalue()
      mime_type = uploaded_file.type

      # 1. تحليل الصورة بواسطة Gemini 2.0 Flash
      with st.spinner("🔍 1/2 Gemini 2.0 Flash يقدم تحليلاً للمشهد..."):
        enhanced_desc = generate_enhanced_prompt(
            img_bytes, mime_type, user_prompt
        )
        st.expander("📝 الوصف المولد من Gemini:").write(enhanced_desc)

      # 2. توليد الصورة بواسطة Imagen 3
      with st.spinner("🎨 2/2 Imagen 3 يقوم بتوليد الصورة العقارية..."):
        gen_img_bytes = generate_imagen_photo(enhanced_desc)
        st.session_state["gen_img_bytes"] = gen_img_bytes
        st.session_state["enhanced_desc"] = enhanced_desc
        st.success("✅ تم التوليد بنجاح!")

  if "gen_img_bytes" in st.session_state:
    st.image(
        st.session_state["gen_img_bytes"],
        caption="الصورة المولدة بالذكاء الاصطناعي",
        use_container_width=True,
    )

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
      if st.button("☁️ حفظ في Supabase Storage"):
        filename = f"property_{int(time.time())}.jpg"
        pub_url = upload_bytes_to_supabase(
            st.session_state["gen_img_bytes"], filename
        )
        if pub_url:
          st.session_state["last_pub_url"] = pub_url
          st.success("تم الحفظ بنجاح في Storage!")
          st.code(pub_url)

          # تحديث جدول properties إذا كان العقار محدداً
          if selected_property_id:
            if update_property_image_in_db(selected_property_id, pub_url):
              st.success(f"تم ربط الصورة بالعقار رقم #{selected_property_id}")

    with col_btn2:
      if st.button("📲 إرسال إلى الواتساب"):
        if "last_pub_url" not in st.session_state:
          filename = f"property_{int(time.time())}.jpg"
          pub_url = upload_bytes_to_supabase(
              st.session_state["gen_img_bytes"], filename
          )
          st.session_state["last_pub_url"] = pub_url
        else:
          pub_url = st.session_state["last_pub_url"]

        if pub_url:
          caption = f"📸 صورة عقارية جديدة (Bernard Claude Studio)\n{selected_property_title}"
          if send_whatsapp_image(pub_url, caption):
            st.success("📲 تم إرسال الصورة بنجاح عبر الواتساب!")
          else:
            st.error("فشل الإرسال عبر الواتساب.")
