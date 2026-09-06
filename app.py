import streamlit as st
from groq import Groq
import pandas as pd
import os
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from duckduckgo_search import DDGS
import requests
from datetime import datetime

# إعداد الصفحة
st.set_page_config(
    page_title="🤖 OMEGA Super Agentic AI",
    page_icon="👑",
    layout="wide"
)

# العنوان الرئيسي
st.title("👑 OMEGA Super Agentic AI")
st.markdown("### CEO + CTO + COO + Copywriter + Closer في وكيل واحد")
st.markdown("---")

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # مفاتيح API
    groq_api_key = st.text_input("🔑 Groq API Key", type="password", 
                                  value=os.getenv("GROQ_API_KEY", ""))
    
    use_google_sheets = st.checkbox("📊 تفعيل Google Sheets", value=False)
    
    if use_google_sheets:
        st.info("📝 أضف ملف `credentials.json` في مجلد المشروع")
        sheet_id = st.text_input("📋 معرف جدول البيانات (Sheet ID)")
        sheet_name = st.text_input("📄 اسم الورقة (Worksheet)", value="Sheet1")
    
    # اختيار المجال
    domain = st.selectbox(
        "🎯 اختر المجال",
        ["تسويق ومبيعات", "تطوير أعمال", "كتابة إعلانية", "تحليل بيانات", "بحث إنترنت", "تفريغ صوتي"]
    )
    
    # اختيار النموذج
    model = st.selectbox(
        "🤖 النموذج",
        ["whisper-large-v3", "whisper-large-v3-turbo", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    )

# تهيئة Groq Client
client = None
if groq_api_key:
    client = Groq(api_key=groq_api_key)
    st.sidebar.success("✅ Groq متصل")

# تهيئة Google Sheets
gc = None
if use_google_sheets and sheet_id and os.path.exists("credentials.json"):
    try:
        creds = service_account.Credentials.from_service_account_file(
            "credentials.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        gc = gspread.authorize(creds)
        st.sidebar.success("✅ Google Sheets متصل")
    except Exception as e:
        st.sidebar.error(f"❌ خطأ في Google Sheets: {e}")

# التبويبات الرئيسية
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 محادثة ذكية", 
    "🎙️ تفريغ صوتي", 
    "🌐 بحث إنترنت", 
    "📊 Google Sheets",
    "📝 سجل العمليات"
])

# === التبويب 1: محادثة ذكية ===
with tab1:
    st.header("💬 محادثة ذكية مع AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # إدخال المستخدم
    if prompt := st.chat_input("اكتب رسالتك..."):
        if client:
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("جاري التفكير..."):
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": f"أنت مساعد ذكي متخصص في {domain}. قدم إجابات دقيقة ومفيدة."},
                                *st.session_state.messages
                            ],
                            max_tokens=2048,
                            temperature=0.7
                        )
                        
                        ai_response = response.choices[0].message.content
                        st.write(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        
                        # حفظ في Google Sheets إذا مفعّل
                        if gc and sheet_id:
                            try:
                                sh = gc.open_by_key(sheet_id)
                                worksheet = sh.worksheet(sheet_name)
                                worksheet.append_row([
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "user",
                                    prompt[:500]
                                ])
                                worksheet.append_row([
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "assistant",
                                    ai_response[:500]
                                ])
                            except Exception as e:
                                st.warning(f"⚠️ لم يُحفظ في Sheets: {e}")
                    
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
        else:
            st.warning("⚠️ يرجى إدخال مفتاح Groq API في الشريط الجانبي")

# === التبويب 2: تفريغ صوتي ===
with tab2:
    st.header("🎙️ تفريغ صوتي باستخدام Whisper")
    
    if client:
        uploaded_file = st.file_uploader(
            "حمّل ملف صوتي أو فيديو",
            type=["wav", "mp3", "mp4", "m4a", "ogg", "flac", "webm", "mpeg", "mpga"]
        )
        
        if uploaded_file:
            st.info(f"📁 {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
            
            if uploaded_file.type.startswith("audio"):
                st.audio(uploaded_file)
            elif uploaded_file.type.startswith("video"):
                st.video(uploaded_file)
            
            if st.button("🚀 ابدأ التفريغ", type="primary"):
                with st.spinner("جاري التفريغ..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name
                        
                        with open(tmp_path, "rb") as f:
                            transcription = client.audio.transcriptions.create(
                                file=(uploaded_file.name, f),
                                model=model,
                                response_format="text",
                                language="ar"
                            )
                        
                        os.unlink(tmp_path)
                        
                        st.success("✅ تم التفريغ بنجاح!")
                        st.text_area("📝 النص المفّرغ", value=transcription.text, height=300)
                        
                        st.download_button(
                            label="📥 تحميل النص",
                            data=transcription.text,
                            file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                        
                        # حفظ في Sheets
                        if gc and sheet_id:
                            try:
                                sh = gc.open_by_key(sheet_id)
                                worksheet = sh.worksheet(sheet_name)
                                worksheet.append_row([
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "transcription",
                                    uploaded_file.name,
                                    transcription.text[:500]
                                ])
                            except Exception as e:
                                st.warning(f"⚠️ لم يُحفظ في Sheets: {e}")
                    
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
                        st.code(str(e))
    else:
        st.warning("⚠️ يرجى إدخال مفتاح Groq API")

# === التبويب 3: بحث إنترنت ===
with tab3:
    st.header("🌐 بحث إنترنت باستخدام DuckDuckGo")
    
    search_query = st.text_input("أدخل كلمة البحث")
    
    if st.button("🔍 بحث"):
        if search_query:
            with st.spinner("جاري البحث..."):
                try:
                    with DDGS() as ddgs:
                        results = ddgs.text(search_query, max_results=10)
                    
                    if results:
                        for i, result in enumerate(results, 1):
                            with st.expander(f"📄 {i}. {result.get('title', 'بدون عنوان')[:100]}"):
                                st.write(f"**الرابط:** {result.get('href', 'N/A')}")
                                st.write(f"**الوصف:** {result.get('body', 'N/A')[:500]}")
                        
                        # حفظ في Sheets
                        if gc and sheet_id:
                            try:
                                sh = gc.open_by_key(sheet_id)
                                worksheet = sh.worksheet(sheet_name)
                                for result in results[:5]:
                                    worksheet.append_row([
                                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "search",
                                        search_query,
                                        result.get('title', '')[:200],
                                        result.get('href', '')
                                    ])
                            except Exception as e:
                                st.warning(f"⚠️ لم يُحفظ في Sheets: {e}")
                    else:
                        st.warning("⚠️ لم تُعثر على نتائج")
                
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
        else:
            st.warning("⚠️ يرجى إدخال كلمة بحث")

# === التبويب 4: Google Sheets ===
with tab4:
    st.header("📊 إدارة Google Sheets")
    
    if gc and sheet_id:
        try:
            sh = gc.open_by_key(sheet_id)
            worksheet = sh.worksheet(sheet_name)
            
            # عرض البيانات
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            
            st.dataframe(df, use_container_width=True)
            
            # إحصائيات
            st.subheader("📈 إحصائيات")
            st.metric("عدد الصفوف", len(df))
            st.metric("عدد الأعمدة", len(df.columns))
            
            # تصدير
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 تحميل كـ CSV",
                data=csv,
                file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ خطأ في قراءة البيانات: {e}")
    else:
        st.warning("⚠️ قم بتفعيل Google Sheets في الشريط الجانبي")

# === التبويب 5: سجل العمليات ===
with tab5:
    st.header("📝 سجل العمليات")
    
    log_file = "operations_log.txt"
    
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            logs = f.read()
        st.text_area("سجل العمليات", value=logs, height=500)
    else:
        st.info("📝 لا يوجد سجل عمليات بعد")
    
    if st.button("🗑️ مسح السجل"):
        if os.path.exists(log_file):
            os.remove(log_file)
            st.success("✅ تم مسح السجل")
            st.rerun()

# التذييل
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <b>👑 OMEGA Super Agentic AI</b> | 
    يعمل على <b>Groq</b> 🚀 | 
    تم التطوير باستخدام <b>Streamlit</b>
</div>
""", unsafe_allow_html=True)
