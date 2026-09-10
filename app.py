import streamlit as st
import requests
from google_connector import get_google_sheets_data, calculate_roi_from_sheet

# === موديلات محدثة (سبتمبر 2026) ===
# llama-3.1-8b و llama-3.3-70b تدهورت فـ 16 غشت 2026
GROQ_MODELS = [
    "openai/gpt-oss-20b",          # سريع ورخيص
    "openai/gpt-oss-120b",         # قوي
    "llama-3.3-70b-versatile",     # fallback (Enterprise)
    "llama-3.1-8b-instant",        # fallback
]

def call_super_ai(prompt, agent_name, domain):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        return "❌ خطأ: مفتاح GROQ_API_KEY غير موجود فـ الخزنة."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are {agent_name}, an elite Super Agentic AI specialized in '{domain}' "
        f"powered by fast models on Groq. Think step by step. "
        f"Respond in Moroccan Arabic Darija + العربية الفصحى."
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
                last_error = f"⚠️ {model} غير متاح ({res.status_code}). جاري البديل..."
                continue

            res.raise_for_status()
            st.session_state.last_model_used = model
            st.session_state.last_model_status = "✅ نجح"
            return res.json()["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            last_error = f"⏱️ {model} timeout."
            continue
        except Exception as e:
            last_error = f"❌ {model}: {str(e)[:120]}"
            continue

    st.session_state.last_model_status = "❌ فشل"
    return "❌ تعذر الاتصال بالنماذج. " + (last_error or "")


def send_whatsapp_alert(message):
    try:
        phone_id = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID")
        access_token = st.secrets.get("WHATSAPP_ACCESS_TOKEN")
        target_number = st.secrets.get("WHATSAPP_BUSINESS_NUMBER")
        version = st.secrets.get("WHATSAPP_API_VERSION", "v20.0")

        if not all([phone_id, access_token, target_number]):
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
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass


class SuperOmegaAgent:
    def __init__(self, domain):
        self.domain = domain

    def ceo(self, task):
        prompt = f"""بصفتك CEO فائق، ضع خطة استراتيجية لـ {self.domain}: {task}.

المطلوب:
1. SWOT
2. الميزة التنافسية
3. خطة 90 يوم
4. KPIs

جاوب بالدارجة + الفصحى."""
        return call_super_ai(prompt, "CEO", self.domain)

    def cto(self, task):
        prompt = f"""بصفتك CTO فائق، اقترح Tech Stack لـ {task} في {self.domain}.

المطلوب:
1. البنية التقنية
2. الأتمتة
3. استهداف رقمي
4. أمان

جاوب بالدارجة + الفصحى."""
        return call_super_ai(prompt, "CTO", self.domain)

    def coo(self, task):
        financial_context = ""
        if hasattr(st.session_state, "financial_data") and st.session_state.financial_data:
            fd = st.session_state.financial_data
            financial_context = f"\n\n[Drive]: إيرادات {fd['total_revenue']:,.0f} درهم | ROI {fd['avg_roi']:.1f}%"
        
        prompt = f"""بصفتك COO فائق، ضع خطة تنفيذية لـ {task} في {self.domain}.{financial_context}

المطلوب:
1. الفريق
2. الجدولة
3. KPIs
4. المخاطر

جاوب بالدارجة + الفصحى."""
        return call_super_ai(prompt, "COO", self.domain)

    def copywriter(self, plan):
        whatsapp_num = st.secrets.get("WHATSAPP_BUSINESS_NUMBER", "")
        prompt = f"""بناءً على: {plan}

اكتب 3 إعلانات بالدارجة والفصحى مع:
• عنوان
• نص
• CTA: {whatsapp_num}
• هاشتاقات
• إيموجيز"""
        ad = call_super_ai(prompt, "Copywriter", self.domain)
        send_whatsapp_alert(f"👑 OMEGA v4.5\n📂 {self.domain}\n📝 {ad[:1000]}...")
        return ad

    def closer(self, ad):
        prompt = f"""حسن هذا الإعلان:

{ad}

أضف:
1. FOMO
2. ضمان
3. شهادات
4. FAQ
5. CTA أقوى"""
        return call_super_ai(prompt, "Closer", self.domain)

    def full_pipeline(self, task):
        with st.spinner("🧠 CEO..."):
            ceo = self.ceo(task)
        with st.spinner("⚙️ CTO..."):
            cto = self.cto(task)
        with st.spinner("📋 COO..."):
            coo = self.coo(task)
        
        combined = f"=== CEO ===\n{ceo}\n\n=== CTO ===\n{cto}\n\n=== COO ===\n{coo}"
        
        with st.spinner("✍️ Copy..."):
            ad = self.copywriter(combined)
        with st.spinner("🔥 Close..."):
            final = self.closer(ad)
        
        return {
            "ceo": ceo,
            "cto": cto,
            "coo": coo,
            "ad_original": ad,
            "ad_final": final
        }


# ==================== الواجهة ====================
st.set_page_config(page_title="👑 OMEGA v4.5", page_icon="🤖", layout="wide")
st.title("👑 OMEGA SUPER AGENTIC v4.5 + Google Drive")

# محاولة جلب البيانات المالية
with st.spinner("📊 جاري الاتصال بـ Drive..."):
    financial_data = get_google_sheets_data()
    if financial_data:
        roi = calculate_roi_from_sheet(financial_data)
        if roi:
            st.session_state.financial_data = roi
            st.success(f"✅ إيرادات: {roi['total_revenue']:,.0f} درهم | ROI: {roi['avg_roi']:.1f}%")
        else:
            st.info("ℹ️ تم الاتصال بالشيت ولكن ما قدرناش نحسبو ROI")
    else:
        st.info("ℹ️ ما كاينش بيانات مالية من Google Sheets (التطبيق غادي يخدم عادي)")

domain = st.selectbox("المجال", ["العقار", "التسويق", "الزيتون", "أخرى"])
task = st.text_area("المهمة", placeholder="مثلاً: إطلاق منصة...", height=100)

if st.button("🚀 تنفيذ", type="primary"):
    if not task.strip():
        st.error("⚠️ أدخل المهمة")
    else:
        agent = SuperOmegaAgent(domain)
        with st.spinner("جاري التنفيذ الكامل..."):
            result = agent.full_pipeline(task)
        
        st.success("✅ تم بنجاح!")
        
        # عرض الموديل اللي خدم
        if hasattr(st.session_state, "last_model_used"):
            st.caption(f"الموديل المستخدم: `{st.session_state.last_model_used}` | {st.session_state.last_model_status}")
        
        st.subheader("📢 الإعلان النهائي")
        st.markdown(result["ad_final"])
        
        with st.expander("📋 الخطط الكاملة"):
            st.markdown("### 🧠 CEO")
            st.markdown(result["ceo"])
            st.markdown("### ⚙️ CTO")
            st.markdown(result["cto"])
            st.markdown("### 📋 COO")
            st.markdown(result["coo"])
