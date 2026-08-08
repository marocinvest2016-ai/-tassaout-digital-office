import streamlit as st
from agent import TassaoutAgenticCore

# إعدادات الصفحة
st.set_page_config(
    page_title="سراغنة العقارية | المساعد الذكي",
    page_icon="🏢",
    layout="wide"
)

# إنشاء كائن من الوكيل الذكي
agent = TassaoutAgenticCore()

# عرض لوحة البيانات الميدانية والعقارية في الشريط الجانبي أو الأعلى
st.sidebar.title("📌 إدارة المنظومة")
page_choice = st.sidebar.radio("اختر العرض:", ["الدردشة الذكية مع الوكيل", "لوحة البيانات والسكور الميداني"])

if page_choice == "لوحة البيانات والسكور الميداني":
    # استدعاء دالة العرض الموجودة في agent.py لعرض كل السجلات التي كتبتها
    agent.render_dashboard()

else:
    # شاشة الدردشة التفاعلية
    st.title(f"🏢 {agent.commercial_name}")
    st.subheader("🤖 المساعد الذكي للعمليات والعقارات (قلعة السراغنة ومراكش)")
    st.markdown("---")

    # تهيئة سجل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"أهلاً بك في {agent.commercial_name}. أنا جاهز لإدارة الاستفسارات العقارية واللوجستية. كيف يمكنني خدمتك اليوم؟"}
        ]

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال مدخلات المستخدم
    if prompt := st.chat_input("اطرح سؤالك أو استفسارك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # معالجة ذكية بناءً على البيانات الموجودة في الكلاس
            if "هدى" in prompt or "عقار" in prompt:
                response = "بخصوص العقارات، لدينا توثيق ميداني لتجزئة الهدى 1 و الهدى 2 وبقع البدر 1 مع إحداثيات ومتابعة دقيقة."
            elif "شحن" in prompt or "لوجستيك" in prompt:
                response = "بالنسبة للشحن الدولي، نتابع مسارات أوروبا - المغرب بدقة ومواعيد الإطلاق المجدولة."
            else:
                response = f"تم استقبال استفسارك بنجاح في {agent.commercial_name}. النظام يعمل بكفاءة عالية لتلبية طلباتكم في قلعة السراغنة ومراكش."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
