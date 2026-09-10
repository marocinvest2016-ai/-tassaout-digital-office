import streamlit as st
import requests
from google_connector import get_google_sheets_data, calculate_roi_from_sheet

# ===== قائمة نماذج Groq محدثة مع fallback تلقائي =====
GROQ_MODELS = [
    "llama-3.1-8b-instant",        # أساسي: سريع ومستقر 100%
    "llama-3.2-11b-vision-preview", # بديل: أقوى شوية
    "llama-3.3-70b-versatile",      # قوي جداً (إذا كان متاح لحسابك)
]

def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق مع نظام Fallback وتتبع النموذج الناجح"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' powered by Meta Llama on Groq. "
        f"Think step by step. Provide professional, highly tailored, actionable strategies. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى, with professional formatting, bullet points, emojis, and tables when needed."
    )

    last_error = None
    for model in GROQ_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.75,
            "max_completion_tokens": 2000
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=90)
            
            # معالجة أخطاء النموذج غير المتاح
            if res.status_code == 404:
                last_error = f"⚠️ النموذج {model} غير موجود (404). جاري تجربة البديل..."
                continue
            elif res.status_code == 400:
                last_error = f"⚠️ النموذج {model} غير صالح (400). جاري تجربة البديل..."
                continue
            elif res.status_code == 429:
                last_error = f"⏳ تجاوزت حد الطلبات (429) على {model}. جاري تجربة البديل..."
                continue
            
            # أي خطأ آخر
            res.raise_for_status()
            
            # تسجيل النموذج الناجح في الجلسة
            st.session_state.last_model_used = model
            st.session_state.last_model_status = "✅ نجح"
            
            return res.json()['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            last_error = f"⏱️ انتهت مهلة الاتصال بالنموذج {model} (90 ثانية). جاري تجربة البديل..."
            continue
        except Exception as e:
            last_error = f"❌ خطأ في الاتصال (النموذج {model}): {type(e).__name__} - {str(e)}"
            continue

    # إذا فشل كل النماذج
    st.session_state.last_model_status = "❌ فشل"
    return f"❌ تعذر الاتصال بجميع النماذج المتاحة.

آخر خطأ: {last_error}"

def send_whatsapp_alert(message):
    """إرسال إشعار مباشر عبر واتساب API"""
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

        if not all([phone_id, access_token, target_number]):
            st.warning("⚠️ إعدادات WhatsApp غير مكتملة في Secrets")
            return

        url = f"https://graph.facebook.com/{version}/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": target_number,
            "type": "text",
            "text": {"body": message[:4096]}
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code != 200:
            st.warning(f"⚠️ فشل إرسال WhatsApp: HTTP {res.status_code}")
    except Exception as e:
        st.warning(f"⚠️ تعذر إرسال إشعار الواتساب: {type(e).__name__} - {str(e)}")

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        prompt = (
            f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}.

"
            f"المطلوب:
"
            f"1. تحليل SWOT مفصّل (نقاط القوة، الضعف، الفرص، التهديدات)
"
            f"2. الميزة التنافسية الأساسية (Unique Value Proposition)
"
            f"3. خطة تنفيذية لمدة 90 يوم (30-60-90) مع معالم رئيسية
"
            f"4. مؤشرات الأداء الرئيسية (KPIs) المقترحة

"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي، نقاط، إيموجيز، وجداول عند الحاجة."
        )
        return call_super_ai(prompt, "Super CEO Agent", self.domain)

    def cto(self, task):
        prompt = (
            f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية، أدوات التشغيل، stack تقني، واستهداف الجمهور الرقمي لـ: {task} في {self.domain}.

"
            f"المطلوب:
"
            f"1. البنية التقنية المقترحة (Tech Stack: Frontend, Backend, Database, APIs)
"
            f"2. أدوات التشغيل والأتمتة (Automation Tools, CI/CD, Monitoring)
"
            f"3. استراتيجية استهداف الجمهور الرقمي (Digital Audience Targeting)
"
            f"4. خطة أمان وحماية البيانات الأساسية

"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي، نقاط، إيموجيز، وجداول عند الحاجة."
        )
        return call_super_ai(prompt, "Super CTO Agent", self.domain)

    def coo(self, task):
        # جلب البيانات المالية إلا كانت متوفرة
        financial_context = ""
        if hasattr(st.session_state, 'financial_data') and st.session_state.financial_data:
            fd = st.session_state.financial_data
            financial_context = (
                f"

[البيانات المالية الحالية من Google Drive]:
"
                f"• إجمالي الإيرادات: {fd['total_revenue']:,.0f} درهم
"
                f"• إجمالي المصاريف: {fd['total_expenses']:,.0f} درهم
"
                f"• الربح الإجمالي: {fd['total_profit']:,.0f} درهم
"
                f"• متوسط ROI: {fd['avg_roi']:.1f}%
"
                f"استعمل هاد البيانات باش تحط KPIs واقعية وقابلة للقياس."
            )
        
        prompt = (
            f"بصفتك COO فائق، ضع خطة تنفيذية، إدارة الموارد، KPI، وجدولة زمنية دقيقة لـ: {task} في {self.domain}.{financial_context}

"
            f"المطلوب:
"
            f"1. هيكل الفريق والموارد البشرية المطلوبة
"
            f"2. الجدولة الزمنية التفصيلية (Gantt-style timeline)
"
            f"3. مؤشرات الأداء الرئيسية (KPIs) لكل مرحلة
"
            f"4. إدارة المخاطر وخطة طوارئ

"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي، نقاط، إيموجيز، وجداول عند الحاجة."
        )
        return call_super_ai(prompt, "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = (
            f"بناءً على هذه الخطة الاستراتيجية:

{plan}

"
            f"اكتب 3 إعلانات تسويقية جذابة باللهجة المغربية والعربية الفصحى، مع:
"
            f"• عنوان قوي (Headline) يلفت الانتباه
"
            f"• نص إعلاني مقنع (Body Copy) يبرز الفوائد والحلول
"
            f"• دعوة واضحة للعمل (CTA) مع رقم الواتساب: {whatsapp_num}
"
            f"• هاشتاقات مناسبة (3-5 هاشتاقات)
"
            f"• أيقونات وإيموجيز لجذب الانتباه

"
            f"الإعلانات تكون مناسبة لـ Facebook, Instagram, WhatsApp Status."
        )
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        
        # إرسال إشعار WhatsApp
        alert_msg = (
            f"👑 OMEGA SUPER AGENTIC v4.5
"
            f"📂 المجال: {self.domain}
"
            f"🤖 النموذج المستخدم: {st.session_state.get('last_model_used', 'غير محدد')}

"
            f"📝 نص الإعلان:
{ad[:1500]}..."
        )
        send_whatsapp_alert(alert_msg)
        
        return ad

    def closer(self, ad):
        prompt = (
            f"قم بتحسين نص هذا الإعلان لزيادة المبيعات والتحويلات:

{ad}

"
            f"أضف العناصر التالية:
"
            f"1. محفزات الاستعجال (FOMO): عرض محدود، وقت محدود، كمية محدودة
"
            f"2. ضمان قوي (Money-back Guarantee أو ضمان الرضا)
"
            f"3. شهادات عملاء (Testimonials) واقعية ومقنعة
"
            f"4. أسئلة شائعة (FAQ) قصيرة تجاوب على اعتراضات الزبون
"
            f"5. دعوة أقوى للعمل (Stronger CTA) مع شعور بالاستعجال

"
            f"حافظ على اللهجة المغربية + العربية الفصحى، والتنسيق الأصلي."
        )
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

    def full_pipeline(self, task):
        """تشغيل الخط الكامل: CEO → CTO → COO → Copywriter → Closer"""
        with st.spinner("🧠 جاري تحليل المهمة..."):
            ceo_plan = self.ceo(task)
        
        with st.spinner("⚙️ جاري وضع الاستراتيجية التقنية..."):
            cto_plan = self.cto(task)
        
        with st.spinner("📋 جاري وضع الخطة التنفيذية..."):
            coo_plan = self.coo(task)
        
        combined_plan = f"=== خطة CEO ===
{ceo_plan}

=== خطة CTO ===
{cto_plan}

=== خطة COO ===
{coo_plan}"
        
        with st.spinner("✍️ جاري كتابة الإعلانات..."):
            ad = self.copywriter(combined_plan)
        
        with st.spinner("🔥 جاري تحسين الإعلان لزيادة المبيعات..."):
            final_ad = self.closer(ad)
        
        return {
            "ceo": ceo_plan,
            "cto": cto_plan,
            "coo": coo_plan,
            "ad_original": ad,
            "ad_final": final_ad,
            "model_used": st.session_state.get('last_model_used', 'غير محدد')
        }


# ===== واجهة Streamlit =====
st.set_page_config(page_title="👑 OMEGA SUPER AGENTIC v4.5", page_icon="🤖", layout="wide")

st.title("👑 OMEGA SUPER AGENTIC v4.5 + Google Drive")
st.markdown("**نظام الذكاء الاصطناعي الفائق متعدد المجالات - Groq + Llama + Google Sheets**")

# ===== تحميل البيانات المالية من Google Drive =====
with st.spinner("📊 جاري تحميل البيانات المالية من Google Drive..."):
    financial_data = get_google_sheets_data()
    
    if financial_data is not None:
        roi_stats = calculate_roi_from_sheet(financial_data)
        if roi_stats:
            st.session_state.financial_data = roi_stats
            st.success(f"✅ تم تحميل البيانات: إيرادات {roi_stats['total_revenue']:,.0f} درهم | ROI متوسط {roi_stats['avg_roi']:.1f}%")
        else:
            st.warning("⚠️ لم يتم العثور على أعمدة مالية (revenue, expenses, budget)")
    else:
        st.info("ℹ️ Google Drive غير مفعّل - النظام سيعمل بدون بيانات مالية خارجية")

# اختيار المجال
domain = st.selectbox(
    "المجال",
    ["العقار - بيع وشراء الكراء", "التسويق الرقمي", "الزيتون وزيت الزيتون", "أخرى"],
    index=0
)

# إدخال المهمة
task = st.text_area(
    "وصف المهمة المطلوبة",
    placeholder="مثلاً: إطلاق منصة عقارية ذكية في قلعة السراغنة...",
    height=150
)

# زر التنفيذ
if st.button("🚀 تنفيذ المهمة الكاملة", type="primary"):
    if not task.strip():
        st.error("⚠️ المرجو إدخال وصف المهمة")
    else:
        # إنشاء الوكيل
        agent = SuperOmegaAgent(domain)
        
        # تشغيل الخط الكامل
        with st.spinner("جاري المعالجة..."):
            result = agent.full_pipeline(task)
        
        # عرض النتائج
        st.success("✅ تم إنجاز المهمة بنجاح!")
        
        # عرض النموذج المستخدم
        if "last_model_used" in st.session_state:
            st.info(f"🤖 النموذج المستخدم: {st.session_state.last_model_used}")
        
        # عرض الإعلانات
        st.subheader("📢 الإعلان الأصلي (Copywriter)")
        st.markdown(result["ad_original"])
        
        st.subheader("🔥 الإعلان المحسّن (Closer)")
        st.markdown(result["ad_final"])
        
        # تفاصيل إضافية (اختياري)
        with st.expander("📋 عرض الخطط الكاملة (CEO / CTO / COO)"):
            st.markdown("### خطة CEO")
            st.markdown(result["ceo"])
            st.markdown("### خطة CTO")
            st.markdown(result["cto"])
            st.markdown("### خطة COO")
            st.markdown(result["coo"])

# ===== أزرار سيادية إضافية =====
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⚡ GO SPEED TEST"):
        st.write(call_super_ai("قول كلمة واحدة", "Test", "Test"))
with col2:
    if st.button("📊 GO STATS"):
        st.json(st.session_state)
with col3:
    if st.button("🔄 GO RESET"):
        st.session_state.clear()
        st.rerun()
