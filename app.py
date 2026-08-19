import streamlit as st
from supabase import create_client, Client
import os
from google import genai
from fpdf import FPDF
import tempfile

# إعدادات الصفحة السيادية
st.set_page_config(
    page_title="OMEGA OS - Elite Core [PDF Master Edition]",
    page_icon="👑",
    layout="wide"
)

# الربط الآمن مع Supabase (حماية الأسرار السيادية)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

st.title("👑 OMEGA OS - Elite Core [PDF Master Edition]")
st.sidebar.success("مرحباً بك يا رئيس (الوصول السيادي المطلق)")

# القائمة السيادية الشاملة لكافة الوحدات
menu = st.sidebar.selectbox(
    "اختر الوحدة السيادية", 
    [
        "رصد الميدان والتقارير", 
        "إدارة الإعلانات", 
        "الذاكرة الرقمية (Gemini Memo)", 
        "الوكيل الذكي الخارق (Max AI Agent)"
    ]
)

# ==========================================
# 1. وحدة رصد الميدان والتقارير + مصنع الـ PDF
# ==========================================
if menu == "رصد الميدان والتقارير":
    st.header("📊 وحدة رصد الميدان والتقارير الرسمية")
    
    project_name = st.text_input("اسم المشروع / الورش")
    report_content = st.text_area("محتوى التقرير أو التحليل")
    report_type = st.selectbox("نوع التقرير", ["ورش", "عقار", "صفقات"])
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("حفظ التقرير بأمان في القاعدة"):
            if project_name and report_content:
                try:
                    supabase.table("reports").insert({
                        "project_name": project_name,
                        "report_content": report_content,
                        "report_type": report_type
                    }).execute()
                    st.success("تم حفظ التقرير بنجاح في قاعدة البيانات السيادية!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الحفظ: {e}")
            else:
                st.warning("المرجو ملء جميع الحقول الأساسية.")

    st.markdown("---")
    st.subheader("📁 الأرشيف السيادي وتوليد ملفات PDF")
    
    try:
        # جلب التقارير مرتبة تنازلياً حسب تاريخ الإنشاء
        reports_data = supabase.table("reports").select("*").order("created_at", desc=True).execute()
        
        if reports_data.data:
            for idx, r in enumerate(reports_data.data):
                p_name = r.get('project_name', 'مفهرس بدون عنوان')
                r_type = r.get('report_type', 'عام')
                r_date = r.get('created_at', '')
                r_text = r.get('report_content', '')
                
                with st.expander(f"📌 [{r_type}] {p_name} — ({r_date})"):
                    st.write(r_text)
                    
                    # زر توليد وتنزيل الـ PDF لكل تقرير
                    if st.button(f"📄 تصدير كـ PDF رسمي", key=f"pdf_btn_{r.get('id', idx)}"):
                        try:
                            # إنشاء ملف PDF مؤقت
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", size=12)
                            
                            # كتابة محتوى التقرير
                            pdf.cell(200, 10, txt="OMEGA OS - Official Report", ln=True, align="C")
                            pdf.ln(10)
                            pdf.cell(200, 10, txt=f"Project: {p_name}", ln=True)
                            pdf.cell(200, 10, txt=f"Type: {r_type}", ln=True)
                            pdf.cell(200, 10, txt=f"Date: {r_date}", ln=True)
                            pdf.ln(10)
                            
                            # تقسيم النص الطويل
                            pdf.multi_cell(0, 10, txt=r_text)
                            
                            # حفظ الملف في مسار مؤقت
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                                pdf.output(tmp_file.name)
                                tmp_path = tmp_file.name
                                
                            with open(tmp_path, "rb") as pdf_file:
                                st.download_button(
                                    label="⬇️ انقر هنا لتحميل وثيقة PDF الرسمية",
                                    data=pdf_file,
                                    file_name=f"OMEGA_Report_{p_name}.pdf",
                                    mime="application/pdf",
                                    key=f"dl_pdf_{r.get('id', idx)}"
                                )
                        except Exception as pdf_err:
                            st.error(f"تعذر توليد الـ PDF: {pdf_err}")
        else:
            st.info("لا توجد تقارير مسجلة حتى الآن.")
    except Exception as e:
        st.error(f"تعذر جلب سجل التقارير: {e}")

# ==========================================
# 2. وحدة إدارة الإعلانات الفورية
# ==========================================
elif menu == "إدارة الإعلانات":
    st.header("📢 وحدة إدارة الإعلانات الفورية (instant_ads)")
    
    default_title = "عرض عقاري مميز: بقع، شقق ومكاتب في قلعة السراغنة"
    default_desc = """🌟 فرص ذهبية للاستثمار والسكن في قلب قلعة السراغنة! 🌟
خدمات تساوت الرقمية للعقار توفر لكم:
* بقع سكنية والتجارية بمواقع استراتيجية.
* شقق عصرية بتشطيبات راقية.
* مكاتب مهنية مجهزة.
📞 للاتصال والحجز: 0691897126"""

    title = st.text_input("عنوان الإعلان", value=default_title)
    description = st.text_area("تفاصيل الإعلان", value=default_desc, height=150)
    
    if st.button("نشر الإعلان"):
        if title and description:
            try:
                supabase.table("instant_ads").insert({
                    "content": title,
                    "message": description
                }).execute()
                st.success("تم نشر الإعلان العقاري بنجاح في قاعدة البيانات!")
            except Exception as e:
                st.error(f"خطأ أثناء النشر: {e}")
        else:
            st.warning("املأ العنوان والوصف.")
            
    st.subheader("الإعلانات المنشورة حالياً")
    try:
        ads_data = supabase.table("instant_ads").select("*").order("created_at", desc=True).execute()
        if ads_data.data:
            for ad in ads_data.data:
                st.info(f"📌 **{ad.get('content')}**\n\n{ad.get('message')}")
        else:
            st.info("لا توجد إعلانات مسجلة حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب الإعلانات: {e}")

# ==========================================
# 3. الذاكرة الرقمية
# ==========================================
elif menu == "الذاكرة الرقمية (Gemini Memo)":
    st.header("🧠 الذاكرة الرقمية")
    memo_content = st.text_area("محتوى المذكرة أو الفكرة")
    if st.button("حفظ في الذاكرة"):
        if memo_content:
            try:
                supabase.table("gemini_memo").insert({
                    "content": memo_content
                }).execute()
                st.success("تم الحفظ في الذاكرة!")
            except Exception as e:
                st.error(f"خطأ: {e}")
    
    memos = supabase.table("gemini_memo").select("*").order("created_at", desc=True).execute()
    if memos.data:
        for m in memos.data:
            st.write(f"💡 {m.get('content')}")

# ==========================================
# 4. الوكيل الذكي الخارق (نظام Perplexity الشامل للمغرب)
# ==========================================
elif menu == "الوكيل الذكي الخارق (Max AI Agent)":
    st.header("🌐 المحرك الذكي السيادي الشامل [Perplexity Style]")
    st.write("مرحباً بك يا رئيس. هذا المحرك مفعل للبحث المفتوح في شبكة الإنترنت عبر كافة جهات المغرب (عقارات، صفقات، طلبات، استثمار، وتحليلات شاملة).")

    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    
    target_region = st.selectbox(
        "نطاق البحث الجغرافي:", 
        [
            "جميع جهات المغرب (وطني)", 
            "جهة مراكش آسفي", 
            "قلعة السراغنة والنواحي", 
            "الجهة الشرقية", 
            "جهة الدار البيضاء سطات", 
            "جهة الرباط سلا القنيطرة",
            "جهة طنجة تطوان الحسيمة",
            "جهة سوس ماسة"
        ]
    )
    
    user_query = st.text_area(
        "ما الذي تبحث عنه أو تريد استكشافه في الإنترنت؟", 
        value="ابحث عن أحدث الفرص، الطلبات، أو العروض المتاحة في السوق المغربي مع تحليل دقيق."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        launch_search = st.button("🔍 ابحث واقترح عبر الويب")
    with col2:
        auto_archive = st.checkbox("أرشفة النتائج تلقائياً في قاعدة البيانات", value=True)
    
    if launch_search:
        if user_query:
            with st.spinner("جاري التمشيط الشامل للإنترنت وتحليل البيانات الحية..."):
                try:
                    client = genai.Client(api_key=gemini_api_key)
                    
                    system_prompt = (
                        f"أنت محرك بحث ووكيل استخباري ذكي ومحترف (يشبه Perplexity) مخصص للسوق المغربي. "
                        f"نطاق البحث المستهدف حالياً هو: {target_region}. "
                        "قم بالبحث الحقيقي في الإنترنت عبر أدوات البحث، واستخرج تفاصيل دقيقة، روابط، إحصائيات، "
                        "أو طلبات عروض، وقدم إجابة مهيكلة، عميقة، ومفصلة باللغة العربية مع ذكر المصادر إن وجدت."
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=f"{system_prompt}\n\nالسؤال أو البحث المطلوب: {user_query}",
                        config={
                            'tools': [{'google_search': {}}],
                        }
                    )
                    
                    search_result = response.text
                    st.success("تم إنجاز عملية البحث والاستخراج بنجاح:")
                    st.markdown(search_result)
                    
                    if response.candidates and response.candidates[0].grounding_metadata:
                        metadata = response.candidates[0].grounding_metadata
                        if hasattr(metadata, 'grounding_chunks') and metadata.grounding_chunks:
                            st.subheader("🔗 المصادر الحية المستند إليها:")
                            for chunk in metadata.grounding_chunks:
                                if chunk.web:
                                    st.markdown(f"- [{chunk.web.title}]({chunk.web.uri})")
                    
                    if auto_archive:
                        try:
                            supabase.table("reports").insert({
                                "project_name": f"بحث شبكي: {target_region}",
                                "report_content": f"السؤال: {user_query}\n\nالنتائج:\n{search_result}",
                                "report_type": "صفقات"
                            }).execute()
                            st.info("💾 تم حفظ واستصدار التقرير الشبكي في قاعدة بيانات Supabase بنجاح.")
                        except Exception as db_err:
                            st.warning(f"تم عرض النتائج لكن تعذر الحفظ التلقائي: {db_err}")
                            
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالمحرك الذكي: {e}")
        else:
            st.warning("المرجو كتابة ما تريد البحث عنه أولاً.")
