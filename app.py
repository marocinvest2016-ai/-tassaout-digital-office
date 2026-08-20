import streamlit as st
from supabase import create_client, Client
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="OMEGA OS | نظام إدارة الأعمال", layout="wide")

# إعداد الاتصال باستخدام Secrets
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# القائمة الجانبية
st.sidebar.title("⚡ OMEGA OS")
menu = st.sidebar.radio("العمليات:", ["لوحة القيادة", "إدارة العقارات", "إدارة CRM", "متابعة الصفقات"])

# 1. لوحة القيادة
if menu == "لوحة القيادة":
    st.title("📊 لوحة القيادة العامة")
    st.write("مرحباً بك في نظامك السيادي لإدارة العمليات والعقارات.")
    
    try:
        # جلب إحصائيات سريعة
        reports_res = supabase.table("reports").select("id", count="exact").execute()
        contacts_res = supabase.table("crm_contacts").select("id", count="exact").execute()
        deals_res = supabase.table("crm_deals").select("id", count="exact").execute()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي العقارات والإعلانات", reports_res.count if hasattr(reports_res, 'count') else "غير متوفر")
        col2.metric("إجمالي الزبناء", contacts_res.count if hasattr(contacts_res, 'count') else "غير متوفر")
        col3.metric("إجمالي الصفقات", deals_res.count if hasattr(deals_res, 'count') else "غير متوفر")
    except Exception as e:
        st.info("جاري تهيئة الإحصائيات أو التحقق من اتصال قاعدة البيانات.")

# 2. إدارة العقارات
elif menu == "إدارة العقارات":
    st.title("🏠 إدارة العقارات والإعلانات")
    
    with st.form("new_property"):
        st.subheader="إضافة عقار أو مشروع جديد"
        name = st.text_input("اسم العقار/المشروع")
        price = st.number_input("السعر (درهم)", step=1000.0)
        desc = st.text_area("وصف الإعلان")
        if st.form_submit_button("إضافة العقار"):
            if name:
                supabase.table("reports").insert({
                    "project_name": name, 
                    "price": price, 
                    "report_content": desc
                }).execute()
                st.success("تم إضافة العقار بنجاح!")
            else:
                st.warning("يرجى إدخال اسم العقار.")
                
    st.markdown("---")
    st.subheader("📋 قائمة العقارات المسجلة")
    try:
        response = supabase.table("reports").select("*").execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد عقارات مسجلة حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")

# 3. إدارة CRM
elif menu == "إدارة CRM":
    st.title("👥 إدارة الزبناء وجهات الاتصال")
    
    with st.form("new_contact"):
        st.subheader="إضافة عميل جديد"
        full_name = st.text_input("اسم العميل الكامل")
        phone = st.text_input("رقم الهاتف")
        email = st.text_input("البريد الإلكتروني")
        interest_area = st.text_input("مجال الاهتمام")
        if st.form_submit_button("حفظ العميل"):
            if full_name:
                supabase.table("crm_contacts").insert({
                    "full_name": full_name, 
                    "phone": phone,
                    "email": email,
                    "interest_area": interest_area
                }).execute()
                st.success("تم حفظ العميل بنجاح!")
            else:
                st.warning("يرجى إدخال اسم العميل.")
                
    st.markdown("---")
    st.subheader("📋 قائمة الزبناء المسجلين")
    try:
        response = supabase.table("crm_contacts").select("*").execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد جهات اتصال مسجلة حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")

# 4. الصفقات
elif menu == "متابعة الصفقات":
    st.title("💼 متابعة الصفقات")
    
    with st.form("new_deal"):
        st.subheader="تسجيل صفقة جديدة"
        contact_id = st.number_input("معرف العميل (Contact ID)", min_value=1, step=1)
        report_id = st.text_input("معرف العقار/الإعلان (Report UUID - اختياري)")
        amount = st.number_input("مبلغ الصفقة (درهم)", step=1000.0)
        deal_stage = st.selectbox("مرحلة الصفقة", ["في طور المتابعة", "تم إرسال العرض", "تم إغلاق الصفقة بنجاح", "ملغاة"])
        
        if st.form_submit_button("إنشاء وتسجيل الصفقة"):
            try:
                deal_data = {
                    "contact_id": int(contact_id),
                    "amount": amount,
                    "deal_stage": deal_stage
                }
                if report_id.strip():
                    deal_data["report_id"] = report_id.strip()
                    
                supabase.table("crm_deals").insert(deal_data).execute()
                st.success("تم إنشاء الصفقة بنجاح!")
            except Exception as e:
                st.error(f"فشل تسجيل الصفقة (تأكد من صحة معرف العميل/العقار وأنها تتبع لحسابك): {e}")
                
    st.markdown("---")
    st.subheader("📋 قائمة الصفقات الجارية")
    try:
        response = supabase.table("crm_deals").select("*").execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد صفقات مسجلة حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")
