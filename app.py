import streamlit as st
from supabase import create_client, Client
import urllib.parse
from datetime import datetime
import plotly.express as px
import pandas as pd

# إعدادات النظام السيادي
st.set_page_config(page_title="OMEGA OS - Sovereign Edition", layout="wide")

# إعداد Supabase
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("👑 Ameur Signature | النظام السيادي المتكامل")

# دالة رابط الواتساب المباشر
def get_whatsapp_link(phone_number, message):
    encoded_msg = urllib.parse.quote(message)
    clean_number = "212" + phone_number.lstrip('0')
    return f"https://wa.me/{clean_number}?text={encoded_msg}"

# القائمة السيادية الكاملة
menu = st.sidebar.selectbox("الوحدة السيادية", [
    "📊 لوحة تحكم التحليلات",
    "رصد الميدان", 
    "مصنع الإعلانات العقارية 📢", 
    "مصنع الخدمات الرقمية 💻",
    "📑 تدبير الصفقات العمومية",
    "🧠 الوكيل التقني الخبير",
    "🤖 الوكيل الذكي (AI Deal Closer)",
    "CRM العملاء المهتمين",
    "الأرشيف والتقارير"
])

# ==========================================
# 1. لوحة تحكم التحليلات
# ==========================================
if menu == "📊 لوحة تحكم التحليلات":
    st.header("📊 لوحة الأداء والتحليلات السيادية")
    try:
        data = supabase.table("reports").select("*").execute().data
        if data:
            df = pd.DataFrame(data)
            df['created_at'] = pd.to_datetime(df['created_at'])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي العمليات", len(df))
            col2.metric("أنواع الأنشطة", df['report_type'].nunique())
            col3.metric("العملاء المسجلين", len(supabase.table("clients").select("*").execute().data))
            
            st.subheader("توزيع الأنشطة والصفقات")
            fig_pie = px.pie(df, names='report_type', title="توزيع العمليات حسب النوع")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.subheader("وتيرة النشاط الميداني اليومي")
            df['date_only'] = df['created_at'].dt.date
            df_trend = df.groupby('date_only').size().reset_index(name='count')
            
            fig_line = px.line(
                df_trend, 
                x='date_only', 
                y='count', 
                title="عدد العمليات اليومية",
                markers=True,
                labels={'date_only': 'التاريخ', 'count': 'عدد العمليات'}
            )
            fig_line.update_layout(yaxis=dict(tickformat='d'))
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية للتحليل حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب بيانات التحليلات: {e}")

# ==========================================
# 2. رصد الميدان
# ==========================================
elif menu == "رصد الميدان":
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
# 3. مصنع الإعلانات العقارية (مع واتساب مباشر)
# ==========================================
elif menu == "مصنع الإعلانات العقارية 📢":
    st.header("📢 مصنع صياغة الإعلانات العقارية")
    cat_list = ["عقار فلاحي", "عقار تجاري", "عقار صناعي", "عقار سكني", "عقار مهني وخدماتي", "عقار استثماري", "معدات واليات"]
    p_type = st.selectbox("نوع العقار:", cat_list)
    loc = st.text_input("الموقع:")
    price = st.text_input("السعر (مثلاً: 500000 درهم):")
    
    if price:
        try:
            price_num = float(''.join(filter(str.isdigit, price)))
            commission = price_num * 0.03
            st.metric(label="💰 عمولة الوساطة 3%", value=f"{commission:,.2f} درهم")
            st.metric(label="💵 الثمن النهائي الإجمالي", value=f"{price_num + commission:,.2f} درهم")
        except:
            pass

    features = st.text_area("المميزات:")
    phone_input = st.text_input("رقم الهاتف للإرسال عبر واتساب:", value="0691897126")
    
    if st.button("توليد + أرشفة + تجهيز واتساب 🚀"):
        ad_text = f"""👑 إعلان حصري - {p_type} 👑

فرصة استثنائية وعرض متميز في {loc}.
🔹 التصنيف: {p_type}
🔹 الموقع: {loc}
🔹 السعر المقترح: {price}

المميزات والخصائص:
{features}

للمعاينة والاستفسار المباشر، تواصل معنا:
📞 {phone_input}
Ameur Signature & Sraghna Media"""

        st.code(ad_text, language="text")
        wa_link = get_whatsapp_link(phone_input, ad_text)
        st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
        
        supabase.table("reports").insert({
            "project_name": p_type, 
            "report_content": ad_text, 
            "report_type": "إعلان عقاري",
            "created_at": datetime.now().isoformat()
        }).execute()
        st.success("تم التوليد والأرشفة بنجاح!")

# ==========================================
# 4. مصنع الخدمات الرقمية
# ==========================================
elif menu == "مصنع الخدمات الرقمية 💻":
    st.header("💻 مصنع إعلانات الخدمات الرقمية")
    dig_services = ["تصميم هوية بصرية", "إدارة حملات إعلانية", "إدارة منصات التواصل", "برمجة وأتمتة"]
    selected_service = st.selectbox("نوع الخدمة:", dig_services)
    target = st.text_input("الجمهور المستهدف:")
    details = st.text_area("تفاصيل الباقة أو العرض:")
    phone_input = st.text_input("رقم الهاتف للإرسال عبر واتساب:", value="0691897126")
    
    if st.button("توليد + أرشفة + تجهيز واتساب 🚀"):
        digital_ad = f"""🚀 عرض احترافي: {selected_service} 🚀

هل ترغب في تطوير نشاطك والوصول إلى {target} باحترافية؟
نقدم لك حلولاً رقمية مبتكرة ومتكاملة.

تفاصيل الباقة:
{details}

💡 اجعل مشروعك يبرز في السوق الرقمي اليوم!
📞 تواصل معنا الآن: {phone_input}
DANA Digital Market & Sraghna Media"""

        st.code(digital_ad, language="text")
        wa_link = get_whatsapp_link(phone_input, digital_ad)
        st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
        
        supabase.table("reports").insert({
            "project_name": selected_service, 
            "report_content": digital_ad, 
            "report_type": "إعلان رقمي",
            "created_at": datetime.now().isoformat()
        }).execute()
        st.success("تم التوليد والأرشفة بنجاح!")

# ==========================================
# 5. تدبير الصفقات العمومية
# ==========================================
elif menu == "📑 تدبير الصفقات العمومية":
    st.header("📑 وحدة تدبير الصفقات العمومية والمناقصات")
    tender_title = st.text_input("موضوع الصفقة أو رقم طلب الأثمان:")
    admin_entity = st.text_input("الإدارة صاحبة المشروع:")
    estimated_budget = st.text_input("الميزانية التقديرية (درهم):")
    tender_status = st.selectbox("حالة الصفقة:", ["في طور دراسة الملف", "تم إيداع الملف", "تم الفوز بالصفقة 🏆", "لم يتم التوفيق"])
    tender_notes = st.text_area("ملاحظات وتفاصيل إضافية:")
    
    if st.button("حفظ وتتبع الصفقة في السحابة 📂"):
        if tender_title and admin_entity:
            supabase.table("reports").insert({
                "project_name": tender_title,
                "report_content": f"إدارة: {admin_entity}\nالميزانية: {estimated_budget}\nالحالة: {tender_status}\nملاحظات: {tender_notes}",
                "report_type": "صفقة عمومية",
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("تم تسجيل وتتبع الصفقة العمومية بنجاح!")

# ==========================================
# 6. الوكيل التقني والخبير
# ==========================================
elif menu == "🧠 الوكيل التقني الخبير":
    st.header("🧠 المستشار التقني وخبير الأنظمة الرقمية")
    tech_challenge = st.text_area("اطرح المشكل التقني أو المشروع:")
    if st.button("توليد الحل الهندسي 🛠️"):
        if tech_challenge:
            st.info(f"⚙️ **التوجيه الهندسي:** بناءً على معطياتك حول ({tech_challenge})، اعتمد على هيكلة دقيقة وفصل الوحدات البرمجية لضمان استقرار الأنظمة التشغيلية لـ Ameur Signature.")
        else:
            st.warning("المرجو طرح المشكل أو المشروع أولاً.")

# ==========================================
# 7. الوكيل الذكي (AI Deal Closer)
# ==========================================
elif menu == "🤖 الوكيل الذكي (AI Deal Closer)":
    st.header("🤖 مستشار إغلاق الصفقات الذكي")
    client_objection = st.text_area("اعتراض أو رسالة الزبون:")
    if st.button("توليد استراتيجية الرد 💡"):
        if client_objection:
            st.info("💡 **الرد المقترح:** نضمن لك أعلى معايير الجودة والقيمة المضافة لضمان نجاح استثمارك وقوة مشروعك.")

# ==========================================
# 8. CRM العملاء
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
        st.error(f"خطأ: {e}")

# ==========================================
# 9. الأرشيف والتقارير
# ==========================================
elif menu == "الأرشيف والتقارير":
    st.header("📁 الأرشيف السيادي الشامل")
    try:
        data = supabase.table("reports").select("*").order("created_at", desc=True).execute().data
        if data:
            for r in data:
                with st.expander(f"📌 [{r.get('report_type')}] - {r.get('project_name')}"):
                    st.code(r.get('report_content'), language="text")
                    wa_link = get_whatsapp_link("0691897126", r.get('report_content'))
                    st.link_button("📲 إعادة النشر عبر واتساب", wa_link)
        else:
            st.info("الأرشيف فارغ حالياً.")
    except Exception as e:
        st.error(f"خطأ: {e}")
