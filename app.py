import streamlit as st
from groq import Groq
import os
import tempfile

# إعداد الصفحة
st.set_page_config(page_title="تفريغ صوتي - Groq Whisper", page_icon="🎙️")

# العنوان
st.title("🎙️ تفريغ صوتي باستخدام Groq Whisper V3")
st.markdown("حمّل ملف صوتي أو فيديو للحصول على تفريغ نصي فوري")

# مفتاح API من البيئة أو من المستخدم
if "GROQ_API_KEY" in os.environ:
    api_key = os.environ["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("أدخل مفتاح Groq API", type="password")

# تهيئة العميل
if api_key:
    client = Groq(api_key=api_key)
    
    # رفع الملف
    uploaded_file = st.file_uploader(
        "اختر ملف صوتي أو فيديو",
        type=["wav", "mp3", "mp4", "m4a", "ogg", "flac", "webm", "mpeg", "mpga"],
        help="الملفات المدعومة: WAV, MP3, MP4, M4A, OGG, FLAC, WEBM"
    )
    
    if uploaded_file is not None:
        # عرض معلومات الملف
        st.info(f"📁 الملف: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
        
        # عرض المشغل الصوتي/الفيديو
        if uploaded_file.type.startswith("audio"):
            st.audio(uploaded_file)
        elif uploaded_file.type.startswith("video"):
            st.video(uploaded_file)
        
        # زر التفريغ
        if st.button("🚀 ابدأ التفريغ", type="primary"):
            try:
                with st.spinner("جاري التفريغ..."):
                    # حفظ الملف مؤقتًا
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # إرسال إلى Groq
                    with open(tmp_path, "rb") as f:
                        transcription = client.audio.transcriptions.create(
                            file=(uploaded_file.name, f),
                            model="whisper-large-v3",  # أو whisper-large-v3-turbo للسرعة
                            response_format="text",  # أو "json" للتفاصيل
                            language="ar",  # غيّر إلى "en" أو احذف للغة التلقائية
                            temperature=0.0
                        )
                    
                    # تنظيف الملف المؤقت
                    os.unlink(tmp_path)
                    
                    # عرض النتيجة
                    st.success("✅ تم التفريغ بنجاح!")
                    st.subheader("📝 النص المفّرغ:")
                    st.write(transcription.text)
                    
                    # زر النسخ
                    st.download_button(
                        label="📥 تحميل النص",
                        data=transcription.text,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcript.txt",
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
                st.code(f"تفاصيل الخطأ:
{repr(e)}")
                st.markdown("""
                ### حلول مقترحة:
                1. تأكد من صحة مفتاح API
                2. تحقق من حجم الملف (أقل من 25 MB لـ whisper-large-v3)
                3. جرب نموذج `whisper-large-v3-turbo` للسرعة
                4. تأكد من تنسيق الملف المدعوم
                """)
else:
    st.warning("⚠️ يرجى إدخال مفتاح Groq API للبدء")
    st.markdown("""
    ### كيف تحصل على مفتاح API؟
    1. اذهب إلى [console.groq.com](https://console.groq.com)
    2. سجّل دخولك أو أنشئ حسابًا
    3. اذهب إلى API Keys وأنشئ مفتاحًا جديدًا
    """)

# تذييل
st.markdown("---")
st.markdown("تم التطوير باستخدام **Streamlit** + **Groq API** 🚀")
