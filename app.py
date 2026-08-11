import os
import streamlit as st
from google import genai
from supabase import create_client, Client

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام الإعلانات السيادي", page_icon="👑", layout="centered"
)

# 1. جلب المفاتيح من Streamlit Secrets أو متغيرات البيئة
gemini_key = (
    st.secrets.get("GEMINI_API_KEY")
    or st.secrets.get("GOOGLE_API_KEY")
    or os.environ.get("GEMINI_API_KEY")
)
supabase_url = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
supabase_key = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")

# التحقق من توفر المفاتيح الأساسية
if not gemini_key:
    st.error(
        "❌ مفتاح Gemini API غير موجود في إعدادات Secrets. يرجى إضافته باسم"
        " GEMINI_API_KEY"
    )
    st.stop()

if not supabase_url or not supabase_key:
    st.error("❌ مفاتيح Supabase غير مكتملة في إعدادات Secrets.")
    st.stop()

# تهيئة العملاء (Clients)
client = genai.Client(api_key=gemini_key)
supabase: Client = create_client(supabase_url, supabase_key)


def create_and_save_ad(prompt):
  try:
    with st.spinner("🤖 جاري توليد الإعلان عبر الذكاء الاصطناعي..."):
      # توليد المحتوى باستخدام نموذج Gemini الحديث
      response = client.models.generate_content(
          model="gemini-2.0-flash",
          contents=(
              f"قم بصياغة إعلان عقاري أو تجاري جذاب وقصير بناءً على: {prompt}."
              " أعطني العنوان في السطر الأول، وباقي التفاصيل في المحتوى."
          ),
      )

      full_text = response.text
      lines = full_text.strip().split("\n")
      title = lines[0] if lines else "إعلان جديد"
      content = "\n".join(lines[1:]) if len(lines) > 1 else full_text

    with st.spinner("💾 جاري الحفظ في قاعدة بيانات Supabase..."):
      # حفظ الإعلان في جدول ads
      data = {"title": title, "content": content}
      result = supabase.table("ads").insert(data).execute()

      if result:
        st.success("✨ تم توليد ونشر الإعلان بنجاح!")
        st.rerun()

  except Exception as e:
    st.error(f"حدث خطأ أثناء التنفيذ: {e}")


# --- واجهة التطبيق ---
st.markdown(
    "<h1 style='text-align: center;'>نظام الإعلانات السيادي 👑</h1>",
    unsafe_allow_html=True,
)
st.subheader("🤖 توليد إعلان فوري")

user_input = st.text_area(
    "أدخل تفاصيل أو فكرة الإعلان:",
    placeholder=(
        "مثال: شقة للبيع في القليعة بمساحة واسعة وبسعر مناسب..."
    ),
)

col1, col2 = st.columns([1, 1])
with col1:
  if st.button("توليد ونشر الإعلان فوراً", use_container_width=True):
    if user_input.strip():
      create_and_save_ad(user_input)
    else:
      st.warning("⚠️ الرجاء إدخال تفاصيل الإعلان أولاً.")

with col2:
  if st.button("🔄 تحديث اللوحة", use_container_width=True):
    st.rerun()

st.markdown("---")
st.markdown("### 📋 لوحة الإعلانات الحالية")

try:
  # جلب الإعلانات المخزنة من Supabase
  response = (
      supabase.table("ads")
      .select("*")
      .order("created_at", desc=True)
      .execute()
  )
  ads = response.data

  if ads:
    for ad in ads:
      with st.expander(f"📌 {ad.get('title', 'بدون عنوان')}"):
        st.write(ad.get("content", ""))
        st.caption(f"تاريخ النشر: {ad.get('created_at', '')}")
  else:
    st.info("لا توجد إعلانات حالياً. استخدم الذكاء الاصطناعي لإنشاء أول إعلان!")

except Exception as e:
  st.info(
      "لا توجد إعلانات حالياً أو أن جدول (ads) غير مضاف في قاعدة بيانات"
      " Supabase."
  )
