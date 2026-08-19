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
    
    # النصوص الجاهزة للإعلان العقاري في قلعة السراغنة
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
                # التوافق مع الأعمدة الفعلية للجدول
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
        ads_data = supabase.table("instant_ads").select("*").execute()
        if ads_data.data:
            for ad in ads_data.data:
                st.info(f"📌 **{ad.get('content')}**\n\n{ad.get('message')}")
        else:
            st.info("لا توجد إعلانات مسجلة حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب الإعلانات: {e}")

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
    
    memos = supabase.table("gemini_memo").select("*").execute()
    if memos.data:
        for m in memos.data:
            st.write(f"💡 {m.get('content')}")
