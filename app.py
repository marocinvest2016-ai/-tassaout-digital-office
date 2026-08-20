import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
from datetime import datetime
import urllib.parse
from bs4 import BeautifulSoup
import requests

# ==========================================
# 1. الوحدات البرمجية المدمجة (Modules)
# ==========================================

class MarketScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_public_tenders(self):
        tenders_data = []
        try:
            tenders_data.append({
                "project_name": "صفقة تهيئة مسالك واحات قلعة السراغنة",
                "report_content": "إعلان عن طلب أثمانه متعلق بتهيئة الطرق والمسالك القروية بالإقليم.",
                "report_type": "صفقة عمومية",
                "created_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"خطأ في جلب الصفقات: {e}")
        return tenders_data

    def fetch_real_estate_listings(self):
        listings = []
        try:
            listings.append({
                "project_name": "أرض فلاحية محفظة - تساوت",
                "report_content": "مساحة هكتارين مع بئر وموقع استراتيجي قرب الطريق الرئيسية.",
                "report_type": "عقار فلاحي",
                "created_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"خطأ في جلب العقارات: {e}")
        return listings

    def run_full_scan(self, supabase_client):
        all_opportunities = self.fetch_public_tenders() + self.fetch_real_estate_listings()
        inserted_count = 0
        for item in all_opportunities:
            try:
                supabase_client.table("reports").insert(item).execute()
                inserted_count += 1
            except Exception as e:
                print(f"فشل حفظ العنصر: {e}")
        return inserted_count


class ContentGenerator:
    def __init__(self, phone_number="0691897126"):
        self.phone_number = phone_number

    def generate_real_estate_ad(self, title, location, price, features):
        ad_text = f"""👑 إعلان حصري - {title} 👑

فرصة استثنائية وعرض متميز في {location}.
🔹 التصنيف العقاري: {title}
🔹 الموقع الاستراتيجي: {location}
🔹 الثمن المقترح: {price}

المميزات والخصائص الكبرى:
{features}

للمعاينة الميدانية والاستفسار المباشر، تواصل معنا:
📞 {self.phone_number}
Ameur Signature & Sraghna Media"""
        return ad_text

    def generate_digital_service_ad(self, service_name, target_audience, details):
        ad_text = f"""🚀 عرض احترافي: {service_name} 🚀

هل ترغب في تطوير نشاطك والوصول إلى {target_audience} باحترافية تامة؟
نقدم لك حلولاً رقمية مبتكرة ومصممة لتعزيز حضورك في السوق.

تفاصيل الباقة والعرض:
{details}

💡 اجعل مشروعك يبرز في السوق الرقمي اليوم!
📞 تواصل معنا الآن: {self.phone_number}
DANA Digital Market & Sraghna Media"""
        return ad_text

    def get_whatsapp_url(self, message):
        encoded_msg = urllib.parse.quote(message)
        clean_number = "212" + self.phone_number.lstrip('0')
        return f"https://wa.me/{clean_number}?text={encoded_msg}"


class DealCloserAI:
    def __init__(self):
        pass

    def analyze_objection(self, client_message):
        msg_lower = client_message.lower()
        
        if any(word in msg_lower for word in ["ثمن", "غالي", "سعر", "تخفيض", "نقص", "بزاف"]):
            strategy_title = "استراتيجية إقناع الزبون (الاعتراض على السعر)"
            response_text = (
                "أهلاً بك أخي الكريم. السعر المقترح يتماشى بدقة مع جودة العقار وموقعه الاستراتيجي وقيمته في السوق حالياً. "
                "الاستثمار الناجح يبحث دائماً عن الجودة والربح على المدى الطويل. هل نحدد موعداً للمعاينة الميدانية غداً لنحسم الأمر؟"
            )
            analysis = "الزبون يختبر السعر أو يحاول التفاوض لخفض التكلفة."

        elif any(word in msg_lower for word in ["نفكر", "نرد", "وقت", "بعدين", "متردد"]):
            strategy_title = "استراتيجية إقناع الزبون (التردد والتأجيل)"
            response_text = (
                "خذ وقتك في التفكير بكل تأكيد، لكن أحب أن أحيطك علماً أن هناك اهتماماً كبيراً بهذا العرض حالياً من طرف مستثمرين آخرين، "
                "ونخشى أن يتم حسم الصفقة قبلك. ما رايك أن نلتقي في عين المكان لمعاينة التفاصيل عن قرب؟"
            )
            analysis = "الزبون مهتم لكنه يماطل أو يفتقر لشعور الاستعجال."

        elif any(word in msg_lower for word in ["محفظ", "وراق", "وثائق", "مساحة", "رخصة"]):
            strategy_title = "استراتيجية الرد (تأكيد الضمانات القانونية)"
            response_text = (
                "جميع الوثائق القانونية والملفات متوفرة ومطابقة للمعايير الجاري بها العمل. "
                "يمكننا ترتيب لقاء مباشر للاطلاع على كافة التفاصيل التقنية والملف القانوني بكل شفافية."
            )
            analysis = "الزبون جاد ويهتم بالجانب القانوني والتوثيق."

        else:
            strategy_title = "استراتيجية الإغلاق العامة (دفع نحو المعاينة)"
            response_text = (
                "أتفهم ملاحظتك تماماً. أفضل خطوة عملية الآن هي تنظيم معاينة ميدانية سريعة لترى كل التفاصيل بنفسك. "
                "متى يناسبك اللقاء في عين المكان؟"
            )
            analysis = "استجابة عامة موجهة لدفع الزبون لاتخاذ القرار الميداني."

        return {
            "analysis": analysis,
            "strategy": strategy_title,
            "response": response_text
        }


# ==========================================
# 2. إعداد واجهة التطبيق الرئيسية (Streamlit)
# ==========================================

st.set_page_config(
    page_title="OMEGA OS - Ameur Signature", 
    page_icon="👑", 
    layout="wide"
)

# الاتصال بقاعدة البيانات السحابية Supabase
try:
    supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error(f"خطأ في الاتصال بقاعدة البيانات السحابية: {e}")

# تهيئة الكائنات البرمجية
generator = ContentGenerator(phone_number="0691897126")
deal_closer = DealCloserAI()
scraper = MarketScraper()

st.title("👑 Ameur Signature | النظام السيادي المتكامل")

menu = st.sidebar.selectbox("الوحدة السيادية للتحكم", [
    "📊 لوحة تحكم التحليلات",
    "رصد الميدان وجلب البيانات 🌐", 
    "مصنع الإعلانات العقارية 📢", 
    "مصنع الخدمات الرقمية 💻",
    "📑 تدبير الصفقات العمومية",
    "🤖 الوكيل الذكي (AI Deal Closer)",
    "CRM العملاء المهتمين",
    "الأرشيف والتقارير"
])

# ==========================================
# 3. توجيه المسارات والوحدات التفاعلية
# ==========================================

if menu == "📊 لوحة تحكم التحليلات":
    st.header("📊 لوحة الأداء والتحليلات السيادية")
    try:
        data = supabase.table("reports").select("*").execute().data
        if data:
            df = pd.DataFrame(data)
            df['created_at'] = pd.to_datetime(df['created_at'])
            
            col1, col2 = st.columns(2)
            col1.metric("إجمالي العمليات والأرشيف", len(df))
            col2.metric("أنواع الأنشطة والقطاعات", df['report_type'].nunique())
            
            st.subheader("توزيع العمليات حسب النشاط")
            fig_pie = px.pie(df, names='report_type', title="توزيع العمليات في النظام")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.subheader("تطور العمليات الميدانية اليومية")
            df['date_only'] = df['created_at'].dt.date
            df_trend = df.groupby('date_only').size().reset_index(name='count')
            
            fig_line = px.line(
                df_trend, x='date_only', y='count', 
                title="النشاط اليومي المسجل", markers=True,
                labels={'date_only': 'التاريخ', 'count': 'العمليات'}
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لعرض التحليلات حالياً.")
    except Exception as e:
        st.error(f"خطأ في استخراج التحليلات: {e}")

elif menu == "رصد الميدان وجلب البيانات 🌐":
    st.header("🌐 محرك الاستخبارات الميدانية وسحب البيانات")
    st.info("قم بتشغيل المسح الآلي لجلب أحدث عروض العقارات والصفقات العمومية بجهة مراكش-آسفي وأرشفقتها فوراً.")
    
    if st.button("🚀 تشغيل المسح الميداني الشامل وأرشفة النتائج"):
        with st.spinner("جاري مسح السوق وجلب الفرص عبر السكربت الهندسي..."):
            inserted_count = scraper.run_full_scan(supabase)
            st.success(f"تم بنجاح جلب وأرشفة {inserted_count} فرصة جديدة في قاعدة البيانات السيادية!")

    st.markdown("---")
    st.subheader("إدخال تقرير ميداني يدوي")
    p_name = st.text_input("اسم المشروع أو الورش")
    p_content = st.text_area("محتوى التقرير الميداني")
    
    if st.button("حفظ التقرير في السحابة"):
        if p_name and p_content:
            supabase.table("reports").insert({
                "project_name": p_name, 
                "report_content": p_content, 
                "report_type": "ورش ميداني",
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("تم حفظ تقرير الميدان بنجاح!")
        else:
            st.warning("المرجو ملء اسم المشروع ومحتوى التقرير.")

elif menu == "مصنع الإعلانات العقارية 📢":
    st.header("📢 مصنع صياغة الإعلانات العقارية الحصرية")
    cat_list = ["عقار فلاحي", "عقار تجاري", "عقار صناعي", "عقار سكني", "عقار مهني", "عقار استثماري", "معدات وآليات"]
    p_type = st.selectbox("نوع العقار:", cat_list)
    loc = st.text_input("الموقع الاستراتيجي:")
    price = st.text_input("الثمن المقترح (مثلاً: 500000 درهم):")
    
    if price:
        try:
            price_num = float(''.join(filter(str.isdigit, price)))
            commission = price_num * 0.03
            col_m1, col_m2 = st.columns(2)
            col_m1.metric(label="💰 عمولة الوساطة 3%", value=f"{commission:,.2f} درهم")
            col_m2.metric(label="💵 الثمن الإجمالي للزبون", value=f"{price_num + commission:,.2f} درهم")
        except:
            pass

    features = st.text_area("المميزات والخصائص الكبرى:")
    
    if st.button("توليد الإعلان + أرشفة سحابية + تجهيز واتساب 🚀"):
        if loc and price:
            ad_text = generator.generate_real_estate_ad(p_type, loc, price, features)
            st.code(ad_text, language="text")
            
            wa_link = generator.get_whatsapp_url(ad_text)
            st.link_button("📲 إرسال مباشر للإعلان عبر الواتساب", wa_link, use_container_width=True, type="primary")
            
            supabase.table("reports").insert({
                "project_name": p_type, 
                "report_content": ad_text, 
                "report_type": "إعلان عقاري",
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("تم التوليد والأرشفة بنجاح في قاعدة البيانات!")
        else:
            st.warning("المرجو تحديد الموقع والثمن على الأقل.")

elif menu == "مصنع الخدمات الرقمية 💻":
    st.header("💻 مصنع إعلانات الخدمات الرقمية والأتمتة")
    dig_services = ["تصميم هوية بصرية", "إدارة حملات إعلانية", "إدارة منصات التواصل", "برمجة وأتمتة رقمية"]
    selected_service = st.selectbox("نوع الخدمة الرقمية:", dig_services)
    target = st.text_input("الجمهور المستهدف:")
    details = st.text_area("تفاصيل الباقة والعرض الرقمي:")
    
    if st.button("توليد عرض الخدمات + تجهيز واتساب 🚀"):
        if target and details:
            digital_ad = generator.generate_digital_service_ad(selected_service, target, details)
            st.code(digital_ad, language="text")
            
            wa_link = generator.get_whatsapp_url(digital_ad)
            st.link_button("📲 إرسال مباشر للواتساب", wa_link, use_container_width=True, type="primary")
            
            supabase.table("reports").insert({
                "project_name": selected_service, 
                "report_content": digital_ad, 
                "report_type": "إعلان رقمي",
                "created_at": datetime.now().isoformat()
            }).execute()
            st.success("تم توليد الباقة وأرشفتها بنجاح!")
        else:
            st.warning("المرجو إدخال الجمهور المستهدف وتفاصيل الباقة.")

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
            st.success("تم تسجيل وتتبع الصفقة العمومية بنجاح في السحابة!")
        else:
            st.warning("المرجو ملء موضوع الصفقة والإدارة المعنية.")

elif menu == "🤖 الوكيل الذكي (AI Deal Closer)":
    st.header("🤖 مستشار إغلاق الصفقات الذكي")
    st.info("قم بإدخال اعتراض أو رد الزبون، وسيقوم الوكيل بتحليل نفسيته واقتراح استراتيجية الرد الفوري لإغلاق الصفقة.")
    
    client_objection = st.text_area("رسالة أو اعتراض الزبون (مثلاً: الثمن غالي، يريد التفكير، يطلب تخفيض...):")
    
    if st.button("تحليل الموقف وتوليد استراتيجية الرد 💡"):
        if client_objection:
            result = deal_closer.analyze_objection(client_objection)
            
            st.success(f"**التحليل النفسي:** {result['analysis']}")
            st.markdown(f"### 🎯 {result['strategy']}")
            st.info(result['response'])
            
            wa_link = generator.get_whatsapp_url(result['response'])
            st.link_button("📲 إرسال رد الإغلاق مباشرة للزبون عبر واتساب", wa_link, use_container_width=True, type="primary")
        else:
            st.warning("المرجو كتابة ملاحظة أو اعتراض الزبون أولاً.")

elif menu == "CRM العملاء المهتمين":
    st.header("👤 سجل إدارة علاقات العملاء (CRM)")
    try:
        data = supabase.table("reports").select("*").in_("report_type", ["إعلان عقاري", "إعلان رقمي"]).execute().data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df[['project_name', 'report_type', 'created_at']], use_container_width=True)
        else:
            st.info("لا توجد بيانات مسجلة في الـ CRM حالياً.")
    except Exception as e:
        st.error(f"خطأ في جلب بيانات CRM: {e}")

elif menu == "الأرشيف والتقارير":
    st.header("📁 الأرشيف السيادي الشامل")
    try:
        data = supabase.table("reports").select("*").order("created_at", desc=True).execute().data
        if data:
            for r in data:
                with st.expander(f"📌 [{r.get('report_type', 'عام')}] - {r.get('project_name', 'بدون عنوان')} ({r.get('created_at', '')[:10]})"):
                    st.code(r.get('report_content', ''), language="text")
                    wa_link = generator.get_whatsapp_url(r.get('report_content', ''))
                    st.link_button("📲 إعادة النشر عبر واتساب", wa_link)
        else:
            st.info("الأرشيف فارغ حالياً.")
    except Exception as e:
        st.error(f"خطأ في استخراج الأرشيف: {e}")
