import os
import requests
import streamlit as st

st.set_page_config(page_title="Groq Models Explorer", page_icon="🤖")

st.title("🤖 استعراض نماذج Groq المتاحة")
st.write("هذا التطبيق يقوم بجلب قائمة النماذج المتاحة في منصة Groq باستخدام مفتاح الـ API الخاص بك.")

# قراءة مفتاح الـ API من متغيرات البيئة أو إدخاله يدوياً
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
  api_key = st.text_input("أدخل مفتاح GROQ_API_KEY الخاص بك:", type="password")

if st.button("جلب النماذج"):
  if not api_key:
    st.error("الرجاء إدخال مفتاح الـ API أو ضبط متغير البيئة GROQ_API_KEY.")
  else:
    with st.spinner("جاري الاتصال بمنصة Groq..."):
      url = "https://api.groq.com/openai/v1/models"
      headers = {
          "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json",
      }

      response = requests.get(url, headers=headers)

      if response.status_code == 200:
        st.success("تم الاتصال بنجاح!")
        models_data = response.json()

        # عرض النماذج بشكل منظم
        if "data" in models_data:
          st.subheader("النماذج المتاحة:")
          for model in models_data["data"]:
            st.info(f"🔹 **{model.get('id')}** (مُنشئ بواسطة: {model.get('owned_by', 'غير معروف')})")
        else:
          st.json(models_data)
      else:
        st.error(f"حدث خطأ: {response.status_code}")
        st.json(response.json())
