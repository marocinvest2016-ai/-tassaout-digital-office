import streamlit as st
from groq import Groq
import os

# ====================== إعداد الصفحة ======================
st.set_page_config(
    page_title="أخرى | مساعد العقارات الذكي",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 أخرى - مساعد العقارات الذكي")
st.markdown("مولّد إعلانات وتحليلات عقارية بالدارجة والعربية الفصحى باستخدام نماذج Groq المفتوحة المصدر")

# ====================== الاتصال بـ Groq ======================
api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input("أدخل مفتاح Groq API", type="password")

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح Groq API في الشريط الجانبي")
    st.stop()

client = Groq(api_key=api_key)

# ====================== الشريط الجانبي ======================
st.sidebar.header("⚙️ الإعدادات")

model = st.sidebar.selectbox(
    "اختر النموذج",
    [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "llama-3.1-8b-instant"
    ],
    index=0
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 256, 2048, 1024, 128)

# ====================== دالة التوليد ======================
def chat_with_model(prompt: str, model: str, temperature: float, max_tokens: int):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي متخصص في العقارات والتحليل في المغرب. تكتب بالدارجة المغربية والعربية الفصحى حسب الطلب."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}"

# ====================== الواجهة الرئيسية ======================
tab1, tab2, tab3 = st.tabs(["✍️ توليد إعلان", "📊 تحليل سوق", "💡 نصائح للوسطاء"])

with tab1:
    st.subheader("توليد إعلان عقاري")
    property_desc = st.text_area(
        "اكتب تفاصيل العقار (المدينة، النوع، المساحة، السعر...)",
        placeholder="مثال: شقة 120 متر في قلعة السراغنة، طابق ثالث، ثمن 850.000 درهم"
    )
    lang = st.radio("اللغة المطلوبة", ["الدارجة", "العربية الفصحى", "الاثنين معاً"], horizontal=True)

    if st.button("🚀 توليد الإعلان", type="primary"):
        if property_desc:
            with st.spinner("جاري كتابة الإعلان..."):
                prompt = f"اكتب إعلان عقاري جذاب بالـ {lang} للعقار التالي، مع عنوان قوي ودعوة للعمل:\n\n{property_desc}"
                result = chat_with_model(prompt, model, temperature, max_tokens)
                st.success("تم التوليد بنجاح!")
                st.markdown(result)
        else:
            st.warning("أدخل تفاصيل العقار أولاً")

with tab2:
    st.subheader("تحليل فرصة استثمار عقاري")
    city = st.text_input("المدينة أو الجهة", placeholder="مثال: جهة مراكش-آسفي أو قلعة السراغنة")
    if st.button("📈 تحليل الفرصة", type="primary"):
        if city:
            with st.spinner("جاري التحليل..."):
                prompt = f"حلل فرصة استثمار عقاري في {city}. أعطني نقاط القوة والضعف والفرص والتهديدات + توصية واضحة."
                result = chat_with_model(prompt, model, temperature, max_tokens)
                st.markdown(result)
        else:
            st.warning("أدخل المدينة أولاً")

with tab3:
    st.subheader("نصائح للوسطاء العقاريين")
    if st.button("💡 احصل على النصائح", type="primary"):
        with st.spinner("جاري التحضير..."):
            prompt = "لخص أهم النصائح العملية للوسطاء العقاريين في المغرب لزيادة المبيعات في 2026"
            result = chat_with_model(prompt, model, temperature, max_tokens)
            st.markdown(result)

# ====================== تذييل ======================
st.markdown("---")
st.caption(f"النموذج المستخدم حالياً: **{model}** | مدعوم بواسطة Groq")
