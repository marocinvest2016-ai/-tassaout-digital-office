import streamlit as st
import requests
from google_connector import get_google_sheets_data, calculate_roi_from_sheet

# ===== قائمة نماذج Groq محدثة مع fallback تلقائي =====
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.2-11b-vision-preview",
    "llama-3.3-70b-versatile",
]

def call_super_ai(prompt, agent_name, domain):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود."

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
            
            if res.status_code in (404, 400, 429):
                last_error = f"⚠️ النموذج {model} غير متاح (HTTP {res.status_code}). جاري تجربة البديل..."
                continue
            
            res.raise_for_status()
            st.session_state.last_model_used = model
            st.session_state.last_model_status = "✅ نجح"
            return res.json()['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            last_error = f"⏱️ انتهت مهلة {model}. جاري تجربة البديل..."
            continue
        except Exception as e:
            last_error = f"❌ خطأ {model}: {type(e).__name__}"
            continue

    st.session_state.last_model_status = "❌ فشل"
    return f"❌ تعذر الاتصال بجميع النماذج.

آخر خطأ: {last_error}"

def send_whatsapp_alert(message):
    try:
        phone_id = st.secrets.get('WHATSAPP_PHONE_NUMBER_ID')
        access_token = st.secrets.get('WHATSAPP_ACCESS_TOKEN')
        target_number = st.secrets.get('WHATSAPP_BUSINESS_NUMBER')
        version = st.secrets.get('WHATSAPP_API_VERSION', 'v20.0')

        if not all([phone_id, access_token, target_number]):
            st.warning("⚠️ إعدادات WhatsApp غير مكتملة")
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
            st.warning(f"⚠️ فشل WhatsApp: HTTP {res.status_code}")
    except Exception as e:
        st.warning(f"⚠️ خطأ WhatsApp: {e}")

class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        prompt = (
            f"بصفتك CEO فائق، ضع خطة استراتيجية شاملة وتنافسية لهذا المشروع في مجال {self.domain}: {task}.

"
            f"المطلوب:
"
            f"1. تحليل SWOT مفصّل
"
            f"2. الميزة التنافسية الأساسية
"
            f"3. خطة تنفيذية لمدة 90 يوم
"
            f"4. مؤشرات الأداء الرئيسية KPIs

"
            f"جاوب بالدارجة المغربية + العربية الفصحى، مع تنسيق احترافي."
        )
        return call_super_ai(prompt, "Super CEO Agent", self.domain)

    def cto(self, task):
        prompt = (
            f"بصفتك CTO فائق، اقترح الاستراتيجية التقنية وأدوات التشغيل لـ: {task} في {self.domain}.

"
            f"المطلوب:
"
            f"1. البنية التقنية (Tech Stack)
"
            f"2. أدوات التشغيل والأتمتة
"
            f"3. استهداف الجمهور الرقمي
"
            f"4. خطة الأمان

"
            f"جاوب بالدارجة + الفصحى، مع تنسيق احترافي."
        )
        return call_super_ai(prompt, "Super CTO Agent", self.domain)

    def coo(self, task):
        financial_context = ""
        if hasattr(st.session_state, 'financial_data') and st.session_state.financial_data:
            fd = st.session_state.financial_data
            financial_context = (
                f"

[البيانات المالية من Google Drive]:
"
                f"• الإيرادات: {fd['total_revenue']:,.0f} درهم
"
                f"• المصاريف: {fd['total_expenses']:,.0f} درهم
"
                f"• الربح: {fd['total_profit']:,.0f} درهم
"
                f"• ROI: {fd['avg_roi']:.1f}%
"
            )
        
        prompt = (
            f"بصفتك COO فائق، ضع خطة تنفيذية لـ: {task} في {self.domain}.{financial_context}

"
            f"المطلوب:
"
            f"1. هيكل الفريق
"
            f"2. الجدولة الزمنية
"
            f"3. KPIs
"
            f"4. إدارة المخاطر

"
            f"جاوب بالدارجة + الفصحى."
        )
        return call_super_ai(prompt, "Super COO Agent", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get('WHATSAPP_BUSINESS_NUMBER', '')
        prompt = (
            f"بناءً على هذه الخطة:

{plan}

"
            f"اكتب 3 إعلانات تسويقية بالدارجة والفصحى مع:
"
            f"• عنوان قوي
"
            f"• نص مقنع
"
            f"• CTA مع واتساب: {whatsapp_num}
"
            f"• هاشتاقات (3-5)
"
            f"• إيموجيز

"
            f"مناسبة لـ Facebook, Instagram, WhatsApp."
        )
        ad = call_super_ai(prompt, "Super Copywriter Agent", self.domain)
        
        alert_msg = (
            f"👑 OMEGA v4.5
"
            f"📂 المجال: {self.domain}
"
            f"🤖 النموذج: {st.session_state.get('last_model_used', 'N/A')}

"
            f"📝 الإعلان:
{ad[:1500]}..."
        )
        send_whatsapp_alert(alert_msg)
        return ad

    def closer(self, ad):
        prompt = (
            f"حسن هذا الإعلان لزيادة المبيعات:

{ad}

"
            f"أضف:
"
            f"1. FOMO (عرض محدود)
"
            f"2. ضمان قوي
"
            f"3. شهادات عملاء
"
            f"4. FAQ قصيرة
"
            f"5. CTA أقوى

"
            f"حافظ على اللهجة والتنسيق."
        )
        return call_super_ai(prompt, "Super Closer Agent", self.domain)

    def full_pipeline(self, task):
        with st.spinner("🧠 جاري التحليل..."):
            ceo_plan = self.ceo(task)
        
        with st.spinner("⚙️ جاري الخطة التقنية..."):
            cto_plan = self.cto(task)
        
        with st.spinner("📋 جاري الخطة التنفيذية..."):
            coo_plan = self.coo(task)
        
        combined = f"=== CEO ===
{ceo_plan}

=== CTO ===
{cto_plan}

=== COO ===
{coo_plan}"
        
        with st.spinner("✍️ جاري الإعلانات..."):
            ad = self.copywriter(combined)
        
        with st.spinner("🔥 جاري التحسين..."):
            final = self.closer(ad)
        
        return {
            "ceo": ceo_plan, "cto": cto_plan, "coo": coo_plan,
            "ad_original": ad, "ad_final": final,
            "model_used": st.session_state.get('last_model_used', 'N/A')
        }

# ===== واجهة Streamlit =====
st.set_page_config(page_title="👑 OMEGA v4.5", page_icon="🤖", layout="wide")
st.title("👑 OMEGA SUPER AGENTIC v4.5 + Google Drive")
st.markdown("**Groq + Llama + Google Sheets**")

# تحميل البيانات المالية
with st.spinner("📊 جاري تحميل البيانات من Drive..."):
    financial_data = get_google_sheets_data()
    if financial_data is not None:
        roi_stats = calculate_roi_from_sheet(financial_data)
        if roi_stats:
            st.session_state.financial_data = roi_stats
            st.success(f"✅ إيرادات: {roi_stats['total_revenue']:,.0f} درهم | ROI: {roi_stats['avg_roi']:.1f}%")
        else:
            st.warning("⚠️ لا توجد أعمدة مالية")
    else:
        st.info("ℹ️ Drive غير مفعّل")

domain = st.selectbox("المجال", ["العقار", "التسويق", "الزيتون", "أخرى"], index=0)
task = st.text_area("المهمة", placeholder="مثلاً: إطلاق منصة عقارية...", height=150)

if st.button("🚀 تنفيذ", type="primary"):
    if not task.strip():
        st.error("⚠️ أدخل المهمة")
    else:
        agent = SuperOmegaAgent(domain)
        with st.spinner("جاري..."):
            result = agent.full_pipeline(task)
        
        st.success("✅ تم!")
        if "last_model_used" in st.session_state:
            st.info(f"🤖 النموذج: {st.session_state.last_model_used}")
        
        st.subheader("📢 الإعلان الأصلي")
        st.markdown(result["ad_original"])
        
        st.subheader("🔥 الإعلان المحسّن")
        st.markdown(result["ad_final"])
        
        with st.expander("📋 الخطط الكاملة"):
            st.markdown("### CEO"); st.markdown(result["ceo"])
            st.markdown("### CTO"); st.markdown(result["cto"])
            st.markdown("### COO"); st.markdown(result["coo"])

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⚡ TEST"):
        st.write(call_super_ai("قل كلمة", "Test", "Test"))
with col2:
    if st.button("📊 STATS"):
        st.json(st.session_state)
with col3:
    if st.button("🔄 RESET"):
        st.session_state.clear()
        st.rerun()
