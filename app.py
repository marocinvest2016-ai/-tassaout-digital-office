import streamlit as st
import os
from google import genai
from supabase import create_client, Client

# إعداد الصفحة
st.set_page_config(page_title="وكيل تساوت العقاري", page_icon="🏠", layout="centered")

st.title("🏠 وكيل تساوت العقاري والخدمات")
st.markdown("مرحباً بك! اسأل عن الشقق، البقع الأرضية، أو العقارات في قلعة السراغنة ومراكش.")

# 1. الاتصال بقاعدة بيانات Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

# 2. إعداد عميل Gemini
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def fetch_properties_from_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return "قاعدة البيانات غير متصلة حالياً. العروض الافتراضية: شقق وفلل فقلعة السراغنة ومراكش."
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table("properties").select("*").execute()
        return response.data
    except Exception as e:
        return f"خطأ في جلب البيانات: {str(e)}"

# واجهة الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب سؤالك هنا (مثال: بغيت شقة فقلعة السراغنة)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not client:
            response_text = "المرجو إدخال مفتاح Gemini API في إعدادات المنصة (Secrets)."
        else:
            db_data = fetch_properties_from_supabase()
            
            system_instruction = """
            أنت "دانا"، الوكيلة الذكية الرسمية لوكالة تساوت للعقارات والخدمات. 
            مهمتك هي الرد على العملاء بالدارجة المغربية، عرض العقارات المناسبة، وإقناعهم بحجز موعد معاينة.
            - جاوب دائماً بالدارجة المغربية وبشكل ودود.
            - لا تخترع أثمنة، اعتمد على البيانات المتوفرة.
            - يجب أن ختم أي رد برقم الهاتف للتواصل: 0691897126.
            """
            
            full_prompt = f"{system_instruction}\n\nبيانات العقارات المتوفرة: {db_data}\nسؤال العميل: {prompt}"
            
            try:
                response = client.models.generate_content(
                    model="gemini-3.7-flash",
                    contents=full_prompt,
                )
                response_text = response.text
            except Exception as e:
                response_text = f"عذراً، حدث خطأ أثناء معالجة طلبك: {str(e)}"
                
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
