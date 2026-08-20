import streamlit as st
from supabase import create_client, Client
import urllib.parse
from datetime import datetime

# إعدادات النظام السيادي المتقدم
st.set_page_config(page_title="OMEGA OS - V2.2 Integrated", layout="wide")

# إعداد Supabase
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("👑 OMEGA OS - Sovereign Edition V2.2")

# دالة رابط الواتساب المباشر
def get_whatsapp_link(phone_number, message):
    encoded_msg = urllib.parse.quote(message)
    clean_number = "212" + phone_number.lstrip('0')
    return f"https://wa.me/{clean_number}?text={encoded_msg}"

# القائمة الجانبية السيادية
menu = st.sidebar.selectbox("الوحدة السيادية", [
    "رصد الميدان", 
    "مصنع الإعلانات العقارية 📢", 
    "مصنع الخدمات الرقمية 💻",
    "CRM العملاء المهتمين",
    "الأرشيف والتقارير"
])

# ==========================================
# الوحدة 1: رصد الميدان
# ==========================================
if menu == "رصد الميدان":
    st.header("📊 سجل بيانات الميدان")
    p_name = st.text_input("اسم المشروع/الورش")
    p_content = st.text_area("محتوى التقرير أو التحديث")
    
    if st.button("حفظ في السحابة السيادية"):
        if p_name and p_content:
            supabase.table("reports").insert({
                "project_name": p_name, 
                "report_content": p_content, 
                "report_type": "ورش",
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("تم حفظ تقرير الميدان بنجاح!")
        else:
            st.warning("المرجو ملء اسم المشروع ومحتوى التقرير.")

# ==========================================
# الوحدة 2: مصنع الإعلانات العقارية (مع الحاسبة والـ CRM)
# ==========================================
elif menu == "مصنع الإعلانات العقارية 📢":
    st.header("📢 مصنع صياغة الإعلانات (عقار/معدات)")
    cat_list = ["عقار فلاحي", "عقار تجاري", "عقار صناعي", "عقار سكني", "عقار مهني وخدماتي", "عقار استثماري", "معدات واليات"]
    p_type = st.selectbox("نوع العقار:", cat_list)
    loc = st.text_input("الموقع:")
    price = st.text_input("السعر (مثلاً: 500000 أو 500000 درهم):")
    
    # حاسبة العمولة الفورية المطورة
    if price:
        try:
            price_num = float(''.join(filter(str.isdigit, price)))
            commission = price_num * 0.03
            st.metric(label="💰 عمولة الوساطة 3%", value=f"{commission:,.2f} درهم")
            st.metric(label="💵 الثمن النهائي الإجمالي", value=f"{price_num + commission:,.2f} درهم")
        except:
            pass

    features = st.text_area("المميزات:")
    
    if st.button("توليد + أرشفة + نشر 🚀"):
        ad_text = f"""👑 إعلان حصري - {p_type} 👑

فرصة استثنائية وعرض متميز في {loc}.
🔹 التصنيف: {p_type}
🔹 الموقع: {loc}
🔹 السعر المقترح: {price}

المميزات والخصائص:
{features}

للمعاينة والاستفسار المباشر، تواصل معنا:
📞 0691897126
Studio Tassaout & Sraghna Media"""

        st.code(ad_text, language="text")
        
        wa_link = get_whatsapp_link("0691897126", ad_text)
        st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
        
        supabase.table("reports").insert({
            "project_name": p_type, 
            "report_content": ad_text, 
            "report_type": "إعلان عقاري",
            "created_at": datetime.now().isoformat()
        }).execute()
        st.success("تم التوليد والأرشفة والنشر بنجاح!")

    # قسم تسجيل مهتم بهذا الإعلان مباشرة
    with st.expander("📞 تسجيل عميل مهتم بهذا العقار"):
        c_name = st.text_input("اسم المهتم")
        c_phone = st.text_input("هاتف المهتم")
        if st.button("حفظ العميل في CRM"):
            if c_name and c_phone:
                supabase.table("clients").insert({
                    "name": c_name, 
                    "phone": c_phone, 
                    "interest": f"{p_type} - {loc}",
                    "created_at": datetime.now().isoformat()
                }).execute()
                st.success(f"تم حفظ العميل {c_name} بنجاح!")
            else:
                st.warning("المرجو إدخال الاسم والهاتف.")

# ==========================================
# الوحدة 3: مصنع الخدمات الرقمية
# ==========================================
elif menu == "مصنع الخدمات الرقمية 💻":
    st.header("💻 مصنع إعلانات الخدمات الرقمية")
    dig_services = ["تصميم هوية بصرية", "إدارة حملات إعلانية", "إدارة منصات التواصل", "برمجة وأتمتة"]
    selected_service = st.selectbox("نوع الخدمة:", dig_services)
    target = st.text_input("الجمهور المستهدف (مثلاً: أصحاب الشركات، المحلات):")
    details = st.text_area("تفاصيل الباقة أو العرض:")
    
    if st.button("توليد + أرشفة + نشر 🚀"):
        digital_ad = f"""🚀 عرض احترافي: {selected_service} 🚀

هل ترغب في تطوير نشاطك والوصول إلى {target} باحترافية؟
نقدم لك حلولاً رقمية مبتكرة ومتكاملة لرفع مبيعاتك.

تفاصيل الباقة:
{details}

💡 اجعل مشروعك يبرز في السوق الرقمي اليوم!
📞 تواصل معنا الآن: 0691897126
DANA Digital Market & Sraghna Media"""

        st.code(digital_ad, language="text")
        
        wa_link = get_whatsapp_link("0691897126", digital_ad)
        st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
        
        supabase.table("reports").insert({
            "project_name": selected_service, 
            "report_content": digital_ad, 
            "report_type": "إعلان رقمي",
            "created_at": datetime.now().isoformat()
        }).execute()
        st.success("تم التوليد والأرشفة والنشر بنجاح!")

    # قسم تسجيل مهتم بخدمات رقمية
    with st.expander("📞 تسجيل عميل مهتم بهذه الخدمة"):
        c_name_dig = st.text_input("اسم الزبون المهتم")
        c_phone_dig = st.text_input("هاتف الزبون المهتم")
        if st.button("حفظ الزبون الرقمي"):
            if c_name_dig and c_phone_dig:
                supabase.table("clients").insert({
                    "name": c_name_dig, 
                    "phone": c_phone_dig, 
                    "interest": selected_service,
                    "created_at": datetime.now().isoformat()
                }).execute()
                st.success(f"تم حفظ الزبون {c_name_dig} بنجاح!")
            else:
                st.warning("المرجو إدخال الاسم والهاتف.")

# ==========================================
# الوحدة 4: CRM العملاء
# ==========================================
elif menu == "CRM العملاء المهتمين":
    st.header("👤 سجل إدارة علاقات العملاء (CRM)")
    try:
        clients_data = supabase.table("clients").select("*").order("created_at", desc=True).execute().data
        if clients_data:
            st.table(clients_data)
        else:
            st.info("لا توجد بيانات مسجلة في جدول العملاء حالياً.")
    except Exception as e:
        st.error(f"تأكد من إنشاء جدول 'clients' في Supabase بالأعمدة المناسبة (id, name, phone, interest, created_at). الخطأ: {e}")

# ==========================================
# الوحدة 5: الأرشيف
# ==========================================
elif menu == "الأرشيف والتقارير":
    st.header("📁 الأرشيف السيادي")
    data = supabase.table("reports").select("*").order("created_at", desc=True).execute().data
    if data:
        for r in data:
            with st.expander(f"📌 {r.get('report_type')} - {r.get('project_name')} - {str(r.get('created_at'))[:10]}"):
                st.code(r.get('report_content'), language="text")
                wa_link = get_whatsapp_link("0691897126", r.get('report_content'))
                st.link_button("📲 إعادة النشر عبر واتساب", wa_link)
    else:
        st.info("لا توجد تقارير مسجلة في الأرشيف حالياً.")
