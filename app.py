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

# إدارة الجلسة للمستخدم
if "user" not in st.session_state:
    st.session_state.user = None

st.title("👑 OMEGA OS - Elite Core")
st.subheader("تسجيل الدخول السيادي - وكالة تساوت الرقمية")

# واجهة المصادقة إن لم يتم تسجيل الدخول
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        email = st.text_input("الإيميل المهني", key="login_email")
        password = st.text_input("كلمة السر", type="password", key="login_password")
        if st.button("دخول سيادي"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            except Exception as e:
                st.error(f"خطأ في الدخول: {e}")
                
    with tab2:
        new_email = st.text_input("الإيميل المهني الجديد", key="reg_email")
        new_password = st.text_input("كلمة السر الجديدة", type="password", key="reg_password")
        if st.button("إنشاء الحساب"):
            try:
                res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                st.success("تم إنشاء الحساب! تحقق من بريدك أو قم بتسجيل الدخول.")
            except Exception as e:
                st.error(f"خطأ في الإنشاء: {e}")
else:
    # واجهة النظام بعد تسجيل الدخول الناجح
    user = st.session_state.user
    st.sidebar.success(f"مرحباً بك: {user.email}")
    
    if st.sidebar.button("تسجيل الخروج"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
        
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
                        "report_type": report_type,
                        "user_id": user.id
                    }).execute()
                    st.success("تم حفظ التقرير بنجاح في قاعدة البيانات السيادية!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الحفظ: {e}")
            else:
                st.warning("المرجو ملء جميع الحقول الأساسية.")
                
        st.subheader("سجل تقاريرك المحفوظة")
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
                        "description": description,
                        "user_id": user.id
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
                    "content": memo_content,
                    "user_id": user.id
                }).execute()
                st.success("تم الحفظ في الذاكرة!")
        
        memos = supabase.table("gemini_memo").select("*").execute()
        if memos.data:
            for m in memos.data:
                st.write(f"💡 {m.get('content')}")
