import streamlit as __st
from supabase import create_client, Client

# إعداد الصفحة وتكوينها
__st.set_page_config(
    page_title="OMEGA OS - نظام الإدارة والخدمات",
    page_icon="⚡",
    layout="wide"
)

# بيانات الاتصال بقاعدة بيانات Supabase (يُفضل لاحقاً نقلها لـ st.secrets)
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"

@__st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_supabase()
except Exception as e:
    __st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")

# تصميم الواجهة الجانبية (القائمة الرئيسية)
__st.sidebar.title("⚡ OMEGA OS")
__st.sidebar.markdown("---")
menu_option = __st.sidebar.radio(
    "اختر القسم:",
    ["لوحة القيادة (Dashboard)", "إدارة الإعلانات والعقارات", "إدارة الزبناء (CRM)", "متابعة الصفقات"]
)

__st.sidebar.markdown("---")
__st.sidebar.info("نظام سيادي مخصص لإدارة الأعمال والعقارات والخدمات الرقمية.")

# 1. لوحة القيادة (Dashboard)
if menu_option == "لوحة القيادة (Dashboard)":
    __st.title("📊 لوحة القيادة العامة")
    __st.markdown("مرحباً بك في نظامك السيادي لإدارة العمليات.")
    
    col1, col2, col3 = __st.columns(3)
    with col1:
        __st.metric(label="إجمالي العقارات/الإعلانات", value="--")
    with col2:
        __st.metric(label="إجمالي الزبناء (CRM)", value="--")
    with col3:
        __st.metric(label="الصفقات الجارية", value="--")

# 2. إدارة الإعلانات والعقارات
elif menu_option == "إدارة الإعلانات والعقارات":
    __st.title("🏠 إدارة الإعلانات والعقارات والخدمات (Reports)")
    
    with __st.form("add_report_form"):
        __st.subheader="إضافة عقار أو إعلان جديد"
        project_name = __st.text_input("اسم المشروع / العقار / الخدمة")
        report_type = __st.selectbox("نوع الإعلان", ["عقار سكني", "أرض تجارية", "خدمة رقمية", "أخرى"])
        report_content = __st.text_area("وصف تفصيلي")
        price = __st.number_input("السعر (درهم)", min_value=0.0, step=1000.0)
        status = __st.selectbox("الحالة", ["متاح", "محجوز", "مباع"])
        
        submitted = __st.form_submit_button("حفظ وإضافة")
        if submitted:
            if project_name:
                try:
                    data = {
                        "project_name": project_name,
                        "report_type": report_type,
                        "report_content": report_content,
                        "price": price,
                        "status": status
                    }
                    response = supabase.table("reports").insert(data).execute()
                    __st.success("تم إضافة الإعلان/العقار بنجاح!")
                except Exception as e:
                    __st.error(f"حدث خطأ أثناء الإضافة: {e}")
            else:
                __st.warning("يرجى إدخال اسم المشروع على الأقل.")

# 3. إدارة الزبناء (CRM Contacts)
elif menu_option == "إدارة الزبناء (CRM)":
    __st.title("👥 إدارة جهات الاتصال والزبناء (CRM Contacts)")
    
    with __st.form("add_contact_form"):
        __st.subheader("إضافة عميل جديد")
        full_name = __st.text_input("الاسم الكامل")
        phone = __st.text_input("رقم الهاتف")
        email = __st.text_input("البريد الإلكتروني")
        interest_area = __st.text_input("مجال الاهتمام")
        deal_stage = __st.selectbox("مرحلة الاهتمام", ["مهتم", "مهتم جداً", "في طور التفاوض", "عميل سابق"])
        notes = __st.text_area("ملاحظات إضافية")
        
        submitted_contact = __st.form_submit_button("حفظ بيانات العميل")
        if submitted_contact:
            if full_name:
                try:
                    data = {
                        "full_name": full_name,
                        "phone": phone,
                        "email": email,
                        "interest_area": interest_area,
                        "deal_stage": deal_stage,
                        "notes": notes
                    }
                    response = supabase.table("crm_contacts").insert(data).execute()
                    __st.success("تم حفظ بيانات العميل بنجاح!")
                except Exception as e:
                    __st.error(f"حدث خطأ أثناء الحفظ: {e}")
            else:
                __st.warning("يرجى إدخال اسم العميل على الأقل.")

# 4. متابعة الصفقات
elif menu_option == "متابعة الصفقات":
    __st.title("💼 متابعة الصفقات (CRM Deals)")
    __st.info("من هنا يمكنك ربط الزبناء بالعقارات وإدارة الصفقات مع تفعيل قيود الحماية الأمنية تلقائياً.")
    
    with __st.form("add_deal_form"):
        contact_id = __st.number_input("معرف العميل (Contact ID)", min_value=1, step=1)
        report_id = __st.text_input("معرف العقار/الإعلان (Report UUID - اختياري)")
        deal_stage = __st.selectbox("مرحلة الصفقة", ["في طور المتابعة", "تم إرسال العرض", "تم إغلاق الصفقة بنجاح", "ملغاة"])
        amount = __st.number_input("مبلغ الصفقة (درهم)", min_value=0.0, step=1000.0)
        
        submitted_deal = __st.form_submit_button("تسجيل الصفقة")
        if submitted_deal:
            try:
                deal_data = {
                    "contact_id": int(contact_id),
                    "deal_stage": deal_stage,
                    "amount": amount
                }
                if report_id.strip():
                    deal_data["report_id"] = report_id.strip()
                
                response = supabase.table("crm_deals").insert(deal_data).execute()
                __st.success("تم تسجيل الصفقة بنجاح مع مطابقة الشروط الأمنية!")
            except Exception as e:
                __st.error(f"فشل تسجيل الصفقة (تأكد من صحة المعرفات وأنها تتبع لحسابك): {e}")
