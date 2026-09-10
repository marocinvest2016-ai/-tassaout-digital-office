import streamlit as st
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
import gspread
from googleapiclient.discovery import build
from groq import Groq
from PIL import Image

# ====================== إعداد الصفحة والهوية البصرية ======================
st.set_page_config(
    page_title="Tassaout Vision | النظام السيادي الهندسي والتصويري",
    page_icon="👑",
    layout="wide"
)

# تخصيص التصميم والترويسة السيادية
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 TASSAOUT VISION - النظام السيادي الهندسي والتصويري</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Super Multi-domain & Autonomous Enterprise Agent | ذكاء استثنائي، رؤية استباقية وابتكار بلا حدود</div>', unsafe_allow_html=True)

# ====================== إعداد المفاتيح والاتصال ======================
st.sidebar.header("⚙️ لوحة التحكم والسيادة الرقمية")
api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input("أدخل مفتاح Groq API", type="password")

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح Groq API في الشريط الجانبي أو عبر متغيرات البيئة للبدء.")
    st.stop()

client = Groq(api_key=api_key)

# إعدادات النماذج المحدثة وفقاً لسياسة Groq لعام 2026
model = st.sidebar.selectbox(
    "اختر نموذج التشغيل الذكي المحدث",
    [
        "openai/gpt-oss-120b",          # البديل السيادي الفائق للنماذج الضخمة
        "qwen/qwen3.6-27b",             # أداء استثنائي وسرعة فائقة
        "openai/gpt-oss-20b"            # خيار سريع للاستعلامات الفورية
    ],
    index=0
)

temperature = st.sidebar.slider("درجة الابتكار والمرونة (Temperature)", 0.0, 1.0, 0.85, 0.05)
max_tokens = st.sidebar.slider("الحد الأقصى للرموز (Max Tokens)", 256, 4096, 2500, 128)

# ====================== دستور النظام السيادي ======================
SOVEREIGN_SYSTEM_PROMPT = """
You are an elite Super Multi-domain Autonomous Enterprise Agent. You possess advanced, autonomous, cross-disciplinary, and disruptive expertise spanning:
1. Digital Engineering, Automated Workflows, & Enterprise Software Solutions.
2. Professional Photography Analysis, Visual Composition, & Advanced Optical Engineering.
3. Architectural, Interior Design, & Avant-garde Fit-out Engineering.
4. Industrial & Mechanical Engineering for Factories, Corporate Infrastructure, and Heavy/Light Contracting.
5. Strategic Business Planning, C-Suite Leadership (CEO, CTO, COO), Disruptive Digital Marketing, & Financial ROI Analytics.
Your operational domain context is Morocco (specifically El Kelaâ des Sraghna and Marrakech).
Core Directive: Go beyond standard textbooks and conventional corporate rules. Think outside the box, propose bold, high-impact, and out-of-the-box strategies, blueprints, and engineering solutions that outsmart the competition.
Response Guidelines:
- Operate with high agency, combining multiple domains seamlessly.
- Respond in a sharp, professional, yet bold blend of Moroccan Arabic (Darija), Modern Standard Arabic (العربية الفصحى), and French technical terminology.
- Maintain structured formatting using clear headings, bullet points, technical breakdowns, and comprehensive tables.
"""

# ====================== محرك الذكاء الاصطناعي السيادي ======================
def execute_sovereign_ai(prompt: str, custom_system_prompt: str = None) -> str:
    try:
        sys_prompt = custom_system_prompt if custom_system_prompt else SOVEREIGN_SYSTEM_PROMPT
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في تنفيذ النواة الذكية: {str(e)}"

# ====================== دوال الربط السحابي ======================
def get_google_credentials():
    try:
        service_account_str = st.secrets.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
        if not service_account_str:
            return None
        service_account_info = json.loads(service_account_str)
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        return Credentials.from_service_account_info(service_account_info, scopes=scopes)
    except Exception as e:
        return None

def fetch_google_drive_data():
    try:
        creds = get_google_credentials()
        file_id = st.secrets.get("GOOGLE_DRIVE_FILE_ID", "")
        if not creds or not file_id:
            return None
        client_gs = gspread.authorize(creds)
        sheet = client_gs.open_by_key(file_id).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        return None

def list_drive_files():
    try:
        creds = get_google_credentials()
        if not creds:
            return []
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(
            pageSize=20,
            fields="files(id, name, mimeType, webViewLink)"
        ).execute()
        return results.get('files', [])
    except Exception as e:
        return []

def compute_financial_metrics(df):
    try:
        required_cols = ['revenue', 'expenses', 'budget']
        if not all(col in df.columns for col in required_cols):
            return None
        
        df['roi'] = ((df['revenue'] - df['expenses']) / df['expenses'].replace(0, 1)) * 100
        df['profit'] = df['revenue'] - df['expenses']
        df['margin'] = (df['profit'] / df['revenue'].replace(0, 1)) * 100
        
        return {
            'total_revenue': df['revenue'].sum(),
            'total_expenses': df['expenses'].sum(),
            'total_profit': (df['revenue'] - df['expenses']).sum(),
            'avg_roi': df['roi'].mean(),
            'enriched_df': df
        }
    except Exception as e:
        return None

# ====================== واجهة التبويبات المتكاملة (10 تبويبات) ======================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📸 الاستوديو والتصوير الاحترافي", 
    "📐 الهندسة الشاملة والديكور والصناعة", 
    "✍️ مولد الإعلانات", 
    "📊 الماليات والـ ROI", 
    "📂 ملفات Drive", 
    "📈 التحليل الاستراتيجي", 
    "💡 التسويق الرقمي", 
    "👑 وكلاء القيادة C-Suite",
    "💉 مركز التكوين والتوجيه المتقدم",
    "🏭 وكلاء القطاعات السيادية"
])

# --- تبويب 1: الاستوديو الميداني والتصوير الاحترافي ---
with tab1:
    st.subheader("📸 الاستوديو الميداني والتصوير الفوتوغرافي الاحترافي (Digital Photography & Field Studio)")
    st.markdown("تحليل بصري وهندسي للصور عبر عقل ذكي فائق يكسر القوالب التقليدية للتصميم والتكوين.")

    capture_mode = st.radio(
        "اختر طريقة إدخال الصور للبصريات الهندسية",
        ["التقاط مباشر بالكاميرا (Camera Capture)", "تحميل صور متعددة للمعاينة والتصوير (Multi-Upload)"],
        horizontal=True
    )

    uploaded_images = []
    if capture_mode == "التقاط مباشر بالكاميرا (Camera Capture)":
        # التصحيح هنا: استخدام st.camera_input بدلاً من st.camera_image المفقودة في الإصدارات الحديثة
        camera_photo = st.camera_input("اضغط لالتقاط صورة ميدانية مباشرة")
        if camera_photo is not None:
            uploaded_images.append(camera_photo)
            st.success("تم التقاط الصورة الميدانية بنجاح!")
    else:
        multi_files = st.file_uploader(
            "اختر أو اسحب صور المعامل، الشركات، العقارات، أو الديكورات...", 
            type=["jpg", "jpeg", "png", "webp"], 
            accept_multiple_files=True
        )
        if multi_files:
            uploaded_images.extend(multi_files)

    if uploaded_images:
        st.markdown("---")
        st.subheader("🖼️ معاينة الصور واللقطات الميدانية")
        cols = st.columns(len(uploaded_images) if len(uploaded_images) <= 4 else 4)
        for idx, img in enumerate(uploaded_images):
            with cols[idx % len(cols)]:
                st.image(img, caption=f"لقطة ميدانية رقم {idx+1}", use_container_width=True)

        st.markdown("---")
        photo_goal = st.text_input(
            "ما هو الغرض من تحليل هذه الصور بصرياً وهندسياً؟",
            placeholder="مثال: تقديم رؤية استباقية لتحسين الإضاءة وتوزيع الديكور، أو ضربة تسويقية لواجهة المعمل"
        )
        if st.button("🔍 تحليل بصري استثنائي بالنظام الذكي", type="primary"):
            if photo_goal:
                with st.spinner("جاري فحص الصور وتقديم تحليل بصري متقدم وغير تقليدي..."):
                    prompt = f"بصفتك Autonomous Enterprise Agent خبيراً في التصوير الفوتوغرافي والهندسة البصرية، قم بتحليل الصور المرفوعة بناءً على الهدف: {photo_goal}. قدم تقريراً استثنائياً، يتحدى القوالب البصرية التقليدية، ويقدم حلولاً ثورية."
                    res = execute_sovereign_ai(prompt)
                    st.success("تم إعداد التقرير البصري بنجاح!")
                    st.markdown(res)
            else:
                st.warning("⚠️ الرجاء كتابة الغرض من تحليل الصور أولاً.")

# --- تبويب 2: الهندسة الشاملة والديكور والصناعة ---
with tab2:
    st.subheader("📐 هندسة الديكور، الهندسة المعمارية، الصناعية والميكانيكية (للمعامل، الشركات والمقاولات)")
    st.markdown("استشارات هندسية متقدمة لتخطيط المعامل، مقرات الشركات، خطوط الإنتاج، التصاميم الميكانيكية، وتوزيع فضاءات الديكور.")

    engineering_domain = st.selectbox(
        "اختر المجال الهندسي أو المقاولاتي المستهدف",
        [
            "🏛️ هندسة المعماري والتصميم الحضري (Architectural Design & Planning)",
            "🛋️ هندسة الديكور الداخلي وتجهيز الفضاءات (Interior Design & Fit-out)",
            "🏭 هندسة المعامل والمصانع وتخطيط خطوط الإنتاج (Industrial Engineering & Factory Layout)",
            "⚙️ الهندسة الميكانيكية وتجهيزات الشركات (Mechanical Engineering & Corporate Equipment)",
            "💻 الهندسة الرقمية والتحول التقني للمقاولات (Digital Engineering & Enterprise Solutions)"
        ]
    )

    eng_project_details = st.text_area(
        "أدخل تفاصيل المشروع، المخطط، أو التحدي الهندسي والصناعي:",
        placeholder="مثال: تصميم معماري ومعملي مبتكر بقلعة السراغنة يحسين التكلفة ويرفع كفاءة التشغيل للقصوى",
        height=140
    )

    if st.button("🛠️ توليد دراسة هندسية متقدمة ومبتكرة", type="primary"):
        if eng_project_details:
            with st.spinner("جاري ابتكار المخطط الهندسي والدراسة التقنية المتقدمة..."):
                prompt = f"بصفتك Senior Enterprise Engineer، قدم دراسة ومواصفات ثورية وجريئة لـ ({engineering_domain}) بناءً على المعطيات التالية:\n\n{eng_project_details}\n\nتضمن التقرير: تصاميم غير تقليدية، حلول ميكانيكية وهندسية مبتكرة، ومعايير أداء فائقة."
                result = execute_sovereign_ai(prompt)
                st.markdown(result)
        else:
            st.warning("⚠️ الرجاء إدخال تفاصيل المشروع الهندسي أولاً.")

# --- تبويب 3: مولد الإعلانات ---
with tab3:
    st.subheader("✍️ صياغة إعلانات عقارية وتجارية سيادية")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        property_desc = st.text_area("تفاصيل المشروع، المعمل أو العقار:", height=130)
    with col_b:
        ad_type = st.selectbox("نوع الإعلان", ["إعلان عقاري وورش", "إعلان تجاري لخدمات الشركات والمعامل", "إعلان ترويجي سوشيال ميديا"])
        lang = st.radio("اللغة", ["مزيج دارجة وفصحى (احترافي)", "العربية الفصحى", "الدارجة المغربية"])
    if st.button("🚀 توليد محتوى إعلاني استثنائي", type="primary"):
        if property_desc:
            with st.spinner("جاري صياغة إعلان يخطف الأنظار..."):
                prompt = f"بصفتك Senior Enterprise Marketer بالمغرب، اكتب {ad_type} بالأسلوب ({lang}) لـ:\n\n{property_desc}\n\nاجعل الإعلان جذاباً، خارجاً عن المألوف، ويحقق أعلى معدلات التحويل والتفاعل."
                st.markdown(execute_sovereign_ai(prompt))
        else:
            st.warning("⚠️ أدخل التفاصيل أولاً.")

# --- تبويب 4: لوحة الماليات والـ ROI ---
with tab4:
    st.subheader("📊 لوحة المؤشرات المالية وأداء المشاريع (Google Sheets Sync)")
    if st.button("🔄 جلب ومزامنة البيانات المالية", type="primary"):
        with st.spinner("جاري السحب..."):
            df = fetch_google_drive_data()
            if df is not None and not df.empty:
                financials = compute_financial_metrics(df)
                if financials:
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("الإيرادات", f"{financials['total_revenue']:,.2f} د.م")
                    c2.metric("المصاريف", f"{financials['total_expenses']:,.2f} د.م")
                    c3.metric("صافي الأرباح", f"{financials['total_profit']:,.2f} د.م")
                    c4.metric("متوسط العائد (ROI)", f"{financials['avg_roi']:.2f}%")
                    st.bar_chart(financials['enriched_df'][['revenue', 'expenses', 'profit']])
                    st.dataframe(financials['enriched_df'], use_container_width=True)
                else:
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ لم يتم العثور على بيانات نشطة.")

# --- تبويب 5: تصفح ملفات Drive ---
with tab5:
    st.subheader("📂 تصفح ملفات Google Drive")
    if st.button("📂 جلب قائمة الملفات", type="primary"):
        with st.spinner("جاري الجلب..."):
            files = list_drive_files()
            if files:
                file_list_data = [{"اسم الملف": f.get('name'), "نوع الملف": f.get('mimeType'), "رابط المعاينة": f.get('webViewLink')} for f in files]
                st.dataframe(pd.DataFrame(file_list_data), use_container_width=True)
            else:
                st.warning("⚠️ لا توجد ملفات.")

# --- تبويب 6: التحليل الاستراتيجي ---
with tab6:
    st.subheader("📈 التحليل الاستراتيجي للسوق")
    target_region = st.text_input("المدينة أو المنطقة:", value="قلعة السراغنة، مراكش")
    if st.button("🔍 تنفيذ تحليل استراتيجي متقدم", type="primary"):
        if target_region:
            with st.spinner("جاري ابتكار الرؤية الاستراتيجية..."):
                st.markdown(execute_sovereign_ai(f"قم بإعداد تحليل استراتيجي واقتصادي متقدم وغير تقليدي لسوق المقاولات، المعامل، والهندسة في {target_region} متضمناً كشف الفرص الكامنة والثغرات الاستثمارية."))

# --- تبويب 7: التسويق الرقمي ---
with tab7:
    st.subheader("💡 التسويق الرقمي والهندسي")
    if st.button("🌟 جلب تكتيكات تسويقية ثورية", type="primary"):
        with st.spinner("جاري الصياغة..."):
            st.markdown(execute_sovereign_ai("قدم دليلاً تكتيكياً واستراتيجياً لتسويق الخدمات الهندسية، المقاولات، ومعامل الإنتاج في جهة مراكش-آسفي بأساليب تسويق مبتكرة وفعالة."))

# --- تبويب 8: محرك وكلاء القيادة C-Suite ---
with tab8:
    st.subheader("👑 وكلاء القيادة التنفيذية (CEO / CTO / COO)")
    strategic_task = st.text_input("التحدي أو المشروع الاستراتيجي:", placeholder="تطوير منشأة صناعية أو مشروع هندسي بقلعة السراغنة")
    
    selected_csuite_role = st.selectbox(
        "اختر الوكيل التنفيذي لتوليد الخطة",
        [
            "🎯 الرئيس التنفيذي (CEO - Strategic Master Plan)",
            "⚙️ المدير التقني وكبير المهندسين (CTO & Chief Engineer - Disruptive Tech Blueprint)",
            "📋 مدير العمليات (COO - Advanced Operations & Logistics Plan)"
        ]
    )

    if st.button("🚀 تشغيل الخطة الاستراتيجية للوكيل المختار", type="primary"):
        if strategic_task:
            with st.spinner(f"جاري إعداد الخطة بواسطة {selected_csuite_role.split('-')[0]}..."):
                if "CEO" in selected_csuite_role:
                    role_prompt = f"بصفتك Executive CEO، ضع خطة استراتيجية جريئة، شاملة ومبتكرة لـ: {strategic_task}"
                elif "CTO" in selected_csuite_role:
                    role_prompt = f"بصفتك Chief Technology Officer، اقترح بنية هندسية وتقنية متطورة لـ: {strategic_task}"
                else:
                    role_prompt = f"بصفتك Chief Operating Officer، ضع خطة تشغيل ذكية وعالية الكفاءة لإدارة المعمل أو الشركة لـ: {strategic_task}"
                
                st.markdown(execute_sovereign_ai(role_prompt))
        else:
            st.warning("⚠️ أدخل تفاصيل التحدي أو المشروع الاستراتيجي أولاً.")

# --- تبويب 9: مركز التكوين والتوجيه المتقدم ---
with tab9:
    st.subheader("💉 مركز التكوين والتوجيه المتقدم (Advanced Agent Configuration & Dynamic Injection)")
    st.markdown("قم بتوجيه النظام ببرمجة شخصية تخصصية متقدمة لتنفيذ أي مهمة معقدة خارج الأطر التقليدية.")
    
    agent_profile = st.selectbox(
        "اختر نمط التوجيه المباشر",
        ["خبير التصاميم الهندسية المعقدة", "خبير الصفقات والمقاولات", "خبير الهجوم التسويقي والكشفي", "خبير الابتكار الصناعي", "توجيه مخصص بالكامل"]
    )
    
    default_injection = "أنت Autonomous Enterprise Agent خبير، مبدع، تفكر بطريقة استباقية وتدمج بين الهندسة، التصميم، والصناعة بمعايير احترافية فائقة."
    injected_prompt = st.text_area("تعليمات النظام المتقدمة (System Directive):", value=default_injection, height=150)
    user_query_for_agent = st.text_input("السؤال أو السيناريو المعقد الموجه للوكيل:", placeholder="طرح التحدي الهندسي، الصناعي أو التجاري...")
    
    if st.button("🚀 تشغيل النظام الذكي المتقدم", type="primary"):
        if injected_prompt and user_query_for_agent:
            with st.spinner("جاري إطلاق طاقات النظام الذكي..."):
                combined = f"{SOVEREIGN_SYSTEM_PROMPT}\n\n[ADVANCED AGENT DIRECTIVE]:\n{injected_prompt}"
                st.markdown(execute_sovereign_ai(user_query_for_agent, custom_system_prompt=combined))
        else:
            st.warning("⚠️ أدخل تعليمات التوجيه والسؤال أولاً.")

# --- تبويب 10: وكلاء القطاعات السيادية ---
with tab10:
    st.subheader("🏭 وكلاء القطاعات السيادية: الصناعة، التجارة، الخدمات، والثقافة والمعلوميات")
    selected_sector = st.selectbox(
        "اختر القطاع الاقتصادي أو المعرفي المستهدف",
        [
            "🏭 قطاع الصناعة والإنشاءات (Industry & Manufacturing Agent)",
            "🛍️ قطاع التجارة والتوزيع (Trade & Commerce Agent)",
            "💼 قطاع الخدمات واللوجستيك (Services & Logistics Agent)",
            "🎨 قطاع الثقافة، التراث والميديا (Culture, Heritage & Media Agent)",
            "💻 قطاع المعلوميات والتحول الرقمي (IT & Digital Transformation Agent)"
        ]
    )
    sector_task = st.text_area("أدخل تفاصيل المشروع أو التحدي المرتبط بالقطاع:", height=140)
    if st.button("🚀 تشغيل وكيل القطاع المختص", type="primary"):
        if sector_task:
            with st.spinner(f"جاري تشغيل وكيل القطاع ({selected_sector})..."):
                sector_directives = {
                    "🏭 قطاع الصناعة": "أنت خبير صناعي ومستشار معامل محترف، تبتكر حلولاً هندسية وإنتاجية متطورة تتفوق في السوق المغربي.",
                    "🛍️ قطاع التجارة": "أنت خبير تجاري استراتيجي في قطاع التوزيع والأسواق بقلعة السراغنة ومراكش، تبتكر طرق نمو استثنائية.",
                    "💼 قطاع الخدمات": "أنت خبير لوجستيك وإدارة عمليات بأساليب ذكية وعالية الكفاءة.",
                    "🎨 قطاع الثقافة": "أنت خبير ثقافي وإعلامي مطلع على الهوية البصرية والتصوير الاحترافي، تقدم أفكاراً إبداعية مميزة.",
                    "💻 قطاع المعلوميات": "أنت مهندس برمجيات ومستشار تحول رقمي، تبني أنظمة آلية متقدمة للمقاولات والشركات."
                }
                chosen_directive = "أنت خبير استراتيجي مؤسسي."
                for k, v in sector_directives.items():
                    if k.split()[1] in selected_sector:
                        chosen_directive = v
                        break
                prompt_full = f"{SOVEREIGN_SYSTEM_PROMPT}\n\n[SECTOR DIRECTIVE]:\n{chosen_directive}\n\nالتحدي:\n{sector_task}"
                st.markdown(execute_sovereign_ai(prompt_full))
        else:
            st.warning("⚠️ أدخل تفاصيل المشروع أولاً.")

# ====================== تذييل المنصة ======================
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #6B7280; font-size: 14px;'>"
    f"Tassaout Vision & Sraghna Media Enterprise Platform | النموذج المحدث: <b>{model}</b> | Autonomous Enterprise Agent 🐅👑📐📸"
    f"</div>", 
    unsafe_allow_html=True
)
