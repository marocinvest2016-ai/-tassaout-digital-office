import streamlit as st
import requests
import json
import time

st.set_page_config(
    page_title="OMEGA Super Agentic AI - Enterprise", 
    page_icon="👑", 
    layout="wide"
)

# ===== المحرك الذكي الموحد (Groq API) =====
def call_super_ai(prompt, agent_name, domain):
    """محرك الذكاء الاصطناعي الفائق متعدد المجالات المدعوم بـ Groq و Llama"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets الخاصة بـ Streamlit."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite, autonomous Super Agentic AI specialized in '{domain}' "
        f"powered by Meta Llama on Groq. Think deeply step by step. Provide professional, highly tailored, "
        f"actionable strategies, execution steps, and precise metrics. "
        f"Respond professionally in Moroccan Arabic Darija mixed with Standard Arabic (العربية الفصحى), "
        f"using clean formatting, bullet points, emojis, and tables where applicable."
    )

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2500
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ خطأ في الاتصال بنظام الذكاء الاصطناعي: {e}"

# ===== خدمة إرسال الإشعارات عبر واتساب =====
def send_whatsapp_alert(message):
    """إرسال تنبيهات تلقائية عبر Meta WhatsApp Cloud API"""
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

        if not all([phone_id, access_token, target_number]):
            return False

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
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        st.warning(f"تعذر إرسال إشعار الواتساب: {e}")
        return False

# ===== هيكل الوكلاء الأذكياء (Multi-Agent System) =====
class SuperOmegaOrchestrator:
    def __init__(self, domain):
        self.domain = domain

    def run_ceo(self, task):
        prompt = (
            f"بصفتك المدير التنفيذي (CEO) الفائق، قم بتحليل هذا المشروع في مجال {self.domain}: '{task}'. "
            f"قدم لي خطة استراتيجية شاملة تحتوي على: تحليل SWOT، الميزة التنافسية الفريدة، وتخطيط زمني دقيق لـ 90 يوماً."
        )
        return call_super_ai(prompt, "Super CEO Agent", self.domain)

    def run_cto(self, task):
        prompt = (
            f"بصفتك المدير التقني (CTO) الفائق، بناءً على المشروع في مجال {self.domain}: '{task}'. "
            f"اقترح البنية التحتية التقنية المناسبة، أدوات التشغيل الرقمية، تكديس التقنيات (Tech Stack)، وأدوات الأتمتة لضمان كفاءة العمل."
        )
        return call_super_ai(prompt, "Super CTO Agent", self.domain)

    def run_coo(self, task):
        prompt = (
            f"بصفتك مدير العمليات (COO) الفائق، للمشروع في مجال {self.domain}: '{task}'. "
            f"ضع خطة تشغيلية يومية، مؤشرات الأداء الرئيسية (KPIs)، إدارة الموارد المتاحة، وجدولة زمنية صارمة للتنفيذ."
        )
        return call_super_ai(prompt, "Super COO Agent", self.domain)

    def run_copywriter(self, strategy_plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', 'الهاتف غير محدد')
        prompt = (
            f"بناءً على هذه الاستراتيجية التنفيذية:\n{strategy_plan}\n\n"
            f"بصفتك خبير كتابة إعلانية (Copywriter)، اكتب 3 صيغ إعلانية تسويقية قوية جداً باللهجة المغربية والفلصحة المبسطة، "
            f"تتضمن عناوين جذابة، فوائد واضحة، هاشتاقات، ودعوة مباشرة لاتخاذ الإجراء (Call to Action) عبر الواتساب على الرقم: {whatsapp_num}"
        )
        ad_text = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        return ad_text

    def run_closer(self, ad_copy):
        prompt = (
            f"بصفتك خبير مبيعات وإغلاق صفقات (Closer) محترف، قم بتحسين هذا النص الإعلاني:\n{ad_copy}\n\n"
            f"أضف إليه محفزات الاستعجال الحقيقي (FOMO)، ضمانات قوية لإزالة المخاطر لدى الزبون، وعناصر لبناء الثقة الفورية لرفع نسبة المبيعات."
        )
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

# ===== واجهة المستخدم الاحترافية (Streamlit UI) =====
st.title("👑 OMEGA Super Agentic AI - Multi-Domain Enterprise")
st.caption("النظام الذكي المتكامل للوكلاء المتعددين (CEO + CTO + COO + Copywriter + Closer) مدعوم بـ Groq Llama 3.1")

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("⚙️ إعدادات النظام")
    domain = st.selectbox(
        "اختر قطاع العمل (Domain)", 
        ["العقار والمقاولات", "التجارة الإلكترونية (E-commerce)", "المطاعم والضيافة", "التعليم والتدريب", "الخدمات الطبية والصحية", "التسويق الرقمي والوكالات"]
    )
    st.info("💡 نصيحة: حدد بدقة تفاصيل المشروع في مربع النص للحصول على نتائج دقيقة وقابلة للتنفيذ الفوري.")
    st.markdown("---")
    st.write("📌 **الإصدار:** v5.0 Autonomous")

# واجهة المدخلات الرئيسية
task = st.text_area(
    "📝 أدخل تفاصيل المهمة أو المشروع المراد إنجازه:", 
    placeholder="مثال: تسويق وبيع بقع أرضية سكنية في تجزئة الهدى بقلعة السراغنة مع استهداف المستثمرين المغاربة المقيمين بالخارج.",
    height=100
)

orchestrator = SuperOmegaOrchestrator(domain)

# تبويبات العمل المستقل لكل وكيل
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 الاستراتيجية (CEO)", "💻 التقنية (CTO)", "📊 العمليات (COO)", "✍️ الحملة الإعلانية", "🚀 دورة المبيعات الكاملة (Pipeline)"])

with tab1:
    if st.button("تشغيل وكيل CEO", key="btn_ceo"):
        if not task.strip():
            st.warning("⚠️ يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("المدير التنفيذي الفائق يحلل السوق ويضع الاستراتيجية..."):
                result = orchestrator.run_ceo(task)
                st.markdown(result)

with tab2:
    if st.button("تشغيل وكيل CTO", key="btn_cto"):
        if not task.strip():
            st.warning("⚠️ يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("المدير التقني يجهز البنية التحتية والتقنيات..."):
                result = orchestrator.run_cto(task)
                st.markdown(result)

with tab3:
    if st.button("تشغيل وكيل COO", key="btn_coo"):
        if not task.strip():
            st.warning("⚠️ يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("مدير العمليات ينظم مسار التشغيل والمؤشرات..."):
                result = orchestrator.run_coo(task)
                st.markdown(result)

with tab4:
    if st.button("توليد الإعلان التسويقي", key="btn_copy"):
        if not task.strip():
            st.warning("⚠️ يرجى إدخال وصف المهمة أولاً.")
        else:
            with st.spinner("كاتب الإعلانات المحترف يصيغ الحملة..."):
                plan = orchestrator.run_ceo(task)
                ad_result = orchestrator.run_copywriter(plan)
                st.markdown(ad_result)

with tab5:
    st.subheader("⚡ مسار الأتمتة الشامل (Full Autonomous Pipeline)")
    st.write("هذا الزر يشغل السلسلة كاملة: استراتيجية CEO -> صياغة الإعلان -> تحسين المبيعات بالـ Closer -> إرسال التنبيه تلقائياً عبر WhatsApp API.")
    
    if st.button("🚀 تنفيذ المسار الفائق بالكامل وإرسال التنبيه", type="primary", key="btn_full"):
        if not task.strip():
            st.warning("⚠️ يرجى إدخال وصف المهمة أولاً.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("1/4 - جارٍ إعداد الاستراتيجية الكبرى (CEO)...")
            progress_bar.progress(25)
            plan = orchestrator.run_ceo(task)

            status_text.text("2/4 - جارٍ كتابة الإعلانات الترويجية (Copywriter)...")
            progress_bar.progress(50)
            ad = orchestrator.run_copywriter(plan)

            status_text.text("3/4 - تحسين الإعلان عبر خبير الإغلاق (Closer & FOMO)...")
            progress_bar.progress(75)
            final_output = orchestrator.run_closer(ad)

            status_text.text("4/4 - إرسال التقرير النهائي عبر واتساب API...")
            progress_bar.progress(90)
            
            whatsapp_msg = f"👑 *OMEGA SUPER AGENTIC v5.0*\n🎯 القطاع: {domain}\n\n{final_output}"
            sent_status = send_whatsapp_alert(whatsapp_msg)

            progress_bar.progress(100)
            status_text.text("✅ تمت العملية بنجاح تام!")

            if sent_status:
                st.success("📩 تم إرسال الإشعار والتفاصيل بنجاح إلى رقم الواتساب المخصص في إعدادات Secrets!")
            else:
                st.info("ℹ️ تم إعداد المخرجات بالأسفل بنجاح (تأكد من إعدادات مفاتيح الواتساب في حال رغبتك بالتنبيه التلقائي).")

            st.markdown("---")
            st.markdown(final_output)
