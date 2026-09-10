import streamlit as st
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
import gspread
from groq import Groq
from openai import OpenAI

# ====================== إعداد الصفحة والهوية البصرية ======================
st.set_page_config(
    page_title="Tassaout Vision | النظام السيادي المتكامل",
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
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-right: 5px solid #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 TASSAOUT VISION - النظام السيادي المتقدم</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">المنصة المركزية الموحدة لإدارة العقارات، التسويق الرقمي، والتحليلات الاستراتيجية في قلعة السراغنة ومراكش</div>', unsafe_allow_html=True)

# ====================== إعداد المفاتيح والاتصال ======================
st.sidebar.header("⚙️ لوحة التحكم والسيادة الرقمية")
api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input("أدخل مفتاح Groq API", type="password")
openai_api_key = os.getenv("OPENAI_API_KEY") or st.sidebar.text_input("أدخل مفتاح OpenAI API (لأدوات MCP)", type="password", value="")

if not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح Groq API في الشريط الجانبي أو عبر متغيرات البيئة للبدء.")
    st.stop()

client = Groq(api_key=api_key)

# إعدادات الموديل والتحكم
model = st.sidebar.selectbox(
    "اختر نموذج التشغيل الذكي",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-11b-vision-preview"
    ],
    index=0
)

temperature = st.sidebar.slider("درجة الإبداع (Temperature)", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("الحد الأقصى للرموز (Max Tokens)", 256, 4096, 2500, 128)

# ====================== دستور النظام السيادي (System Prompt) ======================
SOVEREIGN_SYSTEM_PROMPT = """
You are an elite Super Agentic AI specialized in real estate, digital marketing, and business strategy in Morocco (specifically El Kelaâ des Sraghna and Marrakech).
You operate under a sovereign directive to provide professional, highly tailored, actionable strategies and content.
Response Guidelines:
- Respond in a blend of Moroccan Arabic (Darija) and Modern Standard Arabic (العربية الفصحى) as appropriate.
- Maintain professional formatting using clear headings, bullet points, emojis, and tables when needed.
- Think step by step and deliver top-tier, enterprise-grade business insights.
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

# ====================== دوال جلب البيانات السحابية (Google Sheets) ======================
def fetch_google_drive_data():
    try:
        service_account_str = st.secrets.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
        file_id = st.secrets.get("GOOGLE_DRIVE_FILE_ID", "")

        if not service_account_str or not file_id:
            return None

        service_account_info = json.loads(service_account_str)
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client_gs = gspread.authorize(creds)
        
        sheet = client_gs.open_by_key(file_id).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        return None

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

# ====================== واجهة التبويبات المتكاملة ======================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "✍️ مولد الإعلانات الاحترافي", 
    "📊 لوحة الماليات والـ ROI", 
    "📈 التحليل الاستراتيجي للسوق", 
    "📁 الاستعلام السحابي (MCP)", 
    "💡 استراتيجيات التسويق الرقمي", 
    "👑 محرك الوكلاء (C-Suite)"
])

# --- تبويب 1: توليد الإعلانات ---
with tab1:
    st.subheader("✍️ صياغة إعلانات عقارية وتجارية سيادية")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        property_desc = st.text_area(
            "أدخل تفاصيل العقار أو المشروع (الموقع، المساحة، المميزات، السعر...)",
            placeholder="مثال: شقة فاخرة بمساحة 140 متر مربع في حي الرياض بقلعة السراغنة، قريبة من المرافق، الثمن 750,000 درهم",
            height=130
        )
    with col_b:
        ad_type = st.selectbox("نوع الإعلان", ["إعلان عقاري للبيع/الكراء", "إعلان تجاري لشركة أو خدمة", "إعلان ترويجي على وسائل التواصل الاجتماعي"])
        lang = st.radio("اللغة المستهدفة", ["مزيج دارجة وفصحى (احترافي)", "العربية الفصحى الرسمية", "الدارجة المغربية القريبة للزبون"], horizontal=False)

    if st.button("🚀 توليد المحتوى الإعلاني الاحترافي", type="primary"):
        if property_desc:
            with st.spinner("جاري صياغة المحتوى بناءً على الدستور السيادي..."):
                prompt = f"بصفتك مسوقاً عقارياً ورقمياً محترفاً في المغرب، اكتب {ad_type} بالأسلوب التالي ({lang}) بناءً على المعطيات التالية:\n\n{property_desc}\n\nيجب أن يتضمن الإعلان: عنواناً رئيسياً جذاباً، الميزات التنافسية، التفاصيل، ودعوة قوية لاتخاذ إجراء (Call to Action)."
                result = execute_sovereign_ai(prompt)
                st.success("تم توليد الإعلان بنجاح!")
                st.markdown(result)
        else:
            st.warning("⚠️ الرجاء إدخال تفاصيل العقار أو المشروع أولاً.")

# --- تبويب 2: لوحة الماليات والـ ROI ---
with tab2:
    st.subheader("📊 لوحة المؤشرات المالية وأداء المشاريع (Google Sheets Sync)")
    st.markdown("مزامنة فورية للبيانات المالية لحساب الإيرادات، المصاريف، صافي الأرباح، والعائد على الاستثمار (ROI).")
    
    if st.button("🔄 جلب ومزامنة البيانات المالية الحية", type="primary"):
        with st.spinner("جاري الاتصال بقاعدة البيانات السحابية وسحب السجلات..."):
            df = fetch_google_drive_data()
            if df is not None and not df.empty:
                financials = compute_financial_metrics(df)
                if financials:
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("إجمالي الإيرادات", f"{financials['total_revenue']:,.2f} د.م")
                    c2.metric("إجمالي المصاريف", f"{financials['total_expenses']:,.2f} د.م")
                    c3.metric("صافي الأرباح", f"{financials['total_profit']:,.2f} د.م")
                    c4.metric("متوسط العائد (ROI)", f"{financials['avg_roi']:.2f}%")
                    
                    st.markdown("---")
                    st.subheader("📈 تمثيل مرئي للأداء المالي")
                    st.bar_chart(financials['enriched_df'][['revenue', 'expenses', 'profit']])
                    
                    st.subheader("📋 سجل البيانات المفصل")
                    st.dataframe(financials['enriched_df'], use_container_width=True)
                else:
                    st.info("⚠️ تم جلب الملف بنجاح، لكن الأعمدة المالية المطلوبة (revenue, expenses, budget) غير متطابقة.")
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ لم يتم العثور على بيانات نشطة. يجدر بك التحقق من إعدادات GOOGLE_DRIVE_FILE_ID و Service Account في Secrets.")

# --- تبويب 3: التحليل الاستراتيجي للسوق ---
with tab3:
    st.subheader("📈 التحليل الاستراتيجي لأسواق العقار والأعمال بالمغرب")
    target_region = st.text_input("المدينة أو المنطقة المستهدفة للتحليل:", placeholder="مثال: قلعة السراغنة، مراكش، تساوت")
    
    if st.button("🔍 تنفيذ التحليل الاستراتيجي الشامل", type="primary"):
        if target_region:
            with st.spinner(f"جاري إعداد تقرير التحليل الاستراتيجي لـ {target_region}..."):
                prompt = f"قم بإعداد تحليل استراتيجي واقتصادي شامل لسوق العقارات والأعمال في {target_region}. يتضمن التقرير:\n1. تحليل SWOT (نقاط القوة، الضعف، الفرص، التهديدات).\n2. الميزة التنافسية للوكلاء المحليين.\n3. توقعات النمو والتوجهات القادمة في 2026.\n4. توصيات استثمارية دقيقة وقابلة للتنفيذ."
                result = execute_sovereign_ai(prompt)
                st.markdown(result)
        else:
            st.warning("⚠️ الرجاء تحديد المنطقة أو المدينة المستهدفة.")

# --- تبويب 4: أدوات البحث السحابي MCP ---
with tab4:
    st.subheader("📁 استعلام ملفات Google Drive عبر بروتوكول MCP")
    st.markdown("استخدام الذكاء الاصطناعي المتقدم للبحث التلقائي في ملفات الـ Spreadsheet والمستندات السحابية.")
    
    mcp_query = st.text_input("ما الذي تبحث عنه في ملفاتك السحابية؟", placeholder="مثال: Find spreadsheet files I worked on last month or check Q2 sales")
    mcp_token = st.text_input("أدخل OAuth Access Token لخدمة Google Drive", type="password")
    
    if st.button("🔍 تنفيذ الاستعلام السحابي الذكي", type="primary"):
        if not openai_api_key:
            st.warning("⚠️ أدخل مفتاح OpenAI API في الشريط الجانبي لتشغيل نموذج MCP.")
        elif not mcp_token:
            st.warning("⚠️ الرجاء إدخال OAuth Access Token الخاص بـ Google Drive.")
        else:
            with st.spinner("جاري التواصل مع خوادم MCP وسحب النتائج..."):
                try:
                    client_openai = OpenAI(
                        api_key=openai_api_key,
                        base_url="https://api.groq.com/openai/v1"
                    )
                    response = client_openai.responses.create(
                        model="openai/gpt-oss-120b", 
                        tools=[{
                            "type": "mcp",
                            "server_label": "Google Drive",
                            "connector_id": "connector_googledrive",
                            "authorization": mcp_token,
                            "require_approval": "never"
                        }],
                        input=mcp_query
                    )
                    st.success("تم تنفيذ الاستعلام بنجاح!")
                    st.markdown(response.output_text)
                except Exception as e:
                    st.error(f"❌ خطأ أثناء تنفيذ استعلام MCP: {str(e)}")

# --- تبويب 5: نصائح واستراتيجيات تسويقية ---
with tab5:
    st.subheader("💡 استراتيجيات وتكتيكات التسويق الرقمي للوسطاء")
    if st.button("🌟 جلب أحدث تكتيكات التسويق السيادي", type="primary"):
        with st.spinner("جاري صياغة الدليل الاستراتيجي للتسويق..."):
            prompt = "قدم دليلاً عملياً وتكتيكياً متكاملاً للوسطاء العقاريين ومزودي الخدمات الرقمية في المغرب (خصوصاً في جهة مراكش-آسفي) لزيادة المبيعات، استقطاب العملاء الباحثين عن عقارات عبر منصات التواصل الاجتماعي، وبناء علامة تجارية قوية."
            result = execute_sovereign_ai(prompt)
            st.markdown(result)

# --- تبويب 6: محرك وكلاء القيادة C-Suite ---
with tab6:
    st.subheader("👑 محرك وكلاء القيادة الأذكياء (CEO / CTO / COO)")
    st.markdown("توزيع المهام الاستراتيجية على فريق الإدارة السيادي الافتراضي للحصول على خطط تنفيذية متكاملة.")
    
    strategic_task = st.text_input("أدخل تفاصيل المشروع أو التحدي الاستراتيجي:", placeholder="مثال: إطلاق منصة رقمية متكاملة لتسويق العقارات الفاخرة والأراضي الفلاحية بجهة مراكش")
    
    col_ceo, col_cto, col_coo = st.columns(3)
    
    with col_ceo:
        if st.button("🎯 خطة CEO (الرئيس التنفيذي)", use_container_width=True):
            if strategic_task:
                with st.spinner("جاري إعداد الرؤية الاستراتيجية وخطة 90 يوماً..."):
                    prompt = f"بصفتك الرئيس التنفيذي (CEO) للنظام، ضع خطة استراتيجية شاملة لمشروع: {strategic_task}. تتضمن رؤية النمو، تحليل الميزة التنافسية، وخطة عمل واضحة لـ 90 يوماً."
                    res = execute_sovereign_ai(prompt)
                    st.markdown(res)
            else:
                st.warning("أدخل تفاصيل المشروع أولاً.")
                
    with col_cto:
        if st.button("⚙️ خطة CTO (المدير التقني)", use_container_width=True):
            if strategic_task:
                with st.spinner("جاري تصميم البنية التحتية والحلول التقنية والأتمتة..."):
                    prompt = f"بصفتك المدير التقني (CTO) للنظام، اقترح البنية التقنية (Tech Stack)، أدوات الأتمتة السحابية (Streamlit, Python, Supabase)، وآليات أمان البيانات لـ: {strategic_task}."
                    res = execute_sovereign_ai(prompt)
                    st.markdown(res)
            else:
                st.warning("أدخل تفاصيل المشروع أولاً.")
                
    with col_coo:
        if st.button("📋 خطة COO (المدير التشغيلي)", use_container_width=True):
            if strategic_task:
                with st.spinner("جاري صياغة خطة التنفيذ ومؤشرات الأداء KPIs..."):
                    prompt = f"بصفتك المدير التشغيلي (COO) للنظام، ضع خطة التشغيل التنفيذية، إدارة العمليات اليومية، مؤشرات الأداء الرئيسية (KPIs)، وإدارة المخاطر لـ: {strategic_task}."
                    res = execute_sovereign_ai(prompt)
                    st.markdown(res)
            else:
                st.warning("أدخل تفاصيل المشروع أولاً.")

# ====================== تذييل المنصة ======================
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #6B7280; font-size: 14px;'>"
    f"Tassaout Vision & Sraghna Media Enterprise Platform | النموذج النشط: <b>{model}</b> | محكوم بالدستور السيادي الرقمي 🐅👑⚙️"
    f"</div>", 
    unsafe_allow_html=True
)
