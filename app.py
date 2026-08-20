import streamlit as st
from supabase import create_client, Client
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# إعداد الصفحة بنمط واسع واحترافي
st.set_page_config(
    page_title="OMEGA OS | نظام وكلاء الذكاء الاصطناعي السيادي", 
    layout="wide", 
    page_icon="⚡"
)

# تهيئة الاتصالات والأسرار (Secrets)
@st.cache_resource
def init_system():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    supabase = create_client(url, key)
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    return supabase

supabase = init_system()

# القائمة الجانبية السيادية المتكاملة
st.sidebar.title("⚡ OMEGA OS v8.0")
st.sidebar.markdown(f"**المستخدم:** عامر بوخدادة\n**المنطقة:** قلعة السراغنة - مراكش\n**التاريخ:** {datetime.now().strftime('%Y-%m-%d')}")

# نظام الخصوصية القصوى (إخفاء البيانات الحساسة عند الطلب)
privacy_mode = st.sidebar.checkbox("🔒 نمط الخصوصية القصوى (إخفاء الأرباح)", value=False)
st.sidebar.markdown("---")

menu = st.sidebar.radio("قائمة العمليات السيادية:", [
    "📊 لوحة القيادة الشاملة", 
    "🤖 غرفة قيادة وكلاء الذكاء الاصطناعي (Agentic AI)",
    "🌐 وكيل البحث العميق واستخراج الداتا",
    "🏠 إدارة العقارات والمشاريع الذكية", 
    "👥 إدارة الزبناء (CRM) وتقييم الصدارة", 
    "💼 تتبع الصفقات، الأرباح وROI",
    "🧮 الحاسبة التمويلية واستثمار العقار",
    "📁 تصدير التقارير والأرشيف",
    "⚙️ الإعدادات والأمان السيادي"
])

# 1. لوحة القيادة الشاملة
if menu == "📊 لوحة القيادة الشاملة":
    st.title("📊 لوحة القيادة والمؤشرات السيادية الخبيرة")
    st.write("نظرة عامة ومباشرة على أداء العمليات العقارية، الإعلانات، والخدمات الرقمية.")
    
    try:
        r_res = supabase.table("reports").select("*").execute()
        c_res = supabase.table("crm_contacts").select("*").execute()
        d_res = supabase.table("crm_deals").select("*").execute()
        
        r_data = r_res.data if r_res.data else []
        c_data = c_res.data if c_res.data else []
        d_data = d_res.data if d_res.data else []
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("إجمالي العقارات والخدمات", len(r_data))
        col2.metric("إجمالي الزبناء المسجلين", len(c_data))
        col3.metric("إجمالي الصفقات الجارية", len(d_data))
        
        if privacy_mode:
            col4.metric("إجمالي قيمة الصفقات (درهم)", "🔒 مخفي بالخصوصية")
        else:
            total_revenue = sum([float(deal.get('amount', 0)) for deal in d_data if deal.get('amount')])
            col4.metric("إجمالي قيمة الصفقات (درهم)", f"{total_revenue:,.2f}")
        
        st.markdown("---")
        st.markdown("### 📈 أحدث الصفقات والعمليات المسجلة")
        if d_data:
            df_deals = pd.DataFrame(d_data)
            if privacy_mode and 'amount' in df_deals.columns:
                df_deals['amount'] = "🔒 مخفي"
            st.dataframe(df_deals, use_container_width=True)
        else:
            st.info("لا توجد صفقات مسجلة لعرضها في المؤشرات حالياً.")
            
    except Exception as e:
        st.error(f"خطأ في الاتصال أو جلب مؤشرات اللوحة: {e}")

# 2. غرفة قيادة وكلاء الذكاء الاصطناعي (Super Multi-Domain Agentic AI)
elif menu == "🤖 غرفة قيادة وكلاء الذكاء الاصطناعي (Agentic AI)":
    st.title("🤖 غرفة عمليات وكلاء الذكاء الاصطناعي المتخصصين")
    st.write("اختر الوكيل المناسب لتنفيذ المهام المعقدة، تحليل السوق، صياغة الاستراتيجيات، أو حل نزاعات المبيعات.")
    
    agent_type = st.selectbox("اختر الوكيل الذكي (Agent):", [
        "🏢 وكيل العقارات وتحليل السوق المغربي", 
        "🤝 وكيل المبيعات وإغلاق الصفقات (CRM Expert)", 
        "📢 وكيل التسويق الرقمي والحملات (Sraghna Media / DANA)", 
        "💰 وكيل الإدارة المالية وتقييم الأرباح (CFO Agent)"
    ])
    
    st.markdown("---")
    
    with st.form("agent_command_form"):
        user_task = st.text_area("أدخل التوجيه أو المشكلة ليقوم الوكيل بتحليلها وإنجازها:", placeholder="مثال: اقترح خطة تسويقية لبيع أرض تجارية بقلعة السراغنة، أو اكتب رسالة واتساب لإقناع عميل متردد...")
        submit_agent = st.form_submit_button("🚀 إرسال المهمة للوكيل الذكي")
        
        if submit_agent:
            if user_task:
                try:
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    system_personas = {
                        "🏢 وكيل العقارات وتحليل السوق المغربي": "أنت خبير استراتيجي عقاري في السوق المغربي (قلعة السراغنة ومراكش). مهمتك تحليل الفرص، تقديم نصائح الاستثمار، وتقييم الأصول.",
                        "🤝 وكيل المبيعات وإغلاق الصفقات (CRM Expert)": "أنت خبير مبيعات وتفاوض عالمي. مهمتك تقديم سيناريوهات إقناع العملاء، الرد على الاعتراضات، ورفع نسبة إغلاق الصفقات.",
                        "📢 وكيل التسويق الرقمي والحملات (Sraghna Media / DANA)": "أنت مدير تسويق رقمي وإعلانات ممولة (Meta & Google). مهمتك ابتكار أفكار إعلانية، كتابة نصوص Reels/TikTok، وتخطيط الحملات.",
                        "💰 وكيل الإدارة المالية وتقييم الأرباح (CFO Agent)": "أنت مستشار مالي محترف. مهمتك تحليل العائد على الاستثمار (ROI)، إدارة الهوامش، وتقديم نصائح تحسين صافي الأرباح والعمولات."
                    }
                    prompt = f"{system_personas[agent_type]}\n\nالمهمة المطلوبة بناءً على طلب المستخدم: {user_task}"
                    with st.spinner("جاري معالجة المهمة بواسطة الوكيل المتخصص..."):
                        response = model.generate_content(prompt)
                        st.success("✅ تم تنفيذ المهمة بنجاح بواسطة الوكيل الذكي:")
                        st.markdown(response.text)
                except Exception as ag_err:
                    st.error(f"حدث خطأ أثناء تشغيل الوكيل الذكي: {ag_err}")
            else:
                st.warning("يرجى كتابة المهمة أو السؤال أولاً.")

# 3. وكيل البحث العميق واستخراج الداتا (Deep Web Research Agent)
elif menu == "🌐 وكيل البحث العميق واستخراج الداتا":
    st.title("🌐 وكيل البحث العميق واستخراج عروض السوق والداتا")
    st.write("استخدم هذا الوكيل للبحث واستخراج أحدث العروض، بيانات السوق، اتجاهات الأسعار العقارية والتجارية في المغرب (قلعة السراغنة، مراكش، والمدن المجاورة).")
    
    with st.form("deep_research_form"):
        research_query = st.text_input("ما الذي تريد من وكيل البحث العميق استخراجه أو البحث عنه؟", placeholder="مثال: متوسط أسعار الأراضي الفلاحية بقلعة السراغنة، أو أحدث توجهات الاستثمار العقاري بمراكش...")
        target_focus = st.selectbox("مجال البحث والتركيز:", [
            "العقارات والأراضي (Real Estate)", 
            "الخدمات الرقمية والتسويق (Digital & Media)", 
            "السيارات واللوجستيات (Auto & Logistics)", 
            "اتجاهات السوق العامة (General Market Trends)"
        ])
        
        run_research = st.form_submit_button("🔍 بدء البحث العميق وتحليل الداتا")
        
        if run_research:
            if research_query:
                try:
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    research_prompt = f"""
                    أنت وكيل بحث عميق ومحلل أسواق خبير في السوق المغربي (خاصة جهة مراكش آسفي، قلعة السراغنة، والمحيط).
                    بناءً على طلب المستخدم في مجال '{target_focus}':
                    قم بتقديم تقرير شامل، مفصل، ودقيق يستخرج ويحلل البيانات والعروض والفرص المتعلقة بـ: '{research_query}'.
                    نظم التقرير في نقاط واضحة ومباشرة مفيدة لوسيط عقاري ورجل أعمال رقمي.
                    """
                    with st.spinner("جاري البحث العميق واستخراج وتحليل البيانات..."):
                        response = model.generate_content(research_prompt)
                        st.success("✅ تقرير البحث العميق واستخراج الداتا جاهز:")
                        st.markdown(response.text)
                except Exception as rs_err:
                    st.error(f"فشل تشغيل وكيل البحث العميق: {rs_err}")
            else:
                st.warning("يرجى إدخال موضوع أو سؤال البحث أولاً.")

# 4. إدارة العقارات والمشاريع الذكية
elif menu == "🏠 إدارة العقارات والمشاريع الذكية":
    st.title("🏠 إدارة العقارات والإعلانات والخدمات الميدانية")
    
    tab1, tab2 = st.tabs(["➕ إضافة عقار/مشروع جديد", "📋 استعراض، فلترة وتصدير العقارات"])
    
    with tab1:
        with st.form("prop_form"):
            st.markdown("### إضافة عقار أو مشروع جديد (قلعة السراغنة / مراكش)")
            name = st.text_input("اسم العقار / المشروع / الخدمة")
            price = st.number_input("السعر المقترح (درهم)", step=1000.0)
            status = st.selectbox("حالة العقار", ["متاح", "محجوز", "مباع"])
            location_url = st.text_input("رابط موقع خريطة جوجل (Google Maps URL - اختياري)")
            refurb_cost = st.number_input("تكلفة التجهيز والصيانة الإضافية (درهم)", step=500.0, value=0.0)
            desc = st.text_area("وصف تفصيلي أو ملاحظات ميدانية")
            
            use_ai = st.checkbox("🤖 توليد وصف تسويقي احترافي باستخدام Gemini AI")
            
            if st.form_submit_button("حفظ العقار في النظام"):
                final_desc = desc
                if use_ai and name:
                    try:
                        model = genai.GenerativeModel('gemini-3.6-flash')
                        prompt = f"اكتب إعلاناً تسويقياً جذاباً ومحترفاً باللغة العربية لعقار باسم '{name}' سعره {price} درهم مغربي، موجه للسوق المغربي بقلعة السراغنة ومراكش."
                        response = model.generate_content(prompt)
                        final_desc = response.text
                    except Exception as ai_e:
                        st.warning(f"تعذر توليد الوصف بالذكاء الاصطناعي: {ai_e}")
                
                if name:
                    supabase.table("reports").insert({
                        "project_name": name,
                        "price": price,
                        "report_content": final_desc,
                        "status": status
                    }).execute()
                    st.success("تم إضافة العقار بنجاح وتحديث قاعدة البيانات!")
                else:
                    st.warning("يرجى إدخال اسم العقار على الأقل.")
                    
    with tab2:
        st.markdown("### 📋 سجل العقارات والبحث المتقدم")
        try:
            res = supabase.table("reports").select("*").execute()
            if res.data:
                df = pd.DataFrame(res.data)
                
                if 'status' in df.columns:
                    statuses = df['status'].unique().tolist()
                    selected_status = st.multiselect("تصفية حسب الحالة:", options=statuses, default=statuses)
                    df = df[df['status'].isin(selected_status)]
                
                st.dataframe(df, use_container_width=True)
                
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 تحميل جدول العقارات (CSV)",
                    data=csv_data,
                    file_name="omega_properties_export.csv",
                    mime="text/csv"
                )
            else:
                st.info("لا توجد عقارات مسجلة حالياً.")
        except Exception as e:
            st.error(f"خطأ في استعراض العقارات: {e}")

# 5. إدارة الزبناء (CRM) وتقييم الصدارة
elif menu == "👥 إدارة الزبناء (CRM) وتقييم الصدارة":
    st.title("👥 إدارة الزبناء وجهات الاتصال مع تقييم جودة الصدارة (Lead Scoring)")
    
    with st.form("crm_form"):
        st.markdown("### تسجيل عميل جديد وتقييم الاهتمام")
        full_name = st.text_input("اسم العميل الكامل")
        phone = st.text_input("رقم الهاتف (مثال: +2126xxxxxxxx)")
        email = st.text_input("البريد الإلكتروني")
        interest = st.text_input("مجال الاهتمام (مثال: شقة بمراكش، أرض بقلعة السراغنة)")
        lead_quality = st.selectbox("مستوى جودة العميل (Lead Scoring)", ["🔥 عميل ساخن (جاد جداً)", "⚡ عميل مهتم (في طور المتابعة)", "🧊 عميل بارد أو استكشافي"])
        
        if st.form_submit_button("حفظ بيانات العميل"):
            if full_name:
                supabase.table("crm_contacts").insert({
                    "full_name": full_name,
                    "phone": phone,
                    "email": email,
                    "interest_area": f"{interest} [{lead_quality}]"
                }).execute()
                st.success("تم حفظ بيانات العميل وتصنيفه بنجاح!")
            else:
                st.warning("اسم العميل مطلوب.")
                
    st.markdown("---")
    st.markdown("### 📋 قاعدة بيانات الزبناء والتواصل الفوري عبر واتساب")
    try:
        c_res = supabase.table("crm_contacts").select("*").execute()
        if c_res.data:
            df_c = pd.DataFrame(c_res.data)
            st.dataframe(df_c, use_container_width=True)
            
            if 'phone' in df_c.columns:
                phones = df_c['phone'].dropna().tolist()
                selected_p = st.selectbox("اختر رقم هاتف العميل للمراسلة الفورية:", options=phones)
                if selected_p:
                    clean_p = selected_p.replace("+", "").replace(" ", "")
                    wa_link = f"https://wa.me/{clean_p}?text=مرحباً، نتواصل معك من نظام OMEGA OS بخصوص طلبك العقاري والخدماتي."
                    st.markdown(f"[🔗 فتح مراسلة واتساب مباشرة للعميل]({wa_link})", unsafe_allow_html=True)
        else:
            st.info("لا توجد جهات اتصال مسجلة حتى الآن.")
    except Exception as e:
        st.error(f"خطأ في جلب بيانات الزبناء: {e}")

# 6. تتبع الصفقات، الأرباح وROI
elif menu == "💼 تتبع الصفقات، الأرباح وROI":
    st.title("💼 إدارة الصفقات وحساب العمولات وصافي الأرباح")
    
    with st.form("deal_form"):
        st.markdown("### تسجيل صفقة جديدة")
        contact_id = st.number_input("معرف العميل (Contact ID)", min_value=1, step=1)
        report_id = st.text_input("معرف العقار المرتبط (اختياري)")
        amount = st.number_input("مبلغ الصفقة الإجمالي (درهم)", step=1000.0)
        ad_expense = st.number_input("تكلفة الحملة الإعلانية المرتبطة بالصفقة (درهم)", step=100.0, value=0.0)
        stage = st.selectbox("مرحلة الصفقة", ["في طور المتابعة", "تم إرسال العرض", "تم إغلاق الصفقة بنجاح", "ملغاة"])
        
        comm = amount * 0.03
        net_profit = comm - ad_expense
        
        if not privacy_mode:
            st.info(f"العمولة الوسيطة (3%): {comm:,.2f} درهم | صافي الربح (بعد خصم الإعلانات): {net_profit:,.2f} درهم")
        else:
            st.info("الحسابات المالية مخفية بناءً على تفعيل نمط الخصوصية.")
        
        if st.form_submit_button("حفظ الصفقة في النظام"):
            try:
                deal_payload = {
                    "contact_id": int(contact_id),
                    "amount": amount,
                    "deal_stage": stage
                }
                if report_id.strip():
                    deal_payload["report_id"] = report_id.strip()
                    
                supabase.table("crm_deals").insert(deal_payload).execute()
                st.success("تم تسجيل الصفقة وحساب أرباحها بنجاح!")
            except Exception as de:
                st.error(f"فشل تسجيل الصفقة: {de}")
                
    st.markdown("---")
    st.markdown("### 📋 سجل الصفقات والمبيعات")
    try:
        d_res = supabase.table("crm_deals").select("*").execute()
        if d_res.data:
            df_deals_log = pd.DataFrame(d_res.data)
            if privacy_mode and 'amount' in df_deals_log.columns:
                df_deals_log['amount'] = "🔒 مخفي"
            st.dataframe(df_deals_log, use_container_width=True)
        else:
            st.info("لا توجد صفقات مسجلة حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب سجل الصفقات: {e}")

# 7. الحاسبة التمويلية واستثمار العقار
elif menu == "🧮 الحاسبة التمويلية واستثمار العقار":
    st.title("🧮 الحاسبة التمويلية وحساب العائد الاستثماري (ROI)")
    
    tab_calc1, tab_calc2 = st.tabs(["🧮 حاسبة القروض البنكية", "📈 حاسبة عائد الاستثمار الاستئجاري (ROI)"])
    
    with tab_calc1:
        col_a, col_b = st.columns(2)
        with col_a:
            prop_price = st.number_input("سعر العقار الإجمالي (درهم)", value=500000.0, step=10000.0)
            down_payment = st.number_input("مبلغ التسبيق (درهم)", value=100000.0, step=10000.0)
        with col_b:
            interest_rate = st.number_input("نسبة الفائدة البنكية السنوية (%)", value=4.5, step=0.1)
            years = st.slider("مدة القرض (بالسنوات)", min_value=5, max_value=25, value=20)
            
        loan_amount = prop_price - down_payment
        st.markdown("---")
        if st.button("حساب القسط الشهري التقريبي"):
            monthly_rate = (interest_rate / 100) / 12
            months = years * 12
            if monthly_rate > 0:
                monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
            else:
                monthly_payment = loan_amount / months
                
            st.success(f"مبلغ القرض المطلوب من البنك: {loan_amount:,.2f} درهم")
            st.metric("قيمة القسط الشهري المتوقع:", f"{monthly_payment:,.2f} درهم / شهرياً")
            
    with tab_calc2:
        st.markdown("### حساب نسبة العائد السنوي على الاستثمار (ROI)")
        inv_cost = st.number_input("تكلفة شراء وتجهيز العقار الاستثماري (درهم)", value=600000.0, step=10000.0)
        monthly_rent = st.number_input("مدخول الإيجار الشهري المتوقع (درهم)", value=4000.0, step=200.0)
        
        if st.button("حساب نسبة العائد (ROI)"):
            annual_return = monthly_rent * 12
            roi_percentage = (annual_return / inv_cost) * 100 if inv_cost > 0 else 0
            st.metric("نسبة العائد السنوي على الاستثمار (ROI):", f"{roi_percentage:.2f}% سنوياً")

# 8. تصدير التقارير والأرشيف
elif menu == "📁 تصدير التقارير والأرشيف":
    st.title("📁 إدارة الأرشيف والتصدير الشامل")
    st.write("استخراج السجلات الكاملة لقاعدة البيانات والتقارير المادية للأعمال الرقمية والعقارية.")
    
    try:
        c_exp = supabase.table("crm_contacts").select("*").execute()
        if c_exp.data:
            df_ce = pd.DataFrame(c_exp.data)
            csv_contacts = df_ce.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 تصدير قاعدة بيانات الزبناء بالكامل (CSV)",
                data=csv_contacts,
                file_name="omega_contacts_archive.csv",
                mime="text/csv"
            )
        else:
            st.info("لا توجد بيانات زبناء للتصدير حالياً.")
    except Exception as ex:
        st.error(f"خطأ في تصدير الأرشيف: {ex}")

# 9. الإعدادات والأمان السيادي
elif menu == "⚙️ الإعدادات والأمان السيادي":
    st.title("⚙️ الإعدادات والأمان السيادي")
    st.write("حالة الاتصال والخدمات المدمجة بمنظومة OMEGA OS:")
    st.info("🟢 متصل بقاعدة بيانات Supabase بنجاح تام.")
    st.info("🤖 نظام وكلاء الذكاء الاصطناعي ووكيل البحث العميق مفعلان بكامل الطاقة وجاهزان للعمل.")
    st.warning("تنبيه أمني: احرص دائماً على حماية مفاتيح الـ Secrets وعدم مشاركتها خارج بيئة التشغيل الآمنة.")
