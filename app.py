import streamlit as st
from supabase import create_client, Client

# إعدادات الصفحة
st.set_page_config(
    page_title="OMEGA OS - Elite Core",
    page_icon="👑",
    layout="wide"
)

# الربط مع Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://rbyjjnkhdjfksyodiujs.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "YOUR_SUPABASE_KEY")

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

st.title("👑 OMEGA OS - Elite Core")
st.sidebar.success("مرحباً بك يا رئيس (الوصول السيادي المباشر)")

# اختيار الوحدة السيادية مباشرة بدون قيود إيميل
menu = st.sidebar.selectbox("اختر الوحدة السيادية", ["رصد الميدان والتقارير", "إدارة الإعلانات", "الذاكرة الرقمية (Gemini Memo)"])

if menu == "رصد الميدان والتقارير":
    st.header("📊 وحدة رصد الميدان والتقارير")
    project_name = st.text_input("اسم المشروع / الورش")
    report_content = st.text_area("محتوى التقرير أو التحليل")
    report_type = st.selectbox("نوع التقرير", ["ورش", "عقار", "صفقات"])
    
    if st.button("حفظ التقرير بأمان"):
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
            
    st.subheader("سجل التقارير المحفوظة")
    try:
        reports_data = supabase.table("reports").select("*").execute()
        if reports_data.data:
            for r in reports_data.data:
                st.info(f"**{r.get('project_name')}** ({r.get('report_type')}) - {r.get('created_at')}\n\n{r.get('report_content')}")
        else:
            st.info("لا توجد تقارير مسجلة حتى الآن.")
    except Exception as e:
        st.error(f"تعذر جلب التقارير: {e}")

elif menu == "إدارة الإعلانات":
    st.header("📢 وحدة إدارة الإعلانات الفورية (instant_ads)")
    title = st.text_input("عنوان الإعلان")
    description = st.text_area("تفاصيل الإعلان")
    
    if st.button("نشر الإعلان"):
        if title and description:
            try:
                supabase.table("instant_ads").insert({
                    "title": title,
                    "description": description
                }).execute()
                st.success("تم نشر الإعلان بنجاح!")
            except Exception as e:
                st.error(f"خطأ: {e}")
        else:
            st.warning("املأ العنوان والوصف.")
            
    ads_data = supabase.table("instant_ads").select("*").execute()
    if ads_data.data:
        for ad in ads_data.data:
            st.write(f"📌 **{ad.get('title')}**: {ad.get('description')}")

elif menu == "الذاكرة الرقمية (Gemini Memo)":
    st.header("🧠 الذاكرة الرقمية")
    memo_content = st.text_area("محتوى المذكرة أو الفكرة")
    if st.button("حفظ في الذاكرة"):
        if memo_content:
            supabase.table("gemini_memo").insert({
                "content": memo_content
            }).execute()
            st.success("تم الحفظ في الذاكرة!")
    
    memos = supabase.table("gemini_memo").select("*").execute()
    if memos.data:
        for m in memos.data:
            st.write(f"💡 {m.get('content')}")
