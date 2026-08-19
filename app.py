import streamlit as st
from supabase import create_client
import google.generativeai as genai
import PIL.Image
import pandas as pd
from datetime import datetime

# --- إعدادات النظام ---
BOT_NAME = "OMEGA OS - Elite Core"
NOM_ENTREPRISE = "وكالة تساوت الرقمية للخدمات"

# 1. قراءة الأسرار من st.secrets
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception as e:
    st.error("⚠️ يرجى التأكد من إعداد ملف الأسرار secrets.toml بشكل صحيح.")
    st.stop()

# 2. تهيئة الاتصال
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=f"""أنت المهندس السيادي لـ {NOM_ENTREPRISE}.
    تخصصاتك:
    1. البرمجة والأنظمة: تكتب أكواد (Python, JS, SQL) لإعداد الكاميرات الرقمية والأتمتة.
    2. الهندسة: مهندس معماري وديكور، تقدم حلولاً تقنية ومقاسات.
    3. الصفقات: خبير صفقات عمومية، تبحث في الإنترنت، تحلل المناقصات، وتصيغ العقود.
    معلومات الشركة: توريد مواد البناء، عقار فلاحي وصناعي، هندسة رقمية وصناعية، خدمات الحج والعمرة بقلعة السراغنة.
    أجب دائماً بعمق تقني ومهنية عالية وباللغة العربية المغربية."""
)

st.set_page_config(page_title=BOT_NAME, layout="wide")

# --- القائمة الجانبية ---
st.sidebar.title(f"👑 {BOT_NAME}")
menu = [
    "المنصة الرئيسية 🏡", 
    "الوكيل الهندسي والتقني 🤖", 
    "رصد الميدان (كاميرا) 📷", 
    "توليد الصور الفوري ✨", 
    "إدارة الصفقات 📋"
]
choice = st.sidebar.radio("الوحدات التشغيلية:", menu)

# --- 1. المنصة الرئيسية ---
if choice == "المنصة الرئيسية 🏡":
    st.title(f"مرحباً بك يا عامر في {NOM_ENTREPRISE}")
    st.success("النظام في وضع الاستعداد التام ومربوط بالسحابة بنجاح.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("حالة الأمان", "مؤمن بـ st.secrets")
    with col2:
        st.metric("قاعدة البيانات", "متصل بـ Supabase")
    with col3:
        st.metric("محرك الذكاء", "Gemini 1.5 Pro")

# --- 2. الوكيل الهندسي والتقني ---
elif choice == "الوكيل الهندسي والتقني 🤖":
    st.title("🤖 الوكيل الذكي (هندسة، صفقات، أكواد)")
    if "chat" not in st.session_state: 
        st.session_state.chat = []
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): 
            st.markdown(m["content"])

    if prompt := st.chat_input("اطلب كود كاميرا، استشارة ديكور، أو بحثاً عن صفقة..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("المهندس السيادي يفكر..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.chat.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"خطأ في الاتصال بالنموذج: {e}")

# --- 3. رصد الميدان (كاميرا) ---
elif choice == "رصد الميدان (كاميرا) 📷":
    st.title("📷 رصد الميدان بالذكاء الاصطناعي")
    img_file = st.camera_input("التقط صورة للورش أو الموقع")
    
    if img_file:
        st.image(img_file, caption="الورش الميداني")
        project_name = st.text_input("اسم المشروع/الورش:")
        
        if st.button("تحليل الورش ميدانياً 🔍"):
            with st.spinner("المهندس السيادي يحلل الصورة..."):
                try:
                    # أ. التحليل البصري بواسطة Gemini Vision
                    img = PIL.Image.open(img_file)
                    vision_model = genai.GenerativeModel("gemini-1.5-pro")
                    prompt = f"""أنت مهندس خبير في أوراش البناء بقلعة السراغنة. 
                    قم بتحليل هذه الصورة لمشروع {project_name} وقدم تقريراً يشمل: 
                    1. نسبة تقدم الأشغال % 2. المواد الظاهرة 3. ملاحظات السلامة 4. توصيات هندسية."""
                    
                    response = vision_model.generate_content([prompt, img])
                    report = response.text
                    
                    st.markdown("### 📊 تقرير التحليل:")
                    st.write(report)
                    
                    # ب. رفع الصورة إلى Supabase Storage وحفظ التقرير
                    if project_name:
                        file_name = f"{project_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        
                        # رفع الصورة (تأكد من وجود Bucket باسم reports في Supabase)
                        supabase.storage.from_("reports").upload(file_name, img_file.getvalue())
                        image_url = supabase.storage.from_("reports").get_public_url(file_name)

                        # حفظ البيانات في جدول reports
                        supabase.table("reports").insert({
                            "project_name": project_name,
                            "report_content": report,
                            "image_url": image_url,
                            "date": datetime.now().isoformat()
                        }).execute()
                        
                        st.success("✅ تم حفظ التقرير والصورة في الأرشيف السحابي بنجاح.")
                    else:
                        st.warning("يرجى كتابة اسم المشروع ليتم حفظ التقرير في الأرشيف.")
                        
                except Exception as e:
                    st.error(f"خطأ في التحليل أو الرفع السحابي: {e}")

# --- 4. توليد الصور الفوري ---
elif choice == "توليد الصور الفوري ✨":
    st.title("✨ توليد المخططات والتصاميم")
    prompt_img = st.text_input("صف التصميم (مثلاً: تصميم فيلا حديثة بقلعة السراغنة):")
    if st.button("توليد الآن 🎨"):
        if prompt_img:
            url = f"https://image.pollinations.ai/prompt/{prompt_img.replace(' ', '%20')}"
            st.image(url, caption="التصميم المولد")
        else:
            st.warning("الرجاء كتابة وصف التصميم أولاً.")

# --- 5. إدارة الصفقات ---
elif choice == "إدارة الصفقات 📋":
    st.title("📋 إدارة الصفقات والسجلات السحابية")
    
    tab1, tab2 = st.tabs(["➕ إضافة صفقة جديدة", "📊 عرض كل الصفقات"])

    # أ. فورم الإضافة
    with tab1:
        with st.form("deal_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("اسم الصفقة / المشروع:")
                type_deal = st.selectbox("نوع الصفقة:", ["مواد البناء", "عقار فلاحي", "عقار صناعي", "هندسة", "حج وعمرة"])
            with col2:
                client = st.text_input("اسم العميل / الجهة:")
                montant = st.number_input("المبلغ التقديري MAD:", min_value=0, step=1000)
            
            notes = st.text_area("ملاحظات إضافية:")

            if st.form_submit_button("حفظ الصفقة في السحابة 🚀"):
                if name:
                    data = {
                        "nom": name,
                        "type": type_deal,
                        "client": client,
                        "montant": montant,
                        "notes": notes,
                        "entreprise": NOM_ENTREPRISE,
                        "date_creation": datetime.now().isoformat()
                    }
                    try:
                        supabase.table("deals").insert(data).execute()
                        st.success(f"✅ تم حفظ صفقة '{name}' بنجاح في قاعدة البيانات.")
                    except Exception as e:
                        st.error(f"خطأ في الحقن السحابي: {e}")
                else:
                    st.warning("الرجاء إدخال اسم الصفقة أو المشروع على الأقل.")

    # ب. عرض الصفقات
    with tab2:
        st.subheader("سجل الصفقات السحابية")
        if st.button("تحديث وعرض البيانات 🔄"):
            try:
                response = supabase.table("deals").select("*").order("date_creation", desc=True).execute()
                df = pd.DataFrame(response.data)
                
                if not df.empty:
                    st.dataframe(df[["date_creation", "nom", "type", "client", "montant", "notes"]], use_container_width=True)
                    
                    total = df["montant"].sum()
                    st.metric("إجمالي قيمة الصفقات النشطة", f"{total:,.2f} MAD")
                else:
                    st.info("لا توجد صفقات مسجلة حالياً.")
            except Exception as e:
                st.error(f"خطأ في استرجاع البيانات: {e}")
